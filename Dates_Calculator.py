import datetime
from datetime import timedelta

def get_dates(START,END): # returns the range dates, day by day
    dates = (get_dates_list(START, END)) # list of dates
    return get_dates_string_list(dates) # list of strings

def encode_date(DATE):
    return int(DATE[:2]),int(DATE[3:5]),int(DATE[6:])

def check(s):
    if(len(s)==1): return "0"+s
    return s

def decode_date(DATE):
    return check(str(DATE.day)) +"-" +check(str(DATE.month))+"-" + check(str(DATE.year))


def get_dates_list(START,END):
    START_d,START_m,START_y = encode_date(START)

    END_d,END_m,END_y= encode_date(END)

    start_date = datetime.date(START_y, START_m, START_d)

    end_date = start_date + timedelta(days=1)

    stop = datetime.date(END_y, END_m, END_d)
    # stop = datetime.date.today() #####

    single_date = start_date
    all_dates = [single_date]

    while single_date != stop:

        single_date += timedelta(days=1)

        end_date = single_date + timedelta(days=1)
        all_dates.append(single_date)

    return all_dates

def get_dates_string_list(DATES):
    string_list_dates = []
    for date in DATES:
        string_list_dates.append(decode_date(date))
    return string_list_dates

