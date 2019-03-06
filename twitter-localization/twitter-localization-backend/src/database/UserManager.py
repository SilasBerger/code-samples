import pymongo
import time
from src.util import context
from src.database.neo4j_binding import Neo4jBinding
from src.model import crawl_status


class UserManager:
    """
    Handles the synchronization of Twitter user objects among the Twitter API, MongoDB, and the graph
    """

    _crawl_delay_seconds = 0.1

    def __init__(self, twitter_api_binding):
        self.neo4j = Neo4jBinding()
        self.twitter = twitter_api_binding
        self._connect()

    def _connect(self):
        self._host_connection = pymongo.MongoClient(context.get_config("mongodb_host"))
        self._database_connection = self._host_connection[context.get_config("influencers_db")]
        self._influencers_mongodb = self._database_connection[context.get_config("influencers_collection")]
        self._users_mongodb = self._database_connection[context.get_config("users_collection")]

    def update_influencers_in_database(self, update_existing_users=False):
        """
        Iterate through influencer list, fetch Twitter user for every influencer based on screen name, reduce
        user to predefined set of field and set type=influencer ("normalize"); add user to users collection in DB,
        or update existing user.
        :param update_existing_users: if False, users influencers will be skipped if they already exist in the users
                collection. If True, existing users will be updated with the latest information from the Twitter API.
        """
        print("Updating influencers in database")
        progress = 0
        influencers_cursor = self._influencers_mongodb.find()
        for influencer_entry in influencers_cursor:
            if (not update_existing_users) and self._user_exists_in_db(influencer_entry):
                continue
            influencer_user = self.twitter.find_user(influencer_entry["screen_name"])
            if influencer_user is None:
                self._handle_user_not_found(influencer_entry)
                continue
            self._update_user_in_mongo(influencer_user, influencer_entry["category"])
            progress += 1
            self._set_crawl_status(influencer_entry, crawl_status.collected)
            print("{} users fetched/updated".format(progress))
            time.sleep(UserManager._crawl_delay_seconds)
        print("done")

    def sync_graph_influencers_with_database(self):
        """
        Filters database for users marked as influencers and adds them to the graph, or updates them if they
        aready exist in the graph
        """
        influencers_cursor = self._users_mongodb.find({"type": "influencer"})
        for influencer_user in influencers_cursor:
            if self.neo4j.user_exists(influencer_user["screen_name"]):
                # TODO handle updating existing users
                continue
            n_user = self._normalize_user_for_graph(influencer_user)
            self._set_crawl_status(influencer_user, crawl_status.in_graph)
            self.neo4j.insert_user(n_user)

    def _handle_user_not_found(self, influencer_entry):
        print("user '{}' suspended or not found, skipping".format(influencer_entry["screen_name"]))
        influencer_entry["crawl_status"] = crawl_status.not_found
        self._influencers_mongodb.save(influencer_entry)

    def _update_user_in_mongo(self, user, influencer_category):
        n_user = UserManager._normalize_user_for_mongo(user, influencer_category)
        existing_user = self._users_mongodb.find_one({"screen_name": n_user["screen_name"]})
        if existing_user is not None:
            # user with that screen name already exists in the collection, preserve static information
            n_user["_id"] = existing_user["_id"]
        self._users_mongodb.save(n_user)

    def _user_exists_in_db(self, user):
        return self._users_mongodb.find_one({"screen_name": user["screen_name"]}) is not None

    @staticmethod
    def _normalize_user_for_mongo(user, influencer_category):
        normalized_user = {}
        for field in context.get_config("collect_user_fields"):
            normalized_user[field] = getattr(user, field)
        normalized_user["user_place"] = {
            "time_zone": user.time_zone,
            "utc_offset": user.utc_offset,
            "location": user.location
        }
        normalized_user["type"] = "influencer"
        normalized_user["influencer_category"] = influencer_category
        return normalized_user

    @staticmethod
    def _normalize_user_for_graph(user):
        normalized_user = {}
        for field in context.get_config("user_fields_in_graph"):
            normalized_user[field] = user[field]
        normalized_user["influencer_category"] = user["influencer_category"]
        return normalized_user

    def _set_crawl_status(self, influencer_entry, crawl_status):
        influencer_entry["crawl_status"] = crawl_status
        self._influencers_mongodb.save(influencer_entry)
