import time
import tweepy
from src.twitter import twitter_api_util
from src.util import context, timing


class TwitterApiBinding:
    """
    Wrapper around the Tweepy binding, facilitates fetching data, iterating through cursors, handling rate limits, etc.
    """

    # leaving some margin for error, rate limit resets after 15 minutes
    _RATE_LIMIT_DELAY_MINUTES = 16

    # check and print rate limits after crawling n pages
    _CHECK_LIMITS_AFTER_PAGES = 50

    def __init__(self):
        TwitterApiBinding._instance_created = True
        self._setup_twitter_api()

    def _setup_twitter_api(self):
        self._auth = tweepy.OAuthHandler(context.get_credentials("twitter_api_key"),
                                         context.get_credentials("twitter_api_key_secret"))
        self._auth.set_access_token(context.get_credentials("twitter_access_token"),
                                    context.get_credentials("twitter_access_token_secret"))
        self._twitter_api = tweepy.API(self._auth)

    def _await_rate_limit(self):
        wait_time = twitter_api_util.safe_check_search_rate_limit_reset(self._twitter_api) + 1
        print(timing.get_timestamp() + ":", "rate limit reached, waiting " + str(wait_time) + " minutes")
        time.sleep(wait_time * 60)

    def _handle_tweep_error_generic(self, tweep_error):
        if tweep_error.response.status_code == 429:
            # rate limit, wasn't caught as RateLimitError
            self._await_rate_limit()
            return True
        elif tweep_error.api_code in [63, 64]:
            # suspended user account
            return True
        else:
            # general tweep error, graceful shutdown
            print("TweepError encountered, shutting down")
            print("Error:", tweep_error)
            exit(1)

    def _iterate_cursor(self, cursor):
        """
        Cursor page generator, prints current rate limit status at set interval, excepts rate limit error, waits
        for specified interval until rate limit is lifted
        :param cursor: tweepy.Cursor to crawl
        :return: next page from Cursor
        """
        rate_limit_check_counter = 0
        while True:
            try:
                rate_limit_check_counter += 1
                if rate_limit_check_counter >= TwitterApiBinding._CHECK_LIMITS_AFTER_PAGES:
                    twitter_api_util.print_relevant_rate_limits(self._twitter_api)
                    rate_limit_check_counter = 0
                yield cursor.next()
            except tweepy.RateLimitError:
                self._await_rate_limit()
            except tweepy.TweepError as err:
                self._handle_tweep_error_generic(err)

    def _execute_api_call(self, call, *args):
        try:
            return call(*args)
        except tweepy.RateLimitError:
            self._await_rate_limit()
            self._execute_api_call(call, *args)
        except tweepy.TweepError as err:
            if err.response.status_code == 429:
                # rate limit, wasn't caught as RateLimitError
                self._await_rate_limit()
                return call(*args)
            elif err.api_code in [63, 64]:
                # suspended user account
                return None
            elif err.api_code == 50:
                # user not found
                return None
            else:
                # general tweep error, graceful shutdown
                print("TweepError encountered, shutting down")
                print("Error:", err)
                exit(1)


    # === Public API Calls === #

    def print_rate_limits(self):
        self._execute_api_call(twitter_api_util.print_relevant_rate_limits, self._twitter_api)

    def find_user(self, screen_name):
        return self._execute_api_call(self._twitter_api.get_user, screen_name)


    # TODO: duplications, insconsitstencies with errors, etc. => needs rework