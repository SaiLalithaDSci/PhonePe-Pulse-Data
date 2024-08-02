import streamlit as st
from streamlit_option_menu import option_menu
import psycopg2
import pandas as pd
import plotly
import plotly.express as px
import requests
import json


#Data Frame Creation
#SQL Connection
my_db=psycopg2.connect(host='localhost',
                        user='postgres',
                        password='password',
                        database='PhonePe_Data',
                        port='5432')
cursor=my_db.cursor()

#aggregated_insurance_df
cursor.execute("select * from aggregated_insurance")
my_db.commit()
T1=cursor.fetchall()

Aggregated_Insurance=pd.DataFrame(T1,columns=("States","Years","Quarter","Transaction_Type","Transaction_Count","Transaction_Amount"))

#aggregated_transaction_df
cursor.execute("select * from aggregated_transaction")
my_db.commit()
T2=cursor.fetchall()

Aggregated_Transaction=pd.DataFrame(T2,columns=("States","Years","Quarter","Transaction_Type","Transaction_Count","Transaction_Amount"))

#aggregated_user_df
cursor.execute("select * from aggregated_user")
my_db.commit()
T3=cursor.fetchall()

Aggregated_User=pd.DataFrame(T3,columns=("States","Years","Quarter","Brand_Name","User_Count","User_Percentage"))

#map_insurance_df
cursor.execute("select * from map_insurance")
my_db.commit()
T4=cursor.fetchall()

Map_Insurance=pd.DataFrame(T4,columns=("States","Years","Quarter","Districts","User_Count","Transaction_Amount"))

#map_transaction_df
cursor.execute("select * from map_transaction")
my_db.commit()
T5=cursor.fetchall()

Map_Transaction=pd.DataFrame(T5,columns=("States","Years","Quarter","Districts","User_Count","Transaction_Amount"))

#map_user_df
cursor.execute("select * from map_user")
my_db.commit()
T6=cursor.fetchall()

Map_User=pd.DataFrame(T6,columns=("States","Years","Quarter","Districts","User_Count","App_Opens"))

#top_insurance_df
cursor.execute("select * from top_insurance")
my_db.commit()
T7=cursor.fetchall()

Top_Insurance=pd.DataFrame(T7,columns=("States","Years","Quarter","Pincodes","User_Count","Transaction_Amount"))

#top_transaction_df
cursor.execute("select * from top_transaction")
my_db.commit()
T8=cursor.fetchall()

Top_Transaction=pd.DataFrame(T8,columns=("States","Years","Quarter","Pincodes","User_Count","Transaction_Amount"))

#top_user_df
cursor.execute("select * from top_user")
my_db.commit()
T9=cursor.fetchall()

Top_User=pd.DataFrame(T9,columns=("States","Years","Quarter","Pincodes","Pincode_Wise_Registered_Users"))

#plotting functions
def Transaction_Amount_Count_Y(df, year):
    TranAmtCnt=df[df["Years"]==year]
    TranAmtCnt['Years'].unique()
    TranAmtCnt.reset_index(drop=True, inplace=True)


    TranAmtCntG=TranAmtCnt.groupby("States")[["Transaction_Count","Transaction_Amount"]].sum()
    TranAmtCntG.reset_index(inplace=True)
    
    col1,col2=st.columns(2)
    with col1:
        fig_amt=px.bar(TranAmtCntG, x="States", y="Transaction_Amount", title=f"{year} TRANSACTION AMOUNT", color_discrete_sequence=px.colors.sequential.Peach_r)
        st.plotly_chart(fig_amt)
    with col2:
        fig_cnt=px.bar(TranAmtCntG, x="States", y="Transaction_Count", title=f"{year} TRANSACTION COUNT", color_discrete_sequence=px.colors.sequential.Peach_r)
        st.plotly_chart(fig_cnt)

    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response=requests.get(url)
    data1=json.loads(response.content)
    state_name=[]
    for feature in data1['features']:
        state_name.append(feature['properties']['ST_NM'])

    state_name.sort()

    with col1:
        fig_india_1=px.choropleth(TranAmtCntG, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                color="Transaction_Amount", color_continuous_scale="Rainbow",
                                range_color=(TranAmtCntG["Transaction_Amount"].min(),TranAmtCntG["Transaction_Amount"].max()),
                                hover_name="States", title=f"{year} TRANSACTION AMOUNT", fitbounds="locations")
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)
    with col2:
        fig_india_2=px.choropleth(TranAmtCntG, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                color="Transaction_Count", color_continuous_scale="Rainbow",
                                range_color=(TranAmtCntG["Transaction_Count"].min(),TranAmtCntG["Transaction_Count"].max()),
                                hover_name="States", title=f"{year} TRANSACTION COUNT", fitbounds="locations")
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)

    return TranAmtCnt

def Transaction_Amount_Count_Q(df,quarter):
    TranAmtCnt=df[df["Quarter"]==quarter]
    TranAmtCnt['Quarter'].unique()
    TranAmtCnt.reset_index(drop=True, inplace=True)


    TranAmtCntG=TranAmtCnt.groupby("States")[["Transaction_Count","Transaction_Amount"]].sum()
    TranAmtCntG.reset_index(inplace=True)

    col1,col2=st.columns(2)
    
    with col1:
        fig_amt=px.bar(TranAmtCntG, x="States", y="Transaction_Amount", title=f"{TranAmtCnt['Years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT", color_discrete_sequence=px.colors.sequential.Peach_r)
        st.plotly_chart(fig_amt)

    with col2:
        fig_cnt=px.bar(TranAmtCntG, x="States", y="Transaction_Count", title=f"{TranAmtCnt['Years'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT", color_discrete_sequence=px.colors.sequential.Peach_r)
        st.plotly_chart(fig_cnt)

    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response=requests.get(url)
    data1=json.loads(response.content)
    state_name=[]
    for feature in data1['features']:
        state_name.append(feature['properties']['ST_NM'])

    state_name.sort()

    with col1:
        fig_india_1=px.choropleth(TranAmtCntG, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                color="Transaction_Amount", color_continuous_scale="Rainbow",
                                range_color=(TranAmtCntG["Transaction_Amount"].min(),TranAmtCntG["Transaction_Amount"].max()),
                                hover_name="States", title=f"{TranAmtCnt['Years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT", fitbounds="locations")
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)

    with col2:
        fig_india_2=px.choropleth(TranAmtCntG, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                color="Transaction_Count", color_continuous_scale="Rainbow",
                                range_color=(TranAmtCntG["Transaction_Count"].min(),TranAmtCntG["Transaction_Count"].max()),
                                hover_name="States", title=f"{TranAmtCnt['Years'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT", fitbounds="locations")
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)

def Transaction_Amount_Count_PT(df,TranType,year):
    trantype=df[df["Transaction_Type"]==TranType]
    trantype['Transaction_Type'].unique()
    trantype.reset_index(drop=True, inplace=True)

    trantypeG=trantype.groupby("States")[["Transaction_Count","Transaction_Amount"]].sum()
    trantypeG.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_amt=px.bar(trantypeG, x="States", y="Transaction_Amount", title=f"{year} YEAR {trantypeList.upper()} TRANSACTION AMOUNT", color_discrete_sequence=px.colors.sequential.Peach_r)
        st.plotly_chart(fig_amt)
    with col2:
        fig_cnt=px.bar(trantypeG, x="States", y="Transaction_Count", title=f"{year} YEAR {trantypeList.upper()} TRANSACTION COUNT", color_discrete_sequence=px.colors.sequential.Peach_r)
        st.plotly_chart(fig_cnt)

    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response=requests.get(url)
    data1=json.loads(response.content)
    state_name=[]
    for feature in data1['features']:
        state_name.append(feature['properties']['ST_NM'])

    state_name.sort()

    with col1:
        fig_india_1=px.choropleth(trantypeG, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                    color="Transaction_Amount", color_continuous_scale="Rainbow",
                                    range_color=(trantypeG["Transaction_Amount"].min(),trantypeG["Transaction_Amount"].max()),
                                    hover_name="States", title=f"{year} YEAR {trantypeList.upper()} TRANSACTION AMOUNT", fitbounds="locations")
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)

    with col2:
        fig_india_2=px.choropleth(trantypeG, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                color="Transaction_Count", color_continuous_scale="Rainbow",
                                range_color=(trantypeG["Transaction_Count"].min(),trantypeG["Transaction_Count"].max()),
                                hover_name="States", title=f"{year} YEAR {trantypeList.upper()} TRANSACTION COUNT", fitbounds="locations")
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)

