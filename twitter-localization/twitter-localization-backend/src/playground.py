from src.util import context
from src.twitter.TwitterApiBinding import TwitterApiBinding
from src.database.InfluencerListManager import InfluencerListManager
from src.database.UserManager import UserManager


def main():
    context.load_credentials()
    context.load_config()
    twitter_api_binding = TwitterApiBinding()
    user_manager = UserManager(twitter_api_binding)
    user_manager.update_influencers_in_database()
    user_manager.sync_graph_influencers_with_database()


if __name__ == "__main__":
    main()