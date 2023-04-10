import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics.pairwise import cosine_similarity

df=pd.read_csv('cleaned_anime.csv')

genres=['Psychological',
       'Supernatural', 'Demons', 'Dementia', 'Shoujo Ai', 'Ecchi', 'Sci-Fi',
       'Harem', 'Super Power', 'Space', 'Adventure', 'Yuri', 'Game', 'Cars',
       'School', 'Shounen Ai', 'Drama', 'Vampire', 'Yaoi', 'Samurai', 'Shoujo',
       'Action', 'Mystery', 'Sports', 'Hentai', 'Horror', 'Shounen',
       'Military', 'Fantasy', 'Josei', 'Historical', 'Magic', 'Slice of Life',
       'Romance', 'Martial Arts', 'Music', 'Kids', 'Thriller', 'Seinen',
       'Comedy', 'Police', 'Mecha', 'Parody', 'G', 'PG', 'PG-13', 'R', 'R+',
       'Rx']
genre_df=df[genres]

cos = cosine_similarity(genre_df)

def selected_anime(id):
    similar = sorted(list(enumerate(cos[id])),key=lambda x:x[1],reverse=True)[1:21]
    index = [x[0] for x in similar]
    return index

class SortBy:
       def __init__(self,index):
              self.index=index
              self.filter=df.loc[self.index]

       def relevance(self):
              df2=self.filter[['MAL_ID','Score-10','Score-9','Score-8','Score-7','Score-6','Score-5','Score-4','Score-3','Score-2','Score-1','Score']].set_index('MAL_ID')
              scaler = MinMaxScaler()
              scaler.fit(df2)
              max = scaler.data_max_
              normalize=scaler.transform(df2)
              score_df=pd.DataFrame(normalize, columns=list(df2.columns)).set_index(df2.index)
              cos = cosine_similarity(score_df)
              similar=sorted(list(enumerate(cos[0])),key=lambda x:x[1],reverse=True)[1:16]
              mal_ids = [id[0] for id in similar]
              mal_ids = score_df.reset_index().loc[mal_ids]['MAL_ID'].values
              return mal_ids

       def popularity(self):
              mal_ids=self.filter.sort_values(by=['Popularity'])['MAL_ID'].values
              return mal_ids
       
       def score(self):
              mal_ids=self.filter.sort_values(by=['Score'],ascending=False)['MAL_ID'].values
              return mal_ids
       
       def aired(self):
              mal_ids=self.filter.sort_values(by=['Aired'],ascending=False)['MAL_ID'].values
              return mal_ids