def TranType_ST(df,state,year):
    trantype=df[df["States"]==state]
    trantype.reset_index(drop=True, inplace=True)

    trantypeG=trantype.groupby("Transaction_Type")[["Transaction_Count","Transaction_Amount"]].sum()
    trantypeG.reset_index(inplace=True)
    
    col1,col2=st.columns(2)
    with col1:
        fig_pie_1=px.pie(data_frame=trantypeG,names="Transaction_Type",values="Transaction_Amount",
                        title=f"{year} YEAR {state.upper()} TRANSACTION AMOUNT",hole=0.4,color_discrete_sequence=px.colors.sequential.Rainbow_r)

        st.plotly_chart(fig_pie_1)
    with col2:
        fig_pie_2=px.pie(data_frame=trantypeG,names="Transaction_Type",values="Transaction_Count",
                        title=f"{year} YEAR {state.upper()} TRANSACTION COUNT",hole=0.4,color_discrete_sequence=px.colors.sequential.Rainbow_r)

        st.plotly_chart(fig_pie_2)

    return trantype

def TranType_QT(df,year,quarter):
    trantype=df[df["Quarter"]==quarter]
    trantype.reset_index(drop=True, inplace=True)

    trantypeG=trantype.groupby("Transaction_Type")[["Transaction_Count","Transaction_Amount"]].sum()
    trantypeG.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        fig_pie_1=px.pie(data_frame=trantypeG,names="Transaction_Type",values="Transaction_Amount",
                        title=f"{year} YEAR {quarter} QUARTER {trantypeList.upper()} TRANSACTION AMOUNT",hole=0.4,color_discrete_sequence=px.colors.sequential.Rainbow_r)

        st.plotly_chart(fig_pie_1)
    with col2:
        fig_pie_2=px.pie(data_frame=trantypeG,names="Transaction_Type",values="Transaction_Count",
                        title=f"{year} YEAR {quarter} QUARTER {trantypeList.upper()} TRANSACTION COUNT",hole=0.4,color_discrete_sequence=px.colors.sequential.Rainbow_r)

        st.plotly_chart(fig_pie_2)

#Aggregated_User
def AggUser_Brand_Y(df,year):
    AU_Y_B_Cnt=df[df['Years']==year]
    AU_Y_B_Cnt.reset_index(drop=True,inplace=True)

    AU_Y_B_Cnt_G=AU_Y_B_Cnt.groupby('Brand_Name')[['User_Count']].sum()
    AU_Y_B_Cnt_G.reset_index(inplace=True)

    fig1=px.bar(data_frame=AU_Y_B_Cnt_G,x='Brand_Name',y='User_Count',color_discrete_sequence=px.colors.sequential.Rainbow_r,
                title=f"{year} BRAND WISE USER COUNT")
    st.plotly_chart(fig1)

    return AU_Y_B_Cnt

def AggUser_Brand_Q(df,quarter):
    AU_Y_B_Cnt_Q=df[df['Quarter']==quarter]
    AU_Y_B_Cnt_Q.reset_index(drop=True,inplace=True)

    AU_Y_B_Cnt_Q_G=AU_Y_B_Cnt_Q.groupby('Brand_Name')[['User_Count']].sum()
    AU_Y_B_Cnt_Q_G.reset_index(inplace=True)

    fig1=px.bar(data_frame=AU_Y_B_Cnt_Q_G,x='Brand_Name',y='User_Count',color_discrete_sequence=px.colors.sequential.Rainbow_r,
                title=f"{quarter} QUARTER BRAND WISE USER COUNT")
    st.plotly_chart(fig1)

def AggUser_Brand_ST(df,state):
    AU_Brand_Count=df[df['States']==state]
    AU_Brand_Count.reset_index(drop=True,inplace=True)

    AU_Brand_Count_G=AU_Brand_Count.groupby('Brand_Name')[['User_Count']].sum()
    AU_Brand_Count_G.reset_index(inplace=True)

    fig1=px.bar(data_frame=AU_Brand_Count_G,x='Brand_Name',y='User_Count',color_discrete_sequence=px.colors.sequential.Rainbow_r,
                title=f"{state.upper()} BRAND WISE USER COUNT")
    st.plotly_chart(fig1)

# MAP ANALYSIS
# MAP INSURANCE
def Map_User_Tran_Y(df,year):
    map1=df[df['Years']==year]
    map1.reset_index(drop=True,inplace=True)
    map1G=map1.groupby('States')[['User_Count','Transaction_Amount']].sum()
    map1G.reset_index(inplace=True)
    
    col1,col2=st.columns(2)
    with col1:
        Mfig1=px.bar(data_frame=map1G, x='States',y='User_Count',title=f"{year} STATE WISE USER COUNT",color_discrete_sequence=px.colors.sequential.Rainbow_r)
        st.plotly_chart(Mfig1)
    with col2:
        Mfig2=px.bar(data_frame=map1G, x='States',y='Transaction_Amount',title=f"{year} STATE WISE TRANSACTION AMOUNT",color_discrete_sequence=px.colors.sequential.Rainbow_r)
        st.plotly_chart(Mfig2)

    return map1

def Map_User_Tran_Q(df,quarter):
    map2=df[df['Quarter']==quarter]
    map2.reset_index(drop=True,inplace=True)
    map2G=map2.groupby('States')[['User_Count','Transaction_Amount']].sum()
    map2G.reset_index(inplace=True)
    
    col1,col2=st.columns(2)
    with col1:
        Mfig1=px.bar(data_frame=map2G, x='States',y='User_Count',title=f"QUARTER - {quarter} STATE WISE USER COUNT",color_discrete_sequence=px.colors.sequential.Rainbow_r)
        st.plotly_chart(Mfig1)
    with col2:
        Mfig2=px.bar(data_frame=map2G, x='States',y='Transaction_Amount',title=f"QUARTER - {quarter} STATE WISE TRANSACTION AMOUNT",color_discrete_sequence=px.colors.sequential.Rainbow_r)
        st.plotly_chart(Mfig2)

    return map2

def Map_User_Tran_DisY(df,state):
    map5=df[df['States']==state]
    map5.reset_index(drop=True,inplace=True)

    map5G=map5.groupby('Districts')[['User_Count','Transaction_Amount']].sum()
    map5G.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        Mfig1=px.bar(data_frame=map5G, x='Districts',y='User_Count',title=f"{state.upper()} DISTRICT WISE USER COUNT FOR ABOVE YEAR",color_discrete_sequence=px.colors.sequential.Rainbow_r)
        st.plotly_chart(Mfig1)
    with col2:
        Mfig2=px.bar(data_frame=map5G, x='Districts',y='Transaction_Amount',title=f"{state.upper()} DISTRICT WISE TRANSACTION AMOUNT FOR ABOVE YEAR",color_discrete_sequence=px.colors.sequential.Rainbow_r)
        st.plotly_chart(Mfig2)

def Map_User_Tran_DisQ(df,state):

    map6=df[df['States']==state]
    map6.reset_index(drop=True,inplace=True)

    map6G=map6.groupby('Districts')[['User_Count','Transaction_Amount']].sum()
    map6G.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        Mfig1=px.bar(data_frame=map6G, x='Districts',y='User_Count',title=f"{state.upper()} DISTRICT WISE USER COUNT FOR ABOVE QUARTER",color_discrete_sequence=px.colors.sequential.Rainbow_r)
        st.plotly_chart(Mfig1)
    with col2:
        Mfig2=px.bar(data_frame=map6G, x='Districts',y='Transaction_Amount',title=f"{state.upper()} DISTRICT WISE TRANSACTION AMOUNT FOR ABOVE QUARTER",color_discrete_sequence=px.colors.sequential.Rainbow_r)
        st.plotly_chart(Mfig2)

#Map User
def Map_User_UC_AO_Y(df,year):

    map1=df[df['Years']==year]
    map1.reset_index(drop=True,inplace=True)

    map1G=map1.groupby('States')[['User_Count','App_Opens']].sum()
    map1G.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        Mfig1=px.bar(data_frame= map1G, x="States", y="User_Count",
                    title=f"{year} STATE WISE USER COUNT", color_discrete_sequence=px.colors.sequential.Rainbow_r)
        st.plotly_chart(Mfig1)
    with col2:
        Mfig2=px.bar(data_frame= map1G, x="States", y="App_Opens",
                    title=F"{year} STATE WISE APP OPENS COUNT", color_discrete_sequence=px.colors.sequential.Rainbow_r)
        st.plotly_chart(Mfig2)

    return map1

def Map_User_UC_AO_Q(df,quarter):

    map2=df[df['Quarter']==quarter]
    map2.reset_index(drop=True,inplace=True)

    map2G=map2.groupby('States')[['User_Count','App_Opens']].sum()
    map2G.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        Mfig1=px.bar(data_frame=map2G, x="States", y="User_Count",
                    title="QUARTER STATE WISE USER COUNT", color_discrete_sequence=px.colors.sequential.Rainbow_r)
        st.plotly_chart(Mfig1)
    with col2:
        Mfig2=px.bar(data_frame=map2G, x="States", y="App_Opens",
                    title="QUARTER STATE WISE APP OPENS COUNT", color_discrete_sequence=px.colors.sequential.Rainbow_r)
        st.plotly_chart(Mfig2)

    return map2

