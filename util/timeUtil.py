from datetime import datetime


def days_between(d1, d2):
    d1 = datetime.strptime(d1,  "%Y-%m-%dT%H:%M:%SZ")
    d2 = datetime.strptime(d2,  "%Y-%m-%dT%H:%M:%SZ")
    return abs((d2 - d1).days)