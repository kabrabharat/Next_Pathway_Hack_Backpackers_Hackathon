def get_DateFromDaysSince2(days, date):
    if days>=0:
        final_date = addDays(date, days)
    else:
        final_date = subDays(date, days)

    return final_date