def Map_User_UC_AO_DY(df,state):

    map3=df[df['States']==state]
    map3.reset_index(drop=True,inplace=True)

    map3G=map3.groupby('Districts')[['User_Count','App_Opens']].sum()
    map3G.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        Mfig1=px.bar(data_frame=map3G, x="Districts", y="User_Count",
                    title="DISTRICT WISE USER COUNT", color_discrete_sequence=px.colors.sequential.Rainbow_r)
        st.plotly_chart(Mfig1)
    with col2:
        Mfig2=px.bar(data_frame=map3G, x="Districts", y="App_Opens",
                    title="DISTRICT WISE APP OPENS COUNT", color_discrete_sequence=px.colors.sequential.Rainbow_r)
        st.plotly_chart(Mfig2)

def Map_User_UC_AO_DQ(df,state):

    map4=df[df['States']==state]
    map4.reset_index(drop=True,inplace=True)

    map4G=map4.groupby('Districts')[['User_Count','App_Opens']].sum()
    map4G.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        Mfig1=px.bar(data_frame=map4G, x="Districts", y="User_Count",
                    title="QUARTER DISTRICT WISE USER COUNT", color_discrete_sequence=px.colors.sequential.Rainbow_r)
        st.plotly_chart(Mfig1)
    with col2:
        Mfig2=px.bar(data_frame=map4G, x="Districts", y="App_Opens",
                    title="QUARTER DISTRICT WISE APP OPENS COUNT", color_discrete_sequence=px.colors.sequential.Rainbow_r)
        st.plotly_chart(Mfig2)

#TOP ANALYSIS
#top transaction and top insurance
def Top_UC_TA_Y(df,year):

    top1=df[df['Years']==year]
    top1.reset_index(drop=True,inplace=True)

    top1G=top1.groupby('States')[['User_Count','Transaction_Amount']].sum()
    top1G.reset_index(inplace=True)
    
    col1,col2=st.columns(2)
    with col1:
        Tfig1=px.bar(data_frame=top1G, x="States", y="User_Count", title=f"{year} STATE WISE USER COUNT", color="User_Count", color_continuous_scale="Rainbow")
        st.plotly_chart(Tfig1)
    with col2:
        Tfig2=px.bar(data_frame=top1G, x="States", y="Transaction_Amount", title=f"{year} STATE WISE TRANSACTION AMOUNT", color="Transaction_Amount", color_continuous_scale="Rainbow")
        st.plotly_chart(Tfig2)

    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response=requests.get(url)
    data1=json.loads(response.content)
    state_name=[]
    for feature in data1['features']:
        state_name.append(feature['properties']['ST_NM'])

    state_name.sort()

    with col1:
        fig_india_1=px.choropleth(top1G, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                color="User_Count", color_continuous_scale="Rainbow",
                                range_color=(top1G["User_Count"].min(),top1G["User_Count"].max()),
                                hover_name="States", title=f"{year} USER COUNT", fitbounds="locations")
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)
    with col2:
        fig_india_2=px.choropleth(top1G, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                color="Transaction_Amount", color_continuous_scale="Rainbow",
                                range_color=(top1G["Transaction_Amount"].min(),top1G["Transaction_Amount"].max()),
                                hover_name="States", title=f"{year} TRANSACTION AMOUNT", fitbounds="locations")
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)

    return top1

def Top_UC_TA_Q(df,quarter):

    top2=df[df['Quarter']==quarter]
    top2.reset_index(drop=True,inplace=True)

    top2G=top2.groupby('States')[['User_Count','Transaction_Amount']].sum()
    top2G.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        Tfig1=px.bar(data_frame=top2G, x="States", y="User_Count", title=f"{quarter} QUARTER STATE WISE USER COUNT", color="User_Count", color_continuous_scale="Rainbow")
        st.plotly_chart(Tfig1)
    with col2:
        Tfig2=px.bar(data_frame=top2G, x="States", y="Transaction_Amount", title=f"{quarter} QUARTER STATE WISE TRANSACTION AMOUNT",color="Transaction_Amount", color_continuous_scale="Rainbow")
        st.plotly_chart(Tfig2)

    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response=requests.get(url)
    data1=json.loads(response.content)
    state_name=[]
    for feature in data1['features']:
        state_name.append(feature['properties']['ST_NM'])

    state_name.sort()

    with col1:
        fig_india_1=px.choropleth(top2G, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                color="User_Count", color_continuous_scale="Rainbow",
                                range_color=(top2G["User_Count"].min(),top2G["User_Count"].max()),
                                hover_name="States", title=f"{quarter} QUARTER USER COUNT", fitbounds="locations")
        fig_india_1.update_geos(visible=False)
        st.plotly_chart(fig_india_1)
    with col2:
        fig_india_2=px.choropleth(top2G, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                                color="Transaction_Amount", color_continuous_scale="Rainbow",
                                range_color=(top2G["Transaction_Amount"].min(),top2G["Transaction_Amount"].max()),
                                hover_name="States", title=f"{quarter} QUARTER TRANSACTION AMOUNT", fitbounds="locations")
        fig_india_2.update_geos(visible=False)
        st.plotly_chart(fig_india_2)


def Top_Pin_UC_TA_Y(df,state):

    top3=df[df['States']==state]
    top3.reset_index(drop=True,inplace=True)

    top3G=top3.groupby('Pincodes')[['User_Count','Transaction_Amount']].sum()
    top3G.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        Tfig1=px.pie(data_frame=top3G, names="Pincodes", values="User_Count", hole=0.35,
                    title=f"{state.upper()} PINCODE WISE USER COUNT", color_discrete_sequence=px.colors.sequential.Rainbow_r)
        st.plotly_chart(Tfig1)
    with col2:
        Tfig2=px.pie(data_frame=top3G, names="Pincodes", values="Transaction_Amount", hole=0.35,
                    title=f"{state.upper()} PINCODE WISE TRANSACTION AMOUNT", color_discrete_sequence=px.colors.sequential.Rainbow_r)
        st.plotly_chart(Tfig2)

    return top3

def Top_Pin_UC_TA_Q(df,quarter):

    top4=df[df['Quarter']==quarter]
    top4.reset_index(drop=True,inplace=True)

    top4G=top4.groupby('Pincodes')[['User_Count','Transaction_Amount']].sum()
    top4G.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        Tfig1=px.pie(data_frame=top4G, names="Pincodes", values="User_Count", hole=0.35,
                    title=f"QUARTER {quarter}, PINCODE WISE USER COUNT", color_discrete_sequence=px.colors.sequential.Rainbow_r)
        st.plotly_chart(Tfig1)
    with col2:
        Tfig2=px.pie(data_frame=top4G, names="Pincodes", values="Transaction_Amount", hole=0.35,
                    title=f"QUARTER {quarter}, PINCODE WISE TRANSACTION AMOUNT", color_discrete_sequence=px.colors.sequential.Rainbow_r)
        st.plotly_chart(Tfig2)

#top user
def Top_User_RU_Y(df,year):

    top5=df[df['Years']==year]
    top5.reset_index(drop=True,inplace=True)

    top5G=top5.groupby('States')[['Pincode_Wise_Registered_Users']].sum()
    top5G.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        Tfig1=px.bar(data_frame=top5G, x="States", y="Pincode_Wise_Registered_Users",
                title=f"{year} STATE WISE REGISTERED USERS", color="Pincode_Wise_Registered_Users",
                color_continuous_scale="Rainbow")
        st.plotly_chart(Tfig1)

    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response=requests.get(url)
    data1=json.loads(response.content)
    state_name=[]
    for feature in data1['features']:
        state_name.append(feature['properties']['ST_NM'])

    state_name.sort()
    with col2:
        Tfig2=px.choropleth(top5G, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                            color="Pincode_Wise_Registered_Users", color_continuous_scale="Rainbow",
                            range_color=(top5G["Pincode_Wise_Registered_Users"].min(),top5G["Pincode_Wise_Registered_Users"].max()),
                            hover_name="States", title=f"{year} STATE WISE REGISTERED USERS", fitbounds="locations")
        Tfig2.update_geos(visible=False)
        st.plotly_chart(Tfig2)

    return top5

def Top_User_RU_Q(df,quarter):

    top6=df[df['Quarter']==quarter]
    top6.reset_index(drop=True,inplace=True)

    top6G=top6.groupby('States')[['Pincode_Wise_Registered_Users']].sum()
    top6G.reset_index(inplace=True)

    col1,col2=st.columns(2)
    with col1:
        Tfig1=px.bar(data_frame=top6G, x="States", y="Pincode_Wise_Registered_Users",
                title=f"QUARTER {quarter}, STATE WISE REGISTERED USERS", color="Pincode_Wise_Registered_Users",
                color_continuous_scale="Rainbow")
        st.plotly_chart(Tfig1)

    url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
    response=requests.get(url)
    data1=json.loads(response.content)
    state_name=[]
    for feature in data1['features']:
        state_name.append(feature['properties']['ST_NM'])

    state_name.sort()
    with col2:
        Tfig2=px.choropleth(top6G, geojson=data1, locations="States", featureidkey="properties.ST_NM",
                            color="Pincode_Wise_Registered_Users", color_continuous_scale="Rainbow",
                            range_color=(top6G["Pincode_Wise_Registered_Users"].min(),top6G["Pincode_Wise_Registered_Users"].max()),
                            hover_name="States", title=f"QUARTER {quarter}, STATE WISE REGISTERED USERS", fitbounds="locations")
        Tfig2.update_geos(visible=False)
        st.plotly_chart(Tfig2)

