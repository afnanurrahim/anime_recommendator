import streamlit as st
from streamlit_extras.no_default_selectbox import selectbox
import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import similar_anime
import similar_user

header={
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36 FKUA/website/42/website/Desktop"
}

st.title('Anime Recommendator')

tab1, tab2 = st.tabs(["Similar anime", "Suggested for you"])

image_dict={}       # for getting image url 

df= pd.read_csv('cleaned_anime.csv')

with tab1:

    option = selectbox("Select anime",df.Name,no_selection_label="-")

    score=None
    if option:
        selected_df=df[df.Name==option]
        score=selected_df['Score'].values[0]
        st.write('Anime Score:', score)

        mal_index= similar_anime.selected_anime(selected_df.index[0])
        sort_by=similar_anime.SortBy(mal_index)
        sort_dict={'Relevance':sort_by.relevance(),'Popularity':sort_by.popularity(),'Score':sort_by.score(),'Aired':sort_by.aired()}

        sort_radio= st.radio("Sort by: ", tuple(sort_dict.keys()))
        mal_ids=sort_dict[sort_radio]

        for i in mal_ids:
            img_col, content_col= st.columns(2)
            content_df=df[df['MAL_ID']==i]
            with img_col:
                st.subheader(content_df['Name'].values[0])
                if image_dict.get(i):
                    img=image_dict.get(i)
                else:
                    URL = f"https://myanimelist.net/anime/{i}"
                    r = requests.get(URL,headers=header)
                    soup = BeautifulSoup(r.content,"html.parser")
                    img=soup.find_all('img')[2]['data-src']
                    image_dict[i]=img

                img_col.image(img)

            with content_col:
                score_col, type_col, episodes_col, aired_col = st.columns([1,1,1.5,1],gap='medium')
                with score_col:
                    st.subheader('Score')
                    st.text(content_df['Score'].values[0])
                with type_col:
                    st.subheader('Type')
                    st.text(content_df['Type'].values[0])
                with episodes_col:
                    st.subheader('Episodes')
                    st.text(content_df['Episodes'].values[0])
                with aired_col:
                    st.subheader('Aired')
                    st.text(content_df['Aired'].values[0])
                
                st.subheader('Synopsis')
                st.write(content_df['synopsis'].values[0])
            
            st.text('\n')
            st.text('\n')

with tab2:
    score={}
    options = st.multiselect(
        'Select you favourite animes',
        df.Name)

    if options:
        for op in options:
            selected_df=df[df.Name==op]
            id=selected_df['MAL_ID'].values[0]
            score[id]=10

        if st.button('Suggest'):
            print(score)
            arr=similar_user.user_anime(score)
            arr= np.array(arr)
            arr.shape=(4,5)


            for i in arr:
                col=st.columns(4)

                for c,j in zip(col,i):
                    with c:
                        if image_dict.get(j):
                            img=image_dict.get(j)
                        else:
                            URL = f"https://myanimelist.net/anime/{j}"
                            r = requests.get(URL,headers=header)
                            soup = BeautifulSoup(r.content,"html.parser")
                            img=soup.find_all('img')[2]['data-src']
                            image_dict[j]=img
                        c.image(img)
                        title= df[df['MAL_ID']==j]['Name'].values[0]
                        st.write(f"{title} [link]({URL})")
