from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter 
import pandas as pd

extract = URLExtract()

sorted_days = ['Monday' , 'Tuesday' , 'Wednesday' , 'Thursday' , 'Friday' , 'Saturday' , 'Sunday']
sorted_months = ['January' , 'February' , 'March' , 'April' , 'May' , 'June' , 'July' , 'August' , 'September' ,'October' , 'November' , 'December']    

# fetching general 4 statistics : 
def fetch_stats(user , df) : 

    if user != 'Overall' :  # particular user : 

        # total number of messages : 
        user_df = df[df['users'] == user]   
        num_messages = user_df.shape[0]

        # total number of words :
        words = []
        for i in user_df['messages'] : 
            words.extend(i.split())

        # total number of media messages :
        num_media_messages = user_df[user_df['messages'] == ' <Media omitted>\n'].shape[0]  

        # total number of links shared :
        links = []
        for link in user_df['messages'] : 
            links.extend(extract.find_urls(link))

        return num_messages , len(words) , num_media_messages , len(links)
    
    # overall stats :
    # total messages shared : 
    num_messages =  df.shape[0]

    # total number of words :
    words = [] 
    for i in df['messages'] : 
        words.extend(i.split())

    # total number of links shared :
    links = [] 
    for link in df['messages'] : 
            links.extend(extract.find_urls(link))
    
    # toal number of media messages :
    num_media_messages = df[df['messages'] == ' <Media omitted>\n'].shape[0]

    return num_messages , len(words) , num_media_messages , len(links)

# fetching busiest users :

def fetch_busy_users(df) : 
    # message per user 
    message_per_user = df['users'].value_counts()

    # percentage chat per user : 
    user_chat_percent_df = round((message_per_user/df.shape[0])*100 , 2).reset_index().rename(
         columns = {'users': 'name' ,'count' : 'percent'})
    
    return message_per_user.head() , user_chat_percent_df



# get meaningful chat words : 
def meaningful_chat_words(df) :

    f = open('../stop_hinglish.txt' , 'r' , encoding= 'utf-8')
    stop_words = f.read()

    words = [] 
    for message in df['messages'] : 
        for word in message.lower().split() : 
            if word not in stop_words and not word.startswith('@'):
                words.append(word)
    return words

# creating wordcloud :

def create_wordcloud(user , df) : 
    

    if user != "Overall" : 
        df = df[df['users'] == user]
    
    words = meaningful_chat_words(df)

    wc = WordCloud(width = 500 , height = 300 , max_words = 100 , background_color = "white").generate(' '.join(words))
    return wc

# getting most common words :   

def most_common_words(user , df) :

    if user != "Overall" : 
        df = df[df['users'] == user]
    
    words = meaningful_chat_words(df)

    most_common = Counter(words).most_common(20)
    most_common_df = pd.DataFrame(most_common)
    return most_common_df

# monthly timeline : 

def monthly_timeline(user , df) :
    if user!= 'Overall' : 
        df = df[df['users'] == user]    
    
    
    monthly_timeline_df = df.groupby(['year' ,'month_no' ,  'month'])['messages'].count().reset_index()
    months = []  # contains each month in format : "december 2023" 
    for i in range(monthly_timeline_df.shape[0]) : 
        months.append(monthly_timeline_df['month'][i] + ' ' + str(monthly_timeline_df['year'][i]))
    
    
    monthly_timeline_df['time'] = months
    return monthly_timeline_df

# daily timeline : 

def daily_timeline(user , df) :
    if user!= 'Overall' : 
        df = df[df['users'] == user]    
    
    daily_timeline_df = df.groupby(['date_only'])['messages'].count().reset_index()
    return daily_timeline_df

# days activity map : 
def day_activity_map(user , df) : 
    if user!= 'Overall' : 
        df = df[df['users'] == user]
    
    x = df['day_name'].value_counts()
    x = x.reindex(sorted_days)
    return x 

# month activity map :
def month_activity_map(user , df) : 
    if user!= 'Overall' : 
        df = df[df['users'] == user]
    
    x =  df['month'].value_counts()
    x = x.reindex(sorted_months)
    return x

# activity heatmap : 

def activity_heatmap(user , df) : 
    if user!= 'Overall' : 
        df = df[df['users'] == user]
    
    x = df.pivot_table(index = "day_name" , columns = "period" , values = "messages" , aggfunc = "count").fillna(0)
    return x