def Top_User_Pin_Y(df,state):

    top7=df[df['States']==state]
    top7.reset_index(drop=True,inplace=True)

    top7G=top7.groupby('Pincodes')[['Pincode_Wise_Registered_Users']].sum()
    top7G.reset_index(inplace=True)

    Tfig1=px.pie(data_frame=top7G, names="Pincodes", values="Pincode_Wise_Registered_Users", hole=0.35,
                title=f"{state} PINCODE WISE REGISTERED USERS COUNT", color_discrete_sequence=px.colors.sequential.Rainbow_r)
    st.plotly_chart(Tfig1)

    return top7

def Top_User_Pin_Q(df,quarter):
    top8=df[df['Quarter']==quarter]
    top8.reset_index(drop=True,inplace=True)

    top8G=top8.groupby('Pincodes')[['Pincode_Wise_Registered_Users']].sum()
    top8G.reset_index(inplace=True)

    Tfig1=px.pie(data_frame=top8G, names="Pincodes", values="Pincode_Wise_Registered_Users", hole=0.35,
                title=f"QUARTER {quarter}, PINCODE WISE REGISTERED USERS COUNT", color_discrete_sequence=px.colors.sequential.Rainbow_r)
    st.plotly_chart(Tfig1)

def Trend_Line_Y(df,state):

    trend1=df[df['States']==state]
    trend1.reset_index(drop=True,inplace=True)

    trend1G=trend1.groupby('Years')[['Transaction_Count','Transaction_Amount']].sum()
    trend1G.reset_index(inplace=True)
    trend1G['Years'] = trend1G['Years'].astype(str)

    fig1=px.scatter(data_frame=trend1G, x="Years", y="Transaction_Count", trendline="ols", 
                    color="Transaction_Count", color_continuous_scale="Rainbow", title=f"TREND LINE OF TRANSACTION COUNT OF {state} OVER THE YEARS")
    fig1.update_layout(xaxis=dict(type='category'))
    st.plotly_chart(fig1)

    fig2=px.scatter(data_frame=trend1G, x="Years", y="Transaction_Amount", trendline="ols", 
                    color="Transaction_Amount", color_continuous_scale="Rainbow", title=f"TREND LINE OF TRANSACTION AMOUNT OF {state} OVER THE YEARS")
    fig2.update_layout(xaxis=dict(type='category'))
    st.plotly_chart(fig2)

    return trend1

def Trend_Line_Q(df,year):

    trend2=df[df['Years']==year]
    trend2.reset_index(drop=True,inplace=True)

    trend2G=trend2.groupby('Quarter')[['Transaction_Count','Transaction_Amount']].sum()
    trend2G.reset_index(inplace=True)
    trend2G['Quarter'] = trend2G['Quarter'].astype(str)

    fig1=px.scatter(data_frame=trend2G, x="Quarter", y="Transaction_Count", trendline="ols", 
                    color="Transaction_Count", color_continuous_scale="Rainbow", title=f"TREND LINE OF TRANSACTION COUNT OVER THE QUARTERS OF {year}")
    fig1.update_layout(xaxis=dict(type='category'))
    st.plotly_chart(fig1)

    fig2=px.scatter(data_frame=trend2G, x="Quarter", y="Transaction_Amount", trendline="ols", 
                    color="Transaction_Amount", color_continuous_scale="Rainbow", title=f"TREND LINE OF TRANSACTION AMOUNT OVER THE QUARTERS OF {year}")
    fig2.update_layout(xaxis=dict(type='category'))
    st.plotly_chart(fig2)

def TranType_All_Trend_Y(df,state):
    trend4 = df[df['States'] == state]

    trend4G = trend4.groupby(['Years', 'Transaction_Type'])[['Transaction_Amount']].sum().reset_index()
    
    fig1 = px.line(trend4G, x='Years', y='Transaction_Amount', color='Transaction_Type', 
                   color_discrete_sequence=px.colors.sequential.Rainbow_r,
                   title=f"TREND OF TRANSACTION AMOUNTS BY TYPE IN {state.upper()}",
                   labels={"Transaction_Amount": "Total Transaction Amount"},
                   markers=True)
    
    fig1.update_traces(mode='markers+lines')

    for i, row in trend4G.iterrows():
        fig1.add_annotation(
            x=row['Years'], 
            y=row['Transaction_Amount'], 
            text=f"{row['Transaction_Amount']}",
            showarrow=True,
            arrowhead=2,
            ax=20,
            ay=-30)
    fig1.update_layout(yaxis_type="log")
    
    st.plotly_chart(fig1)

def Dist_Trend_Y(df,state):

    trend5=df[df['States']==state]
    trend5.reset_index(drop=True,inplace=True)

    trend5G=trend5.groupby(['Years','Districts'])[['User_Count','Transaction_Amount']].sum()
    trend5G.reset_index(inplace=True)

    fig1 = px.line(trend5G, x='Years', y='Transaction_Amount', color='Districts', 
                    color_discrete_sequence=px.colors.sequential.Rainbow_r,
                    title=f"TREND OF TRANSACTION AMOUNTS IN DISTRICTS OF {state.upper()}",
                    labels={"Transaction_Amount": "Total Transaction Amount"},
                    markers=True)

    fig1.update_traces(mode='markers+lines')
    fig1.update_layout(xaxis=dict(type='category'))
    st.plotly_chart(fig1)

    fig2 = px.line(trend5G, x='Years', y='User_Count', color='Districts', 
                    color_discrete_sequence=px.colors.sequential.Rainbow_r,
                    title=f"TREND OF USER COUNTS IN DISTRICTS OF {state.upper()}",
                    labels={"User_Count": "Total User Count"},
                    markers=True)

    fig2.update_traces(mode='markers+lines')
    fig2.update_layout(xaxis=dict(type='category'))
    st.plotly_chart(fig2)

    return trend5

def Dist_Trend_Q(df,year):

    trend6=df[df['Years']==year]
    trend6.reset_index(drop=True,inplace=True)

    trend6G=trend6.groupby(['Quarter','Districts'])[['User_Count','Transaction_Amount']].sum()
    trend6G.reset_index(inplace=True)

    fig1 = px.line(trend6G, x='Quarter', y='Transaction_Amount', color='Districts', 
                    color_discrete_sequence=px.colors.sequential.Rainbow_r,
                    title=f"TREND OF TRANSACTION AMOUNTS IN DISTRICTS",
                    labels={"Transaction_Amount": "Total Transaction Amount"},
                    markers=True)

    fig1.update_traces(mode='markers+lines')
    fig1.update_layout(xaxis=dict(type='category'))
    st.plotly_chart(fig1)

    fig2 = px.line(trend6G, x='Quarter', y='User_Count', color='Districts', 
                    color_discrete_sequence=px.colors.sequential.Rainbow_r,
                    title=f"TREND OF USER COUNTS IN DISTRICTS",
                    labels={"User_Count": "Total User Count"},
                    markers=True)

    fig2.update_traces(mode='markers+lines')
    fig2.update_layout(xaxis=dict(type='category'))
    st.plotly_chart(fig2)

def Pin_Trend_Y(df,state):

    trend7=df[df['States']==state]
    trend7.reset_index(drop=True,inplace=True)

    trend7G=trend7.groupby(['Years','Pincodes'])[['User_Count','Transaction_Amount']].sum()
    trend7G.reset_index(inplace=True)

    fig1 = px.line(trend7G, x='Years', y='Transaction_Amount', color='Pincodes', 
                    color_discrete_sequence=px.colors.sequential.Rainbow_r,
                    title=f"TREND OF TRANSACTION AMOUNTS IN PINCODES OF {state.upper()}",
                    labels={"Transaction_Amount": "Total Transaction Amount"},
                    markers=True)

    fig1.update_traces(mode='markers+lines')
    fig1.update_layout(xaxis=dict(type='category'))
    st.plotly_chart(fig1)

    fig2 = px.line(trend7G, x='Years', y='User_Count', color='Pincodes', 
                    color_discrete_sequence=px.colors.sequential.Rainbow_r,
                    title=f"TREND OF USER COUNTS IN PINCODES OF {state.upper()}",
                    labels={"User_Count": "Total User Count"},
                    markers=True)

    fig2.update_traces(mode='markers+lines')
    fig2.update_layout(xaxis=dict(type='category'))
    st.plotly_chart(fig2)

    return trend7

