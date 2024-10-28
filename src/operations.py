from datetime import datetime


def extract_date(datetime_str):
    """
    Extracts the date from an ISO 8601 datetime string.

    Parameters:
        datetime_str (str): The datetime string in ISO 8601 format.

    Returns:
        str: The date in 'YYYY-MM-DD' format.
    """
    try:
        dt = datetime.fromisoformat(datetime_str)
        return dt.date().isoformat()
    except ValueError:
        print("Invalid datetime format. Please provide a string in ISO 8601 format.")
        return None


def extract_time(datetime_str):
    """
    Extracts the time from an ISO 8601 datetime string.

    Parameters:
        datetime_str (str): The datetime string in ISO 8601 format.

    Returns:
        str: The time in 'HH:MM:SS' format.
    """
    try:
        dt = datetime.fromisoformat(datetime_str)
        return dt.time().isoformat()
    except ValueError:
        print("Invalid datetime format. Please provide a string in ISO 8601 format.")
        return None
