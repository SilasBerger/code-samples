import datetime


def get_timestamp():
    """
    Get current time as formatted string
    :return: current time string in the format YYYY-mm-dd HH:MM
    """
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M")