def Pin_Trend_Q(df,year):

    trend8=df[df['Years']==year]
    trend8.reset_index(drop=True,inplace=True)

    trend8G=trend8.groupby(['Quarter','Pincodes'])[['User_Count','Transaction_Amount']].sum()
    trend8G.reset_index(inplace=True)

    fig1 = px.line(trend8G, x='Quarter', y='Transaction_Amount', color='Pincodes', 
                    color_discrete_sequence=px.colors.sequential.Rainbow_r,
                    title=f"TREND OF TRANSACTION AMOUNTS IN PINCODES",
                    labels={"Transaction_Amount": "Total Transaction Amount"},
                    markers=True)

    fig1.update_traces(mode='markers+lines')
    fig1.update_layout(xaxis=dict(type='category'))
    st.plotly_chart(fig1)

    fig2 = px.line(trend8G, x='Quarter', y='User_Count', color='Pincodes', 
                    color_discrete_sequence=px.colors.sequential.Rainbow_r,
                    title=f"TREND OF USER COUNTS IN PINCODES",
                    labels={"User_Count": "Total User Count"},
                    markers=True)

    fig2.update_traces(mode='markers+lines')
    fig2.update_layout(xaxis=dict(type='category'))
    st.plotly_chart(fig2)

def User_Brand_Trend_Y(df,state):

    trend9=df[df['States']==state]
    trend9.reset_index(drop=True,inplace=True)

    trend9G=trend9.groupby(['Years','Brand_Name'])[['User_Count']].sum()
    trend9G.reset_index(inplace=True)

    fig1=px.line(trend9G, x='Years', y='User_Count', color='Brand_Name', 
                        color_discrete_sequence=px.colors.sequential.Rainbow_r,
                        title=f"TREND OF USER COUNTS OF PHONEPE IN DIFFERENT PHONE BRANDS IN {state.upper()}",
                        labels={"User_Count": "Total User Count"},
                        markers=True)
    fig1.update_traces(mode='markers+lines')
    fig1.update_layout(xaxis=dict(type='category'))
    st.plotly_chart(fig1)

    return trend9

def User_Brand_Trend_Q(df,year):

    trend10=df[df['Years']==year]
    trend10.reset_index(drop=True,inplace=True)

    trend10G=trend10.groupby(['Quarter','Brand_Name'])[['User_Count']].sum()
    trend10G.reset_index(inplace=True)

    fig1=px.line(trend10G, x='Quarter', y='User_Count', color='Brand_Name', 
                        color_discrete_sequence=px.colors.sequential.Rainbow_r,
                        title=f"TREND OF USER COUNTS OF PHONEPE IN DIFFERENT PHONE BRANDS IN {state.upper()}",
                        labels={"User_Count": "Total User Count"},
                        markers=True)
    fig1.update_traces(mode='markers+lines')
    fig1.update_layout(xaxis=dict(type='category'))
    st.plotly_chart(fig1)

def User_Dist_Y(df,state):

    trend11=df[df['States']==state]
    trend11.reset_index(drop=True,inplace=True)

    trend11G=trend11.groupby(['Years','Districts'])[['User_Count','App_Opens']].sum()
    trend11G.reset_index(inplace=True)

    fig1 = px.line(trend11G, x='Years', y='App_Opens', color='Districts', 
                    color_discrete_sequence=px.colors.sequential.Rainbow_r,
                    title=f"TREND OF APP OPENS IN DISTRICTS OF {state.upper()}",
                    labels={"Transaction_Amount": "Total Transaction Amount"},
                    markers=True)

    fig1.update_traces(mode='markers+lines')
    fig1.update_layout(xaxis=dict(type='category'))
    st.plotly_chart(fig1)

    fig2 = px.line(trend11G, x='Years', y='User_Count', color='Districts', 
                    color_discrete_sequence=px.colors.sequential.Rainbow_r,
                    title=f"TREND OF USER COUNTS IN DISTRICTS OF {state.upper()}",
                    labels={"User_Count": "Total User Count"},
                    markers=True)

    fig2.update_traces(mode='markers+lines')
    fig2.update_layout(xaxis=dict(type='category'))
    st.plotly_chart(fig2)

    return trend11

def User_Dist_Q(df,year):

    trend12=df[df['Years']==year]
    trend12.reset_index(drop=True,inplace=True)

    trend12G=trend12.groupby(['Quarter','Districts'])[['User_Count','App_Opens']].sum()
    trend12G.reset_index(inplace=True)

    fig1 = px.line(trend12G, x='Quarter', y='App_Opens', color='Districts', 
                    color_discrete_sequence=px.colors.sequential.Rainbow_r,
                    title=f"TREND OF APP OPENS IN DISTRICTS IN {year}",
                    labels={"Transaction_Amount": "Total Transaction Amount"},
                    markers=True)

    fig1.update_traces(mode='markers+lines')
    fig1.update_layout(xaxis=dict(type='category'))
    st.plotly_chart(fig1)

    fig2 = px.line(trend12G, x='Quarter', y='User_Count', color='Districts', 
                    color_discrete_sequence=px.colors.sequential.Rainbow_r,
                    title=f"TREND OF USER COUNTS IN DISTRICTS IN {year}",
                    labels={"User_Count": "Total User Count"},
                    markers=True)

    fig2.update_traces(mode='markers+lines')
    fig2.update_layout(xaxis=dict(type='category'))
    st.plotly_chart(fig2)

def User_Pin_Y(df,state):

    trend13=df[df['States']==state]
    trend13.reset_index(drop=True,inplace=True)

    trend13G=trend13.groupby(['Years','Pincodes'])[['Pincode_Wise_Registered_Users']].sum()
    trend13G.reset_index(inplace=True)

    fig1 = px.line(trend13G, x='Years', y='Pincode_Wise_Registered_Users', color='Pincodes', 
                    color_discrete_sequence=px.colors.sequential.Rainbow_r,
                    title=f"TREND OF USERS IN PINCODES OF {state.upper()}",
                    labels={"Pincode_Wise_Registered_Users": "Total Users"},
                    markers=True)

    fig1.update_traces(mode='markers+lines')
    fig1.update_layout(xaxis=dict(type='category'))
    st.plotly_chart(fig1)

    return trend13

def User_Pin_Q(df,year):

    trend14=df[df['Years']==year]
    trend14.reset_index(drop=True,inplace=True)

    trend14G=trend14.groupby(['Quarter','Pincodes'])[['Pincode_Wise_Registered_Users']].sum()
    trend14G.reset_index(inplace=True)

    fig1 = px.line(trend14G, x='Quarter', y='Pincode_Wise_Registered_Users', color='Pincodes', 
                    color_discrete_sequence=px.colors.sequential.Rainbow_r,
                    title=f"TREND OF USERS IN PINCODES IN {year}",
                    labels={"Pincode_Wise_Registered_Users": "Total Users"},
                    markers=True)

    fig1.update_traces(mode='markers+lines')
    fig1.update_layout(xaxis=dict(type='category'))
    st.plotly_chart(fig1)


#streamlit code
st.set_page_config(layout ="wide")
st.title("PHONEPE DATA VISUALIZATION")
with st.sidebar:
    select=option_menu("CONTENTS",["HOME","DATA EXPLORATION","TREND CHARTS","TOP CHARTS"])

