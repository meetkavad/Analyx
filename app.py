import streamlit as st 
import preprocessor , helper
import matplotlib.pyplot as plt
import seaborn as sns

st.sidebar.title("Analyx\n WhatsApp Chat Analyzer")

file = st.sidebar.file_uploader("choose a chat File" , type = ['txt'])
if file is not None : 
    bytes_data = file.getvalue()
    data = bytes_data.decode('utf-8')
    df = preprocessor.preprocessor(data)
    
    user_list = df['users'].unique().tolist()
    user_list.remove("group_notification")
    user_list.sort()
    user_list.insert(0 , "Overall")

    user = st.sidebar.selectbox("Select a user" , user_list)
    
    if st.sidebar.button("show Analysis") : 
        # show stats : 
        num_messages , num_words , num_media  , num_links = helper.fetch_stats(user , df) 

        col1 , col2 , col3 , col4 = st.columns(4)
        with col1 : 
            st.subheader("Total Messages")
            st.title(num_messages)
        with col2 : 
            st.subheader("Total Words")
            st.title(num_words) 
        with col3 : 
            st.subheader("Total Media messages")
            st.title(num_media)
        with col4 : 
            st.subheader("Total link messages")
            st.title(num_links)

        # show busiest users :
        if user == "Overall" : 
            st.subheader("Busiest Users")
            result , new_df = helper.fetch_busy_users(df)

            fig , ax = plt.subplots()

            col1 , col2 = st.columns(2)
            with col1 : 
                ax.bar(result.index , result.values)
                plt.xticks(rotation = 90)
                st.pyplot(fig)
            
            with col2 : 
                st.dataframe(new_df)    
    
        # further processing of data : 
        df = preprocessor.furter_pp(df)

        # show wordcloud :
                
        st.subheader("WordCloud")
        wordcloud = helper.create_wordcloud(user , df)
        fig , ax = plt.subplots()
        ax.imshow(wordcloud , interpolation = 'bilinear')
        ax.axis('off')
        st.pyplot(fig)
        
        # most common words : 
        
        most_common_word_df = helper.most_common_words(user , df)
        st.subheader("Most common words")
        fig , ax = plt.subplots()

        ax.barh(most_common_word_df[0] , most_common_word_df[1])
        plt.xticks(rotation = 90)

        st.pyplot(fig)  

        # monthy timeline : 
        st.subheader("Monthly Timeline")
        monthly_timeline_df = helper.monthly_timeline(user , df)
        fig , ax = plt.subplots()

        ax.plot(monthly_timeline_df['time'] , monthly_timeline_df['messages'] , color="green")
        plt.xticks(rotation = 90)
        st.pyplot(fig)

        # daily timeline : 
        st.subheader("Daily Timeline")
        daily_timeline_df = helper.daily_timeline(user , df)
        fig , ax = plt.subplots()

        ax.scatter(daily_timeline_df['date_only'] , daily_timeline_df['messages'] , color="red")
        plt.xticks(rotation = 90)
        st.pyplot(fig)

        # activity map : 

        col1 , col2 = st.columns(2)
        
        with col1 : 
            st.subheader("Weekly Activity Map")
            day_activity_map_series = helper.day_activity_map(user , df)
            fig , ax = plt.subplots()
            ax.bar(day_activity_map_series.index , day_activity_map_series.values , color="green")
            plt.xticks(rotation = 90)
            st.pyplot(fig)
        
        with col2 : 
            st.subheader("Monthly Activity Map")
            month_activity_map_series = helper.month_activity_map(user , df)
            fig , ax = plt.subplots()

            ax.bar(month_activity_map_series.index , month_activity_map_series.values , color="yellow")
            plt.xticks(rotation = 90)
            st.pyplot(fig)

        
        # activity heatmap : 
        st.subheader("User Chat Activity Heatmap ")
        activity_heatmap_df = helper.activity_heatmap(user , df)
        fig , ax = plt.subplots()
        ax = sns.heatmap(activity_heatmap_df)
        st.pyplot(fig)
