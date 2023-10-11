import pandas as pd
from urlextract import URLExtract
from wordcloud import WordCloud
from collections import Counter
import emoji
def fetch_stats(selected_user,df):
    # changing according to user
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    # total messages
    num_messages = df.shape[0]
    # total words
    words = []
    for message in df['message']:
        words.extend(message.split())
    # media count
    num_media_messages = df[df['message'] == '<Media omitted>\n'].shape[0]

    links = []
    extractor = URLExtract()
    for message in df['message']:
        links.extend(extractor.find_urls(message))



    return num_messages, len(words) , num_media_messages,len(links)


def most_text_user(df):
    x = df['users'].value_counts()

    df = (round(df['users'].value_counts()/df.shape[0],2)*100).reset_index().rename(columns={'index':'name','users':'percentage'})

    return x,df

def create_wordcloud(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

        #wc = WordCloud(width=500,height = 500,min_font_size=10,background_color='white')
        #df_wc = wc.generate(df['message'].str.cat(sep=' '))
    temp = df[df['users'] == 'group message']
    temp = df[df['message'] != '<Media omitted>\n']
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()
    def remove_stop_words(message):
        y=[]
        for word in message.lower().split():
            if word not in stop_words:
                y.append(word)
        return " ".join(y)
    temp = temp['message'].apply(remove_stop_words)

    return temp

def most_common_words(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    temp = df[df['users'] == 'group message']
    temp = df[df['message'] != '<Media omitted>\n']
    f = open('stop_hinglish.txt', 'r')
    stop_words = f.read()

    words = []
    for message in temp['message']:
        for word in message.lower().split():
            if word not in stop_words:
                words.append(word)

    most_common_df = pd.DataFrame(Counter(words).most_common(20))

    return most_common_df


def emoji_helper(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    emojis = []
    for message in df['message']:
        emojis.extend([c for c in message if c in emoji.EMOJI_DATA])

    emoji_df = pd.DataFrame(Counter(emojis).most_common(10))

    return emoji_df


def monthly_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]


    month_timeline = df.groupby(['year', 'month_num', 'month']).count()['message'].reset_index()

    time = []
    for i in range(month_timeline.shape[0]):
        time.append(month_timeline['month'][i] + '-' + str(month_timeline['year'][i]))

    month_timeline['time'] = time

    return month_timeline

def daily_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    daily_timeline = df.groupby(['only_date']).count()['message'].reset_index()

    return daily_timeline

def day_timeline(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    day_timeline=df.groupby(['day_name']).count()['message'].sort_values(ascending=False)

    return day_timeline

def month_actitvity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    return df['month'].value_counts()

def hour_activity_map(selected_user,df):
    if selected_user != 'Overall':
        df = df[df['users'] == selected_user]

    return df.pivot_table(index='day_name', columns='period', values='message', aggfunc='count').fillna(0)





