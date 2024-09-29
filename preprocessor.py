import re
import pandas as pd

def preprocess(data):
    pattern = '\[\d{2}/\d{2}/\d{2},\s\d{2}:\d{2}:\d{2}\s(?:AM|PM)\]\s'

    messages = re.split(pattern, data)[1:]
    d = re.findall(pattern, data)
    dates = [x[1:19] + " " + x[20:22] for x in d]
    dates = pd.to_datetime(dates).strftime('%d/%m/%Y, %H:%M')
    #print(dates[96])

    df = pd.DataFrame({"user_message": messages, "date": dates})
    # df = df.set_index(pd.to_datetime(df['date'].values))
    df["date"] = pd.to_datetime(df['date'], format="%d/%m/%Y, %H:%M")

    users = []
    messages = []
    for message in df['user_message']:
        entry = re.split('([\w\W]+?):\s', message)
        if entry[1:]:  # user name
            users.append(entry[1])
            messages.append(" ".join(entry[2:]))
        else:
            users.append('group_notification')
            messages.append(entry[0])

    df['user'] = users
    df['message'] = messages
    df.drop(columns=['user_message'], inplace=True)

    df['only_date'] = df['date'].dt.date
    df['year'] = df['date'].dt.year
    df['month_num'] = df['date'].dt.month
    df['month'] = df['date'].dt.month_name()
    df['day'] = df['date'].dt.day
    df['day_name'] = df['date'].dt.day_name()
    df['hour'] = df['date'].dt.hour
    df['minute'] = df['date'].dt.minute

    period = []
    for hour in df[['day_name', 'hour']]['hour']:
        if hour == 23:
            period.append(str(hour) + "-" + str('00'))
        elif hour == 0:
            period.append(str('00') + "-" + str(hour + 1))
        else:
            period.append(str(hour) + "-" + str(hour + 1))

    df['period'] = period

    return df