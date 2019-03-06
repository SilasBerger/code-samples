from flask import request
from flask import jsonify
from src.database import neo4j_binding


def route(app):
    # =================== Demo Routes =================== #
    @app.route('/')
    def hello_world():
        return 'Hello, World!'

    @app.route('/data')
    def data():
        dat = {"name": "silas", "age": 24}
        return jsonify(dat)

    @app.route("/echoPost", methods=["POST"])
    def echo_post():
        json_data = request.get_json()
        return jsonify({"yourRequestData": json_data})

    @app.route("/echoUser/<user_name>")
    def echo_user(user_name):
        return jsonify({"yourUsername": user_name})

    @app.route("/echoQuery")
    def echo_query():
        query_dict = request.args
        return jsonify({"yourQuery": query_dict})
    # ================= End Demo Routes ================== #

    # ================ Future Routes ===================== #
    @app.route("/query/user/<user_id>", methods=["GET", "POST"])
    def query_user(user_id):
        if request.method == "POST":
            commit_to_graph = request.get_json().get("commitToGraph")
            if type(commit_to_graph) != bool:
                return bad_request_response("commitToGraph"), 400
        else:
            commit_to_graph = False
        return jsonify({"user_id": user_id, "handle": "@RealDonaldTrump", "isSwiss": True, "isSwissConfidence": 0.78,
                        "committedToGraph": commit_to_graph})
    # ============= End Future Routes ==================== #

    # ===================== Routes ======================= #
    # TODO: introduce optional min confidence where it makes sense
    @app.route("/statistics/usersInGraph")
    def stat_users_in_graph():
        return jsonify({"result": neo4j_binding.count_all_users()})

    @app.route("/statistics/tweetsInGraph")
    def stat_tweets_in_graph():
        return jsonify({"result": neo4j_binding.count_all_tweets()})

    @app.route("/statistics/swissUsers")
    def stat_swiss_users():
        return jsonify({"result": neo4j_binding.count_all_swiss_users()})

    @app.route("/statistics/swissTweets")
    def stat_swiss_tweets():
        return jsonify({"result": neo4j_binding.count_swiss_tweets()})

    @app.route("/statistics/standardSwissUsers")
    def stat_standard_swiss_users():
        return jsonify({"result": neo4j_binding.count_standard_swiss_users()})

    @app.route("/statistics/swissInfluencers")
    def stat_swiss_influencers():
        return jsonify({"result": neo4j_binding.count_swiss_influencers()})
    # ================== End Routes ====================== #

    # ================== Helpers ========================= #
    def bad_request_response(bad_parameter):
        return jsonify({"badOrMissingParameter": bad_parameter})
    # ================ End Helpers ======================= #
