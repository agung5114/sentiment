import streamlit as st
import pandas as pd
import numpy as np
import plotly_express as px
import networkx as nx
# from wordcloud import WordCloud
import json

import plotly.io as pio
# pio.templates.default = "ggplot2"
# pio.templates.default = "plotly_white"
pio.templates.default = "simple_white"
# pio.templates.default = "seaborn"
# pio.templates.default = "none"
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm, rcParams
# import nx_altair as nxa

plt.rcParams['font.sans-serif']=['SimHei'] #Show Chinese label
plt.rcParams['axes.unicode_minus']=False   #These two lines need to be set manually
plt.rc('axes', unicode_minus=False)

st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_page_config(layout="wide")

st.title('Sentiment Analysis')

df = pd.read_excel('stdata.xlsx')
df['count']=1
choice = df['keyword'].unique().tolist()
key = st.selectbox('Pilih Keyword',choice)

if key == None or key ==[]:
    df0 = df
else:
    df0 = df[df['keyword'].isin([key])]

a1,a2 = st.beta_columns((1,1))
with a1:
    df1a = df0.groupby(by=['label'],as_index=False).sum('count')
    fig1 = px.pie(df1a,color='label',values='count',hole=0.4)
    fig1.update_layout(clickmode="event+select")
    st.plotly_chart(fig1)
with a2:
    # df1b = df0[['tweet_punct']]
    # cek = df1b['tweet_punct'].str.lower()
    # sw = choice +['di','yg','yang','dan','ini','itu','ya','sama','sudah','lebih']
    # sw = sw +['kena','untuk','sri','mulyani','dengan','dari','ke','atau','tidak']
    # sw = sw +['buat','ada','aja','jadi','juga','ga','tapi','gak','apa','lagi','masih']
    # sw = sw +['pada','terus','akan','kalo','utk','terus','trs','nya','sih','kita']
    # # st.write(df00.head(10))
    # wordcloud = WordCloud (
    #                 background_color = 'white',
    #                 width = 800,
    #                 stopwords =sw,
    #                 height = 450
    #                     ).generate(' '.join(cek))
    # fig2 = px.imshow(wordcloud,title=f'Wordcloud Twitter')
    # st.plotly_chart(fig2)
    st.write(df0.head(10))

df2 = df0[['label','user.name','Value','tweet_punct','count','user.followers_count']]
senti = st.selectbox('Pilih Sentiment',['All','Positif','Negatif'])
df3 = df2[df2['label'].isin(['positif','negatif'])]
dff = df3.groupby(by=['label','user.name','Value'],as_index=False).sum('count').dropna()
# dfa = dff.nlargest(1000,'count').sort_values(by='count',ascending=False)
dfa = dff
dfp = dfa[dfa['label'].isin(['positif'])]
dfn = dfa[dfa['label'].isin(['negatif'])]
if senti == 'All':
    df4 = dff
    G = nx.from_pandas_edgelist(dfa, source='user.name', target='Value',create_using=nx.DiGraph)
    # st.write(G.nodes)
    # st.write(nodelist.tail())
    # sizelist = pd.merge(left= nodelist,right=dfa[['user.name','user.followers_count']],how='inner',on='user.name')
    # sizelist['follower']= sizelist['user.followers_count'].fillna(0)                    
    # st.write(sizelist[-5:-1])
    # nodesizelist = sizelist['follower'].tolist()
    # st.write(sizelist.tail())
    
    nodelist = pd.DataFrame({'user.name':G.nodes})
    sizelist = pd.merge(left= nodelist,right=df0[['user.name','user.followers_count']],how='inner',on='user.name')
    sizelist['user.followers_count'] = sizelist['user.followers_count'].fillna(0)

    Allcolors = []
    for node in G:
        if node in dfp["user.name"].values or node in dfp["Value"].values:
            Allcolors.append("teal")
        else: Allcolors.append("orange")
    
    Allsize = []
    for node in G:
        if node in dfa["user.name"].values:
            dfpp = dfa[dfa["user.name"].isin([node])]
            size = dfpp["user.followers_count"].tolist()
            if size[0] >= 50000:
                size[0] = 50000
            Allsize.append(size[0])
        else: Allsize.append(100)

    plt.figure(figsize=(15,10))
    # nx.draw(G, node_color=colors)
    fig6 = st.pyplot(fig=nx.draw(G, node_color=Allcolors,edge_color='y',node_size=Allsize,\
                        font_size=10, font_weight='light', with_labels=True))
    # fig7 = px.imshow(nx.draw(G, node_color=Allcolors,edge_color='y',\node_size=nodesizelist
    #                     font_size=10, font_weight='light', with_labels=True),title=f'Wordcloud Twitter')
    # st.plotly_chart(fig7)
