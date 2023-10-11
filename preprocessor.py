import re
import pandas as pd
def preprocess(data):
    pattern = '\d{1,2}/\d{1,2}/\d{2},\s\d{1,2}:\d{2}\s[APap][Mm]\s-\s'

    messages = re.split(pattern, data)[1:]
    dates = re.findall(pattern, data)

    df = pd.DataFrame({'message_date': dates, 'user_message': messages})
    df['message_date'] = pd.to_datetime(df['message_date'], format="%m/%d/%y, %I:%M %p - ")
    df.rename(columns={'message_date': 'date'}, inplace=True)

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:
            users.append(entry[1])
            messages.append(entry[2])
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['users'] = users
    df['message'] = messages
    df.drop(columns='user_message', inplace=True)

    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month_name()
    df['month_num'] = df['date'].dt.month
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 12:
            period.append(str(hour) + " PM - " + str(1) + " PM")
        elif hour == 11:
            period.append(str(hour) + " AM - " + str(hour + 1) + " AM")
        elif hour == 23:
            period.append(str(hour - 12) + " PM - " + str(12) + " AM")
        elif hour == 0:
            period.append(str(12) + " AM - " + str(hour + 1) + " AM")
        elif hour > 11:
            period.append(str(hour - 12) + " PM - " + str(hour + 1 - 12) + " PM")
        else:
            period.append(str(hour) + " AM - " + str(hour + 1) + " AM")

    df['period'] = period
    df['period'] = df['period'].sort_values()

    return df