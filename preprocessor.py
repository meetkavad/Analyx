import re
import pandas as pd 

def preprocessor(data):
    # pattern for date-time extraction from chat : 
    pattern_12hr = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[ap]m\s-\s'
    pattern_24hr = r'\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s-\s'

    messages = re.split(pattern_12hr, data)[1:]
    dates = re.findall(pattern_12hr, data)

    if not dates:
        messages = re.split(pattern_24hr, data)[1:]
        dates = re.findall(pattern_24hr, data)

    # removing '\u202f' from dates : 
    for idx, i in enumerate(dates): 
        dates[idx] = dates[idx].replace('\u202f', ' ')

    # converting dates to datetime format :

   # removing '\u202f' from dates : 
    for idx, i in enumerate(dates): 
        dates[idx] = dates[idx].replace('\u202f', ' ')

    # converting dates to datetime format:
    try:
        dates = pd.to_datetime(dates, format='%d/%m/%Y, %I:%M %p - ', dayfirst=True)
    except ValueError:
        try:
            dates = pd.to_datetime(dates, format='%d/%m/%y, %I:%M %p - ', dayfirst=True)
        except ValueError:
            dates = pd.to_datetime(dates, format='%d/%m/%Y, %H:%M - ', dayfirst=True)

    df = pd.DataFrame({'dates': dates, 'messages': messages})

    # getting users from messages : 
    users = []
    messages = [] 
    for i in df['messages'] : 
        if ':' in i :
            split = i.split(':')
            users.append(split[0])
            messages.append(''.join(split[1:]))
        else :  
            users.append('group_notification')
            messages.append(i)
    # inserting user column : 
    df.insert(1,'users' , users)    
    df['messages'] = messages

    # getting year , month , day , hour , minute from dates :
    df['year'] = df['dates'].dt.year
    df['month'] = df['dates'].dt.month_name()
    df['day'] = df['dates'].dt.day
    df['hour'] = df['dates'].dt.hour
    df['minute'] = df['dates'].dt.minute
    df['month_no'] = df['dates'].dt.month
    df['date_only'] = df['dates'].dt.date
    df['day_name'] = df['dates'].dt.day_name()

    period  = [] 
    for hour in df['hour'] : 
        if hour == 23 : 
            period.append(str(hour) + '-' + '00')
        elif hour == 0 : 
            period.append('00' + '-' + str(hour + 1) )
        else : 
            period.append(str(hour) + '-' + str(hour + 1 ))
            
    df['period'] = period

    return df


def furter_pp(df) : 
    temp = df[df['users'] != 'group_notification']
    temp = temp[temp['messages'] != ' <Media omitted>\n']  
    temp = temp[temp['messages'] != ' This message was deleted\n']
    return temp
