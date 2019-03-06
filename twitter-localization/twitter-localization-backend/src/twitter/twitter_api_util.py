import math
import time
import tweepy
from src.util import timing


def get_rate_limit_status(twitter_api):
    """
    Get full rate limit status from API (warning: rate limiting applies to this endpoint as well)
    :param twitter_api: reference to the Tweepy API object
    :return: JSON object containing full rate limit status
    """
    return twitter_api.rate_limit_status()


def get_relevant_rate_limits(twitter_api):
    """
    Get rate limits of relevant endpoints. Currently includes '/search/tweets' and '/application/rate_limit_status'.
    Each status contains
        - limit (max. available calls per 15-minute window
        - remaining (remaining calls within current window)
        - reset (remaining minutes until window resets, always rounded up)
    :param twitter_api: reference to the Tweepy API object
    :return: aggregated rate limits status report, JSON object
    """
    current_status = twitter_api.rate_limit_status()
    search = _parse_rate_limit(current_status["resources"]["search"]["/search/tweets"])
    show_user = _parse_rate_limit(current_status["resources"]["users"]["/users/show/:id"])
    rate_limit_status = _parse_rate_limit(current_status["resources"]["application"]["/application/rate_limit_status"])
    return {
        "search": search,
        "show_user": show_user,
        "rate_limit_status": rate_limit_status
    }


def print_relevant_rate_limits(twitter_api):
    """
    Fetch and print aggregated rate limit report from get_relevant_rate_limits()
    :param twitter_api: reference to the Tweepy API object
    :return:
    """
    status = get_relevant_rate_limits(twitter_api)
    print(timing.get_timestamp() + ": rate limit '/search/tweets': " + str(status["search"])),
    print(timing.get_timestamp() + ": rate limit '/users/show/:id': " + str(status["show_user"]))
    print(timing.get_timestamp() + ": rate limit '/application/rate_limit_status': " + str(status["rate_limit_status"]))


def _parse_rate_limit(rl_node):
    """
    Extract limit/remaining/reset from a rate limit status report dict node corresponding to exactly one endpoint.
    Extract 'reset' field (UTC epoch seconds), convert to minutes, rounded up
    :param rl_node:
    :return:
    """
    limit = rl_node["limit"]
    remaining = rl_node["remaining"]
    reset = math.ceil((rl_node["reset"] - int(time.time())) / 60)
    return {
        "limit": limit,
        "remaining": remaining,
        "reset_in_minutes": reset
    }


def safe_check_search_rate_limit_reset(twitter_api):
    """
    Returns the remaining number of minutes to wait until the `/search` endpoint rate limit is lifted. Can
    used regardless of rate limitation on the `/rate_limits` endpoint itself.
    :param twitter_api: Tweepy binding
    :return: remaining rate limit time in minutes
    """
    # changed after commit db23a06964f27409ee0da740ff43702b9f3f83f2. Each endpoint has its own limit and reset time.
    # TODO: try finding a better way if possible
    return 15