if select =="HOME":
    Htab1,Htab2,Htab3,Htab4=st.tabs(["ABOUT","PHONPE","DATA ANALYSIS","DATA VISUALIZATION"])

    with Htab1:

        st.header("INTRODUCTION")
        st.write("Welcome to the PhonePe Pulse Data Visualization and Exploration Project!")
        st.write("This capstone project aims to provide an in-depth analysis and visualization of transaction data from PhonePe, a leading digital payments platform in India.") 
        st.write("By leveraging the comprehensive data available through PhonePe Pulse, we aim to uncover meaningful insights, trends, and patterns in digital transactions across different regions and time periods.")

        st.header("ABOUT THIS PROJECT")
        st.write("This project focuses on analyzing three main types of data from PhonePe Pulse:")
        st.write("**Aggregated Data:** Overall transaction metrics aggregated over various dimensions such as time, geography, and user demographics.")
        st.write("**Map Data:** Geographic distribution of transactions, visualized on interactive maps to highlight regional trends and patterns.")
        st.write("**Top Data:** Top transaction categories, merchants, and other key entities driving the highest volumes and values of transactions.")
        st.write("We employ PostgreSQL for data storage and querying, Python scripting for data manipulation, Plotly for creating interactive charts, and Streamlit for building a user-friendly web application.")

        st.header("WHY THIS PROJECT?")
        st.write("Digital payments have revolutionized the financial landscape, especially in a diverse and rapidly growing market like India. PhonePe, as one of the major players in this sector, generates vast amounts of transaction data that can offer valuable insights into consumer behavior, economic trends, and the impact of digital financial services.")
        st.write("This project is undertaken to:")
        st.write("Highlight the significance of digital transaction data.")
        st.write("Demonstrate the use of data analysis techniques.")
        st.write("Present the findings in a visually appealing and interactive manner.")

        st.header("KEY TAKEAWAYS OF THIS PROJECT")
        st.write("By the end of this project, I have gained insights into:")
        st.write("**Python Scripting:** Manipulating and processing data for analysis.")
        st.write("**PostgreSQL:** Efficiently storing and querying large datasets.")
        st.write("**Plotly Charts:** Creating interactive and visually compelling data visualizations.")
        st.write("**Streamlit:** Building an interactive and user-friendly data application.")
        st.write("These tools and techniques combined provide a powerful framework for turning raw data into actionable insights, facilitating better decision-making and understanding of digital payment trends.")
    
    with Htab2:
        st.header("WHAT IS PHONEPE?")
        st.write("PhonePe is a leading digital payments platform in India, offering a seamless and secure way to transfer money, pay bills, recharge mobile phones, and make purchases both online and offline. Launched in December 2015, PhonePe has quickly become one of the most popular payment apps in the country, leveraging the Unified Payments Interface (UPI) system for fast and reliable transactions.")

        st.header("OVERVIEW")
        st.write("**Founding Year:** 2015")
        st.write("**Founders:** Sameer Nigam, Rahul Chari, and Burzin Engineer")
        st.write("**Headquarters:** Bangalore, India")
        st.write("**Services:** UPI-based money transfers, bill payments, recharges, online shopping, and more")
        st.write("**User Base:** Over 300 million registered users")
        st.write("**Merchant Base:** Over 25 million merchants accepting PhonePe across India")

        st.header("INDIA TRENDS")
        st.markdown("**PhonePe has significantly influenced digital payment trends in India:**")
        st.write("**Growth in Digital Transactions:** With increasing smartphone penetration and internet access, PhonePe has facilitated a massive surge in digital transactions.")
        st.write("**Geographic Penetration:** Initially more popular in urban areas, PhonePe is now seeing rapid adoption in rural and semi-urban regions.")
        st.write("**Transaction Volumes and Values:** Consistently high transaction volumes and values, especially during peak periods like festivals and sales events.")
        st.write("**User Demographics:** Wide-ranging user demographics, from young tech-savvy individuals to older adults adapting to digital payments.")

        st.header("WHY PHONEPE BUT NOT OTHER PLATFORMS?")
        st.markdown("**PhonePe stands out among other digital payment platforms for several reasons:**")
        st.write("**UPI Integration:** Early and seamless integration with UPI, ensuring fast and secure transactions.")
        st.write("**User-Friendly Interface:** Intuitive design and easy navigation make it accessible to a broad audience.")
        st.write("**Comprehensive Services:** Beyond payments, PhonePe offers a range of financial services, including mutual funds, insurance, and gold purchases.")
        st.write("**Extensive Merchant Network:** A vast and growing network of merchants accepting PhonePe, making it convenient for users to pay across various scenarios.")
        st.write("**Innovative Features:** Continuous innovation with features like PhonePe Switch, PhonePe ATM, and contextual offers and discounts.")
        st.write("These factors contribute to PhonePe's dominant position in the digital payments landscape in India, making it a preferred choice over other platforms.")

    
    with Htab3:
        st.header("OVERVIEW")
        st.write("In this section, we perform a detailed analysis of PhonePe transaction data, focusing on yearly and quarterly trends as well as state and district-wise distributions. This will provide insights into the geographic and temporal dynamics of digital payments in India.")

        st.header("YEARLY AND QUARTERLY ANALYSIS")
        st.markdown("")
        st.markdown("**Yearly Transaction Volume and Value:**")
        st.write("Analysis of total transaction volumes and values on a yearly basis.")
        st.write("Identification of growth patterns and significant changes over the years.")
        st.write("Visualization of yearly trends using bar charts and map.")
        st.markdown("")
        st.write("**Quarterly Transaction Volume and Value:**")
        st.write("Breakdown of transaction data into quarterly segments.")
        st.write("Comparison of each quarter within a year and across different years.")
        st.write("Visualization of quarterly trends using bar charts and map.")

        st.header("STATE AND DISTRICT ANALYSIS")
        st.markdown("")
        st.markdown("**State-wise Transaction Data:**")
        st.write("Analysis of transaction volumes and values across different states.")
        st.write("Identification of top-performing states in terms of digital payment adoption.")
        st.write("Visualization using choropleth maps to show transaction density and distribution.")
        st.markdown("")
        st.markdown("**District-wise Transaction Data:**")
        st.write("Detailed analysis of transaction data at the district level within states.")
        st.write("Identification of districts with high and low transaction volumes.")
        st.write("Visualization using pie charts to illustrate the proportion of transactions in each district within a state.")

    with Htab4:
        st.header("TYPES OF CHARTS USED")
        st.write("For each analysis area, we will use various data visualization techniques to present the findings clearly and interactively:")
        st.write("**Line Charts:** To show yearly and quarterly trends over time.")
        st.write("**Bar Charts:** To compare transaction volumes and values across different periods.")
        st.write("**Pie Charts:** To illustrate the proportion of transactions in each district within a state, highlighting district-wise distributions.")
        st.write("**Choropleth Maps:** To visualize state-wise transaction density.")