elif senti == 'Positif':
    df4 = dff[dff['label'].isin(['positif'])]
    P = nx.from_pandas_edgelist(dfp, source='user.name', target='Value',create_using=nx.DiGraph)
    colors = []
    for node in P:
        if node in dfp["user.name"].values:
            colors.append("blue")
        else: colors.append("blue")

    plt.figure(figsize=(15,10))
    # nx.draw(G, node_color=colors)
    fig6 = st.pyplot(fig=nx.draw(P, node_color=colors,edge_color='y',\
                        font_size=10, font_weight='light', with_labels=True))
else:
    df4 = dff[dff['label'].isin(['negatif'])]
    N = nx.from_pandas_edgelist(dfn, source='user.name', target='Value',create_using=nx.DiGraph)
    colors = []
    for node in N:
        if node in dfn["user.name"].values:
            colors.append("red")
        else: colors.append("red")

    plt.figure(figsize=(15,10))
    # nx.draw(G, node_color=colors)
    fig6 = st.pyplot(fig=nx.draw(N, node_color=colors,edge_color='b',\
                        font_size=10, font_weight='light', with_labels=True))

t1, t2 = st.beta_columns((1,1))
with t1:
    df5 = df4.groupby(by=['user.name'],as_index=False).sum('count').dropna()
    # df5 = df5.nlargest(20,'count').sort_values(by='count',ascending=False)
    fig5 = px.treemap(df5,path=['user.name'],values='count',color='count')
    fig5.update_layout(title_text='Most tweet',coloraxis_showscale=False)
    st.plotly_chart(fig5)
with t2:
    df3b = df4.groupby(by=['Value'],as_index=False).sum('count').dropna()
    # df3b = df3b.nlargest(20,'count').sort_values(by='count',ascending=False)
    fig4 = px.treemap(df3b,path=['Value'],values='count',color='count')
    fig4.update_layout(title_text='Most tagged',coloraxis_showscale=False)
    st.plotly_chart(fig4)



# n1, n2 = st.beta_columns((1,1))
# df2 = df2.head(100)
# with n1:
#     dfp = df2[df2['label'].isin(['positif'])]
#     P = nx.from_pandas_edgelist(dfp, source='user.name', target='Value',create_using=nx.DiGraph)
#     colors = []
#     for node in P:
#         if node in dfp["user.name"].values:
#             colors.append("blue")
#         else: colors.append("blue")

#     plt.figure(figsize=(15,10))
#     # nx.draw(G, node_color=colors)
#     fig5 = st.pyplot(fig=nx.draw(P, node_color=colors,edge_color='y',\
#                         font_size=10, font_weight='light', with_labels=True))
# with n2:
#     dfn = df2[df2['label'].isin(['negatif'])]
#     N = nx.from_pandas_edgelist(dfn, source='user.name', target='Value',create_using=nx.DiGraph)
#     colors = []
#     for node in N:
#         if node in dfn["user.name"].values:
#             colors.append("red")
#         else: colors.append("red")

#     plt.figure(figsize=(15,10))
#     # nx.draw(G, node_color=colors)
#     fig6 = st.pyplot(fig=nx.draw(N, node_color=colors,edge_color='b',\
#                         font_size=10, font_weight='light', with_labels=True))
    # pos = nx.nx_pydot.graphviz_layout(G), \
    #     node_size=1200,linewidths=0.25, \
    #     font_size=10, font_weight='bold', with_labels=True


# dfal = df2
# dfal['label']=dfal['label'].replace({'positif':2,'negatif':1,'tdk-relevan':0,'netral':0})
# G = nx.from_pandas_edgelist(dfal, source='user.name', target='Value',create_using=nx.DiGraph)
# pos = nx.spring_layout(G)
# z = dfal['label']
# w = list(G.nodes())
# # print(z[0])
# for i in range(len(w)-1):
#     n = w[i]
#     G.nodes[n]['weight'] = z[i]

# for e in G.edges():
#     G.edges[e]['weight'] = np.random.uniform(1, 10)


# # Draw the graph using Altair
# viz = nxa.draw_networkx(
#     G, pos=pos,
#     node_color='weight',
#     cmap='viridis',
#     width='weight',
#     edge_color='black')

# st.write(viz.interactive())