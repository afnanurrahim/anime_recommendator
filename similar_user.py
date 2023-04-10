import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

df= pd.read_csv('filtered_rating.csv')
df=df.drop(columns=['Unnamed: 0'],axis=1)

def user_anime(anime_score):          # anime_score -> dictionary
    df_table=pd.DataFrame(columns=['MAL_ID','user_id','rating'])
    for i in list(anime_score.keys()):
        t=df[df['MAL_ID']==i]
        df_table= pd.concat([df_table,t])

    df1=df_table.pivot_table(index='user_id',columns='MAL_ID',values='rating')
    data=[]
    data.insert(0, anime_score)
    pd.concat([pd.DataFrame(data), df1], ignore_index=True) 
    df2 = pd.concat([pd.DataFrame(data), df1], ignore_index=True)
    cos= cosine_similarity(df2.fillna(0))
    most_similar_user = sorted(list(enumerate(cos[0])),key=lambda x:x[1],reverse=True)[1][0] -1

    user_id=df1.reset_index().loc[most_similar_user]['user_id']
    user_list=df[df['user_id']==user_id].sort_values(by=['rating'],ascending=False)
    user_list=list(user_list['MAL_ID'].values)
    for i in list(anime_score.keys()):
        user_list.remove(i)

    return user_list[:20]