elif select =="DATA EXPLORATION":
    tab1, tab2, tab3 =st.tabs(["AGGREGATED ANALYIS","MAP ANALYSIS","TOP ANALYSIS"])

    with tab1:
        A_method=st.radio("Select the Method!",["AGGREGATED INSURANCE ANALYSIS","AGGREGATED TRANSACTION ANALYSIS","AGGREGATED USER ANALYSIS"])

        if A_method=="AGGREGATED INSURANCE ANALYSIS":
            col1,col2=st.columns(2)
            with col1:
                caption=st.write("Year Wise Transaction Amount & Count Analysis on Every State!")
                years=st.slider("Select a year!", Aggregated_Insurance['Years'].min(), Aggregated_Insurance['Years'].max(), Aggregated_Insurance['Years'].min())
            TranAmtCnt_Q=Transaction_Amount_Count_Y(Aggregated_Insurance,years)

            col1,col2=st.columns(2)
            with col1:
                caption=st.write("Quarter Wise Transaction Amount & Count Analysis on Every State!")
                quarters=st.slider("Select a quarter!", TranAmtCnt_Q['Quarter'].min(), TranAmtCnt_Q['Quarter'].max(), TranAmtCnt_Q['Quarter'].min())
            Transaction_Amount_Count_Q(TranAmtCnt_Q,quarters)

        elif A_method=="AGGREGATED TRANSACTION ANALYSIS":
            #year wise
            col1,col2=st.columns(2)
            with col1:
                caption=st.write("Year Wise Transaction Amount & Count Analysis on Every State!")
                year1=st.slider("Select a year!", Aggregated_Transaction['Years'].min(), Aggregated_Transaction['Years'].max(), Aggregated_Transaction['Years'].min())
            TranAmtCnt_Y=Transaction_Amount_Count_Y(Aggregated_Transaction,year1)
            #quarter wise
            col1,col2=st.columns(2)
            with col1:
                caption=st.write("Quarter Wise Transaction Amount & Count Analysis on Every State!")
                quarter1=st.slider("Select a quarter!", TranAmtCnt_Y['Quarter'].min(), TranAmtCnt_Y['Quarter'].max(), TranAmtCnt_Y['Quarter'].min())
            Transaction_Amount_Count_Q(TranAmtCnt_Y,quarter1)
            #tran type wise states
            col1,col2=st.columns(2)
            with col1:
                caption=st.write("Transaction Type Wise Transaction Amount & Count Analysis on Every State!")
                year2=TranAmtCnt_Y['Years'].min()
                trantypeList=st.selectbox("Select the transaction type you want to analyse!",Aggregated_Transaction['Transaction_Type'].unique().tolist())
            Transaction_Amount_Count_PT(TranAmtCnt_Y,trantypeList,year2)
            #state wise tran type
            col1,col2=st.columns(2)
            with col1:
                caption=st.write("State Wise Transaction Amount & Count Analysis on Every Transaction Type!")
                year3=TranAmtCnt_Y['Years'].min()
                states=st.selectbox("Select a state!",TranAmtCnt_Y['States'].unique().tolist())
            TranTypeQ=TranType_ST(TranAmtCnt_Y,states,year3)
            #quarter wise tran type
            col1,col2=st.columns(2)
            with col1:
                caption=st.write("Quarter Wise Transaction Amount & Count Analysis on Above State!")
                year4=TranAmtCnt_Y['Years'].min()
                quarter2=st.slider("Select a quarter for the transaction type you want to analyse!", TranAmtCnt_Y['Quarter'].min(), TranAmtCnt_Y['Quarter'].max(), TranAmtCnt_Y['Quarter'].min())
            TranType_QT(TranTypeQ,year4,quarter2)

        elif A_method=="AGGREGATED USER ANALYSIS":

            col1,col2=st.columns(2)
            with col1:
                caption=st.write("Year Wise Brand-User Count Analysis!")
                year5=st.slider("Select a year!", Aggregated_User['Years'].min(), Aggregated_User['Years'].max(), Aggregated_User['Years'].min())
            AU_ST=AggUser_Brand_Y(Aggregated_User,year5)

            col1,col2=st.columns(2)
            with col1:
                caption=st.write("Above Year's Quarter Wise Brand-User Count Analysis!")
                quarter3=st.slider("Select a Quarter!", Aggregated_User['Quarter'].min(), Aggregated_User['Quarter'].max(), Aggregated_User['Quarter'].min())
            AggUser_Brand_Q(AU_ST,quarter3)

            col1,col2=st.columns(2)
            with col1:
                caption=st.write("Above Year's State Wise Brand-User Count Analysis!")
                state=st.selectbox("Select a state!",AU_ST['States'].unique().tolist())
            AggUser_Brand_ST(AU_ST,state)


    with tab2:
        M_method=st.radio("Select the Method!",["MAP INSURANCE ANALYSIS","MAP TRANSACTION ANALYSIS","MAP USER ANALYSIS"])

        if M_method=="MAP INSURANCE ANALYSIS":
            col1,col2=st.columns(2)
            with col1:
                Mcap=st.write("Year Wise Transaction Amount & User Count Analysis on Every State!")
                years1=st.slider("Select a year to Analyse!", Map_Insurance['Years'].min(), Map_Insurance['Years'].max(), Map_Insurance['Years'].min())
            Map_Ins_Y=Map_User_Tran_Y(Map_Insurance,years1)

            col1,col2=st.columns(2)
            with col1:
                Mcap=st.write("Year Wise Transaction Amount & User Count Analysis on Every District!")
                state=st.selectbox("Select a State to Analyse! ", Map_Ins_Y['States'].unique().tolist())
            Map_User_Tran_DisY(Map_Ins_Y,state)

            col1,col2=st.columns(2)
            with col1:
                Mcap=st.write("Quarter Wise Transaction Amount & User Count Analysis on Every State!")
                quarters1=st.slider("Select a Quarter to Analyse!", Map_Ins_Y['Quarter'].min(), Map_Ins_Y['Quarter'].max(), Map_Ins_Y['Quarter'].min())
            Map_Ins_Q=Map_User_Tran_Q(Map_Ins_Y,quarters1)

            col1,col2=st.columns(2)
            with col1:
                Mcap=st.write("Quarter Wise Transaction Amount & User Count Analysis on Every District!")
                state=st.selectbox("Select a State to Analyse the Quarter! ", Map_Ins_Y['States'].unique().tolist())
            Map_User_Tran_DisQ(Map_Ins_Q,state)

        elif M_method=="MAP TRANSACTION ANALYSIS":
            col1,col2=st.columns(2)
            with col1:
                Mcap=st.write("Year Wise Transaction Amount & User Count Analysis on Every State!")
                years1=st.slider("Select a year to Analyse!", Map_Transaction['Years'].min(), Map_Transaction['Years'].max(), Map_Transaction['Years'].min())
            Map_Tran_Y=Map_User_Tran_Y(Map_Transaction,years1)

            col1,col2=st.columns(2)
            with col1:
                Mcap=st.write("Year Wise Transaction Amount & User Count Analysis on Every District!")
                state=st.selectbox("Select a State to Analyse! ", Map_Tran_Y['States'].unique().tolist())
            Map_User_Tran_DisY(Map_Tran_Y,state)

            col1,col2=st.columns(2)
            with col1:
                Mcap=st.write("Quarter Wise Transaction Amount & User Count Analysis on Every State!")
                quarters1=st.slider("Select a Quarter to Analyse!", Map_Tran_Y['Quarter'].min(), Map_Tran_Y['Quarter'].max(), Map_Tran_Y['Quarter'].min())
            Map_Tran_Q=Map_User_Tran_Q(Map_Tran_Y,quarters1)

            col1,col2=st.columns(2)
            with col1:
                Mcap=st.write("Quarter Wise Transaction Amount & User Count Analysis on Every District!")
                state=st.selectbox("Select a State to Analyse the Quarter! ", Map_Tran_Y['States'].unique().tolist())
            Map_User_Tran_DisQ(Map_Tran_Q,state)

        elif M_method=="MAP USER ANALYSIS":
            col1,col2=st.columns(2)
            with col1:
                Mcap=st.write("Year Wise User Count & App Opens Count Analysis on Every State!")
                years1=st.slider("Select a year to Analyse!", Map_User['Years'].min(), Map_User['Years'].max(), Map_User['Years'].min())
            Map_User_Y=Map_User_UC_AO_Y(Map_User,years1)

            col1,col2=st.columns(2)
            with col1:
                Mcap=st.write("Year Wise User Count & App Opens Count Analysis on Every District!")
                state=st.selectbox("Select a State to Analyse! ", Map_User_Y['States'].unique().tolist())
            Map_User_UC_AO_DY(Map_User_Y,state)

            col1,col2=st.columns(2)
            with col1:
                Mcap=st.write("Quarter Wise User Count & App Opens Count Analysis on Every State!")
                quarters1=st.slider("Select a Quarter to Analyse!", Map_User_Y['Quarter'].min(), Map_User_Y['Quarter'].max(), Map_User_Y['Quarter'].min())
            Map_User_Q=Map_User_UC_AO_Q(Map_User_Y,quarters1)

            col1,col2=st.columns(2)
            with col1:
                Mcap=st.write("Quarter Wise User Count App Opens Count Analysis on Every District!")
                state=st.selectbox("Select a State to Analyse the Quarter! ", Map_User_Y['States'].unique().tolist())
            Map_User_UC_AO_DQ(Map_User_Q,state)
    
    with tab3:
        T_method=st.radio("Select the Method!",["TOP INSURANCE ANALYSIS","TOP TRANSACTION ANALYSIS","TOP USER ANALYSIS"])

        if T_method=="TOP INSURANCE ANALYSIS":
            col1,col2=st.columns(2)
            with col1:
                Tcap=st.write("Year Wise Transaction Amount & User Count Analysis on Every State!")
                years1=st.slider("Select a year to Analyse!!", Top_Insurance['Years'].min(), Top_Insurance['Years'].max(), Top_Insurance['Years'].min())
            Top_Ins_Y=Top_UC_TA_Y(Top_Insurance,years1)

            col1,col2=st.columns(2)
            with col1:
                Tcap=st.write("Quarter Wise Transaction Amount & User Count Analysis on Every District!")
                quarters=st.slider("Select a Quarter to Analyse!!", Top_Ins_Y['Quarter'].min(), Top_Ins_Y['Quarter'].max(), Top_Ins_Y['Quarter'].min())
            Top_UC_TA_Q(Top_Ins_Y,quarters)

            col1,col2=st.columns(2)
            with col1:
                Tcap=st.write("Pincode Wise Transaction Amount & User Count Analysis on Every State!")
                state=st.selectbox("Select a State to Analyse the Year! ", Top_Ins_Y['States'].unique().tolist())
            Top_Ins_Pin_Y=Top_Pin_UC_TA_Y(Top_Ins_Y,state)

            col1,col2=st.columns(2)
            with col1:
                Tcap=st.write("Year Wise Transaction Amount & User Count Analysis on Every District!")
                quarters1=st.slider("Select a Quarter to Analyse the Pincode wise data!!", Top_Ins_Pin_Y['Quarter'].min(), Top_Ins_Pin_Y['Quarter'].max(), Top_Ins_Pin_Y['Quarter'].min())
            Top_Pin_UC_TA_Q(Top_Ins_Pin_Y,quarters1)


        elif T_method=="TOP TRANSACTION ANALYSIS":
            col1,col2=st.columns(2)
            with col1:
                Tcap=st.write("Year Wise Transaction Amount & User Count Analysis on Every State!")
                years1=st.slider("Select a year to Analyse the states !!", Top_Transaction['Years'].min(), Top_Transaction['Years'].max(), Top_Transaction['Years'].min())
            Top_Tran_Y=Top_UC_TA_Y(Top_Transaction,years1)

            col1,col2=st.columns(2)
            with col1:
                Tcap=st.write("Quarter Wise Transaction Amount & User Count Analysis on Every District!")
                quarters=st.slider("Select a Quarter to Analyse !!", Top_Tran_Y['Quarter'].min(), Top_Tran_Y['Quarter'].max(), Top_Tran_Y['Quarter'].min())
            Top_UC_TA_Q(Top_Tran_Y,quarters)

            col1,col2=st.columns(2)
            with col1:
                Tcap=st.write("Pincode Wise Transaction Amount & User Count Analysis on Every State!")
                state=st.selectbox("Select a State to Analyse the Year ! ", Top_Tran_Y['States'].unique().tolist())
            Top_Tran_Pin_Y=Top_Pin_UC_TA_Y(Top_Tran_Y,state)

            col1,col2=st.columns(2)
            with col1:
                Tcap=st.write("Year Wise Transaction Amount & User Count Analysis on Every District!")
                quarters1=st.slider("Select a Quarter to Analyse the Pincode wise data !!", Top_Tran_Pin_Y['Quarter'].min(), Top_Tran_Pin_Y['Quarter'].max(), Top_Tran_Pin_Y['Quarter'].min())
            Top_Pin_UC_TA_Q(Top_Tran_Pin_Y,quarters1)

        elif T_method=="TOP USER ANALYSIS":
            col1,col2=st.columns(2)
            with col1:
                Tcap=st.write("Year Wise Registered Users Count Analysis on Every State!")
                years1=st.slider("Select a year to Analyse!!", Top_User['Years'].min(), Top_User['Years'].max(), Top_User['Years'].min())
            Top_U_RU_Y=Top_User_RU_Y(Top_User,years1)

            col1,col2=st.columns(2)
            with col1:
                Tcap=st.write("Quarter Wise Registered Users Count Analysis on Every District!")
                quarters=st.slider("Select a Quarter to Analyse!!", Top_U_RU_Y['Quarter'].min(), Top_U_RU_Y['Quarter'].max(), Top_U_RU_Y['Quarter'].min())
            Top_User_RU_Q(Top_U_RU_Y,quarters)

            col1,col2=st.columns(2)
            with col1:
                Tcap=st.write("Pincode Wise Registered Users Count Analysis on Every State!")
                state=st.selectbox("Select a State to Analyse the Year! ", Top_U_RU_Y['States'].unique().tolist())
            Top_U_RU_Pin_Y=Top_User_Pin_Y(Top_U_RU_Y,state)

            col1,col2=st.columns(2)
            with col1:
                Tcap=st.write("Year Wise Registered Users Count Analysis on Every District!")
                quarters1=st.slider("Select a Quarter to Analyse the Pincode wise data!!", Top_U_RU_Pin_Y['Quarter'].min(), Top_U_RU_Pin_Y['Quarter'].max(), Top_U_RU_Pin_Y['Quarter'].min())
            Top_User_Pin_Q(Top_U_RU_Pin_Y,quarters1)
            
