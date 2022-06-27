import datetime
from datetime import timedelta


def encode_date(DATE):
    return int(DATE[:2]),int(DATE[3:5]),int(DATE[6:])


def get_dates_list(START,END): # NOT INCLUDE THE END DATE
    START_d,START_m,START_y = encode_date(START)

    END_d,END_m,END_y= encode_date(END)

    start_date = datetime.date(START_y, START_m, START_d)
    end_date = start_date + timedelta(days=1)

    stop = datetime.date(END_y, END_m, END_d)
    # stop = datetime.date.today() #####

    single_date = start_date
    all_dates = []

    while single_date != stop:
        all_dates.append(single_date)
        single_date += timedelta(days=1)
        end_date = single_date + timedelta(days=1)

    return all_dates


print(get_dates_list("01/07/2020","05/07/2020"))