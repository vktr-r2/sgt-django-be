import datetime

def format_date(date_string):
    date_int = int(date_string)
    date = datetime.datetime.fromtimestamp(date_int / 1000)
    return date