elif select=="TREND CHARTS":
    tab1,tab2,tab3=st.tabs(['INSURANCE','TRANSACTION','USER'])

    with tab1:
        type=st.radio('Select a Type!', ['Aggregated','Map','Top'])

        if type=='Aggregated':
            Tnhead=st.subheader("AGGREGATED INSURANCE YEARLY TREND")
            state=st.selectbox("Select a State to Analyse the Year! ", Aggregated_Insurance['States'].unique().tolist())
            Agg_trend_Y=Trend_Line_Y(Aggregated_Insurance,state)
            st.markdown("")
            Tnhead=st.subheader("AGGREGATED INSURANCE QUARTERLY TREND")
            years1=st.slider("Select a year to Analyse the Trend!!", Agg_trend_Y['Years'].min(), Agg_trend_Y['Years'].max(), Agg_trend_Y['Years'].min())
            Trend_Line_Q(Agg_trend_Y,years1)

        elif type=='Map':
            Tnhead=st.subheader("MAP INSURANCE YEARLY TREND")
            state=st.selectbox("Select a State to Analyse the Year ! ", Map_Insurance['States'].unique().tolist())
            DistTrendY=Dist_Trend_Y(Map_Insurance,state)
            st.markdown("")
            Tnhead=st.subheader("MAP INSURANCE QUARTERLY TREND")
            years1=st.slider("Select a year to Analyse the Trend !!", DistTrendY['Years'].min(), DistTrendY['Years'].max(), DistTrendY['Years'].min())
            Dist_Trend_Q(DistTrendY,years1)

        elif type=='Top':
            Tnhead=st.subheader("TOP INSURANCE YEARLY TREND")
            state=st.selectbox(" Select a State to Analyse the Year ! ", Top_Insurance['States'].unique().tolist())
            PinTrendY=Pin_Trend_Y(Top_Insurance,state)
            st.markdown("")
            Tnhead=st.subheader("TOP INSURANCE QUARTERLY TREND")
            years1=st.slider(" Select a year to Analyse the Trend !!", PinTrendY['Years'].min(), PinTrendY['Years'].max(), PinTrendY['Years'].min())
            Pin_Trend_Q(PinTrendY,years1)

    with tab2:
        type=st.radio('Select a Type!', ['Aggregated ','Map ','Top '])

        if type=='Aggregated ':
            Tnhead=st.subheader("AGGREGATED TRANSACTION YEARLY TREND")
            state=st.selectbox("Select a State to Analyse the Year!!!", Aggregated_Transaction['States'].unique().tolist())
            Agg_trend_Y=Trend_Line_Y(Aggregated_Transaction,state)
            st.markdown("")
            Tnhead=st.subheader("AGGREGATED TRANSACTION QUARTERLY TREND")
            years1=st.slider("Select a year to Analyse the Trend!", Agg_trend_Y['Years'].min(), Agg_trend_Y['Years'].max(), Agg_trend_Y['Years'].min())
            Trend_Line_Q(Agg_trend_Y,years1)
            st.markdown("")
            Tnhead=st.subheader("AGGREGATED TRANSACTION TYPES YEARLY TREND")
            state=st.selectbox("Select a State to Analyse for all the Years!!!", Aggregated_Transaction['States'].unique().tolist())
            TranType_All_Trend_Y(Aggregated_Transaction,state)


        elif type=='Map ':
            Tnhead=st.subheader("MAP TRANSACTION YEARLY TREND")
            state=st.selectbox("Select a State to Analyse the Years ! ", Map_Transaction['States'].unique().tolist())
            DistTrendY=Dist_Trend_Y(Map_Transaction,state)
            st.markdown("")
            Tnhead=st.subheader("MAP TRANSACTION QUARTERLY TREND")
            years1=st.slider("Select a year to Analyse The Trend !!", DistTrendY['Years'].min(), DistTrendY['Years'].max(), DistTrendY['Years'].min())
            Dist_Trend_Q(DistTrendY,years1)

        elif type=='Top ':
            Tnhead=st.subheader("TOP TRANSACTION YEARLY TREND")
            state=st.selectbox(" Select a State to Analyse the Years !  ", Top_Transaction['States'].unique().tolist())
            PinTrendY=Pin_Trend_Y(Top_Transaction,state)
            st.markdown("")
            Tnhead=st.subheader("TOP TRANSACTION QUARTERLY TREND")
            years1=st.slider("Select a year to Analyse The Trend !! ", PinTrendY['Years'].min(), PinTrendY['Years'].max(), PinTrendY['Years'].min())
            Pin_Trend_Q(PinTrendY,years1)

    with tab3:
        type=st.radio('Select a Type! ', [' Aggregated ',' Map ',' Top '])

        if type==' Aggregated ':
            Tnhead=st.subheader("AGGREGATED USER YEARLY TREND")
            state=st.selectbox(" Select a State to Analyse the Years !   ", Aggregated_User['States'].unique().tolist())
            UserBrandTrendY=User_Brand_Trend_Y(Aggregated_User,state)
            st.markdown("")
            Tnhead=st.subheader("AGGREGATED USER QUARTERLY TREND")
            years1=st.slider("Select a year to Analyse The Trend !!  ", UserBrandTrendY['Years'].min(), UserBrandTrendY['Years'].max(), UserBrandTrendY['Years'].min())
            User_Brand_Trend_Q(UserBrandTrendY,years1)

        elif type==' Map ':
            Tnhead=st.subheader("MAP USER YEARLY TREND")
            state=st.selectbox("  Select a State to Analyse the Years !   ", Map_User['States'].unique().tolist())
            UserDistY=User_Dist_Y(Map_User,state)
            st.markdown("")
            Tnhead=st.subheader("MAP USER QUARTERLY TREND")
            years1=st.slider(" Select a year to Analyse The Trend !!  ", UserDistY['Years'].min(), UserDistY['Years'].max(), UserDistY['Years'].min())
            User_Dist_Q(UserDistY,years1)

        elif type==' Top ':
            Tnhead=st.subheader("TOP USER YEARLY TREND")
            state=st.selectbox("  Select a State to Analyse the Years  !   ", Top_User['States'].unique().tolist())
            UserPinY=User_Pin_Y(Top_User,state)
            st.markdown("")
            Tnhead=st.subheader("MAP USER QUARTERLY TREND")
            years1=st.slider(" Select a year to Analyse The Trend !!   ", UserPinY['Years'].min(), UserPinY['Years'].max(), UserPinY['Years'].min())
            User_Pin_Q(UserPinY,years1)

elif select=="TOP CHARTS":
    pass
