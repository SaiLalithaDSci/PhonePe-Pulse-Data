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
                        password='sailalitha',
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

#streamlit code
st.set_page_config(layout ="wide")
st.title("PHONEPE DATA VISUALIZATION")
with st.sidebar:
    select=option_menu("EXPLORE",["HOME","DATA EXPLORATION","TOP CHARTS"])

if select =="HOME":
    Htab1,Htab2,Htab3,Htab4,Htabe5=st.tabs(["ABOUT","PHONPE","DATA ANALYSIS","DATA VISUALIZATION","REFERENCES"])


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
            pass
    
    with tab3:
        T_method=st.radio("Select the Method!",["TOP INSURANCE ANALYSIS","TOP TRANSACTION ANALYSIS","TOP USER ANALYSIS"])

        if T_method=="TOP INSURANCE ANALYSIS":
            pass

        elif T_method=="TOP TRANSACTION ANALYSIS":
            pass

        elif T_method=="TOP USER ANALYSIS":
            pass
    
elif select=="TOP CHARTS":
    pass
