import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import preprocessor,helper
from wordcloud import WordCloud
from io import BytesIO
import seaborn as sns


st.sidebar.title('Whatsapp Chat Analyser')

uploaded_file = st.sidebar.file_uploader("Choose a file")
if uploaded_file is not None:
    # To read file as bytes:
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode('utf-8')

    df = preprocessor.preprocess(data)

    user_list = df['users'].unique().tolist()
    if 'group_notification' in user_list:
        user_list.remove('group_notification')
    user_list.sort()
    user_list.insert(0,'Overall')

    selected_user = st.sidebar.selectbox('Show Analysis wrt',user_list)


    if st.sidebar.button('Show Analysis'):

        num_messages,words,num_media_message,num_link = helper.fetch_stats(selected_user,df)

        st.title('Top Statistics')

        col1,col2,col3,col4 = st.columns(4)

        with col1:
            st.header('Total Messages')
            st.title(num_messages)

        with col2:
            st.header('Total Words')
            st.title(words)

        with col3:
            st.header('Total Media')
            st.title(num_media_message)

        with col4:
            st.header('Total Links')
            st.title(num_link)

        col1,col2 = st.columns(2)

        # montly timeline
        monthy_timeline = helper.monthly_timeline(selected_user,df)

        st.header('Monthly Timeline')
        fig,ax = plt.subplots()
        ax=plt.plot(monthy_timeline['time'],monthy_timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        # daily timeline
        daily_timeline = helper.daily_timeline(selected_user,df)

        st.header('Daily Timeline')
        fig,ax = plt.subplots()
        ax=plt.plot(daily_timeline['only_date'], daily_timeline['message'])
        plt.xticks(rotation='vertical')
        st.pyplot(fig)

        #day timeline

        day_timeline= helper.day_timeline(selected_user,df)
        active_month = helper.month_actitvity_map(selected_user,df)
        col1,col2 = st.columns(2)

        with col1:
            st.header('Most Active Day')
            fig, ax = plt.subplots()
            ax = plt.bar(day_timeline.index, day_timeline.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        with col2:
            st.header('Most Active Month')
            fig, ax = plt.subplots()
            ax = plt.bar(active_month.index, active_month.values)
            plt.xticks(rotation='vertical')
            st.pyplot(fig)

        hour_data = helper.hour_activity_map(selected_user,df)
        st.header('Hourly Activity')
        fig,ax=plt.subplots()
        ax = sns.heatmap(hour_data)
        st.pyplot(fig)


        if selected_user == "Overall":
            st.title('Most chatter')
            x,new_df= helper.most_text_user(df)
            col1,col2 = st.columns(2)

            with col1:
                fig,ax=plt.subplots()
                ax=plt.bar(x.index,x.values)
                #bar = px.bar(df,x=x.index,y=x.values,labels={'x' :'Names','y':'Num of chats'})
                st.pyplot(fig)

            with col2:
                fig,ax=plt.subplots()
                ax=plt.pie(new_df['percentage'],labels=new_df['name'],autopct='%0.1f%%')
                #st.plotly_chart(px.pie(new_df,values='percentage',names='name'))
                st.pyplot(fig)

        #WordCloud
        st.title('WordCloud')
        df_wc = helper.create_wordcloud(selected_user,df)
        #fig,ax = plt.subplots()
        #ax.imshow(df_wc)
        #st.pyplot(fig)


        wc = WordCloud(width=500, height=500, min_font_size=10, background_color='white')
        df_wc = wc.generate(df[df['message'] != '<Media omitted>\n']['message'].str.cat(sep=' '))
        fig, ax = plt.subplots()
        ax.imshow(df_wc)
        st.pyplot(fig)

        most_used = helper.most_common_words(selected_user,df)
        fig,ax = plt.subplots()
        ax.bar(most_used[0],most_used[1])
        plt.xticks(rotation='vertical')
        st.title('Most Common Words')
        st.pyplot(fig)

        emoji_df=helper.emoji_helper(selected_user,df)
        st.title("Emoji Analysis")

        col1,col2 = st.columns(2)

        with col1:
            st.dataframe(emoji_df)

        with col2:
            #fig,ax=plt.subplots()
            #ax.pie(emoji_df[1],labels=emoji_df[0])

            # fig = px.pie(values=emoji_df[1],names=emoji_df[0])
            # st.plotly_chart(fig)

            fig, ax = plt.subplots()
            ax = plt.pie(emoji_df[1], labels=emoji_df[0], autopct='%0.1f%%')
            st.pyplot(fig)



