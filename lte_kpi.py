import sqlalchemy as sa
import pandas as pd
import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import pydeck as pdk
import plotly.graph_objects as go
import humanize
from streamlit_login_auth_ui.widgets import __login__

connection_params = {
    'user': 'root',
    'password': 'toor',
    'host': 'localhost'
}

engine = sa.create_engine(
    f"mysql+mysqlconnector://{connection_params['user']}:{connection_params['password']}@{connection_params['host']}")


st.set_page_config(page_title="LTE Dashboard", page_icon=":earth_asia:", layout="wide")

user_input = st.sidebar.text_input(f"Enter preferred Sitenames/Provinces:", "",
                                   placeholder="Format: 'input1', 'input2', ..., ")
if user_input == "":
    site_default_val = "'12STNAZARETHCDOMOR', '10IDMAWABCVLYCOW'"
    province_default_val = "'DAVAO DE ORO'"
else:
    site_default_val = ""
    province_default_val = ""

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.title(":earth_asia: Dashboard")

st.markdown("<style>div.block-container{padding-top:50px}</style>", unsafe_allow_html=True)
st.markdown("<style>.st-af{font-size: 10px;}</style>", unsafe_allow_html=True)

# town = st.sidebar.multiselect("Select Town", loc_df["TOWN"].unique(), default="MAWAB", key="single_select")
# if len(town) > 1:
#     st.warning("Please select only one option.")
#     selected_option = town[:1]
# cvrt_town_str = str(town)

query_location = "SELECT TOWN FROM test.lte_kpi "
loc_df = pd.read_sql(query_location, engine)

query1 = ("SELECT DATE, Cell_Name, SITENAME, Tech,"
          "SUM(RRC_CONNECTED_UE) AS RRC_CONNECTED_UE, SUM(LTE_DLTRAFFIC_MB_JCP) AS LTE_DLTRAFFIC_MB_JCP,"
          "SUM(LTE_ULTRAFFIC_MB_JCP) AS LTE_ULTRAFFIC_MB_JCP, SUM(LTE_VOLTE_USER_JCP) AS LTE_VOLTE_USER_JCP,"
          "SUM(CELL_AVAIL_LTE_5750_NUM) AS CELL_AVAIL_LTE_5750_NUM, SUM(CELL_AVAIL_LTE_5750_DEN) AS CELL_AVAIL_LTE_5750_DEN,"
          "SUM(RRC_LTE_5218_NUM) AS RRC_LTE_5218_NUM, SUM(RRC_LTE_5218_DEN) AS RRC_LTE_5218_DEN,"
          "SUM(ERAB_SSR_LTE_5017_NUM) AS ERAB_SSR_LTE_5017_NUM, SUM(ERAB_SSR_LTE_5017_DEN) AS ERAB_SSR_LTE_5017_DEN,"
          "SUM(ACT_QCI_DROP_NUM) AS ACT_QCI_DROP_NUM, SUM(ACT_QCI_DROP_DEN) AS ACT_QCI_DROP_DEN,"
          "SUM(IaFHO_SR_LTE_5568_NUM) AS IaFHO_SR_LTE_5568_NUM, SUM(IaFHO_SR_LTE_5568_DEN) AS IaFHO_SR_LTE_5568_DEN,"
          "SUM(LTE_PRBDL_UTIL_JCP_NUM) AS LTE_PRBDL_UTIL_JCP_NUM, SUM(LTE_PRBDL_UTIL_JCP_DENOM) AS LTE_PRBDL_UTIL_JCP_DENOM,"
          "SUM(LTE_PRBUL_UTIL_JCP_NUM) AS LTE_PRBUL_UTIL_JCP_NUM, SUM(LTE_PRBUL_UTIL_JCP_DENOM) AS LTE_PRBUL_UTIL_JCP_DENOM,"
          "SUM(LTE_DL_USER_TPUT_JCP_NUM_V2) AS LTE_DL_USER_TPUT_JCP_NUM_V2, SUM(LTE_DL_USER_TPUT_JCP_DENOM_V2) AS LTE_DL_USER_TPUT_JCP_DENOM_V2,"
          "SUM(LTE_UL_USER_TPUT_JCP_NUM_V2) AS LTE_UL_USER_TPUT_JCP_NUM_V2, SUM(LTE_UL_USER_TPUT_JCP_DENOM_V2) AS LTE_UL_USER_TPUT_JCP_DENOM_V2,"
          "SUM(LTE_S1FAILURES_JCP) AS S1_FAILURES, AVG(RSSI_PUCCH_LTE_5441) AS INTERFERENCE,"
          "SUM(LTE_TA_0_500_JCP) AS TA_500, SUM(LTE_TA_500_1KM_JCP) AS TA_500_1KM,"
          "SUM(LTE_TA_1KM_2KM_JCP) AS TA_1KM_2KM, SUM(LTE_TA_2KM_3500M_JCP) AS TA_2KM_3500M,"
          "SUM(LTE_TA_3500M_ABOVE_JCP) AS TA_3500M_ABV FROM test.lte_kpi "
          f"WHERE SITENAME IN ({user_input} {site_default_val})"
          f"GROUP BY DATE, Cell_Name, SITENAME, Tech;")

query2 = ("SELECT DATE, PROVINCE, TOWN, Tech,"
          "SUM(RRC_CONNECTED_UE) AS RRC_CONNECTED_UE, SUM(LTE_DLTRAFFIC_MB_JCP) AS LTE_DLTRAFFIC_MB_JCP,"
          "SUM(LTE_ULTRAFFIC_MB_JCP) AS LTE_ULTRAFFIC_MB_JCP, SUM(LTE_VOLTE_USER_JCP) AS LTE_VOLTE_USER_JCP,"
          "SUM(CELL_AVAIL_LTE_5750_NUM) AS CELL_AVAIL_LTE_5750_NUM, SUM(CELL_AVAIL_LTE_5750_DEN) AS CELL_AVAIL_LTE_5750_DEN,"
          "SUM(RRC_LTE_5218_NUM) AS RRC_LTE_5218_NUM, SUM(RRC_LTE_5218_DEN) AS RRC_LTE_5218_DEN,"
          "SUM(ERAB_SSR_LTE_5017_NUM) AS ERAB_SSR_LTE_5017_NUM, SUM(ERAB_SSR_LTE_5017_DEN) AS ERAB_SSR_LTE_5017_DEN,"
          "SUM(ACT_QCI_DROP_NUM) AS ACT_QCI_DROP_NUM, SUM(ACT_QCI_DROP_DEN) AS ACT_QCI_DROP_DEN,"
          "SUM(IaFHO_SR_LTE_5568_NUM) AS IaFHO_SR_LTE_5568_NUM, SUM(IaFHO_SR_LTE_5568_DEN) AS IaFHO_SR_LTE_5568_DEN,"
          "SUM(LTE_PRBDL_UTIL_JCP_NUM) AS LTE_PRBDL_UTIL_JCP_NUM, SUM(LTE_PRBDL_UTIL_JCP_DENOM) AS LTE_PRBDL_UTIL_JCP_DENOM,"
          "SUM(LTE_PRBUL_UTIL_JCP_NUM) AS LTE_PRBUL_UTIL_JCP_NUM, SUM(LTE_PRBUL_UTIL_JCP_DENOM) AS LTE_PRBUL_UTIL_JCP_DENOM,"
          "SUM(LTE_DL_USER_TPUT_JCP_NUM_V2) AS LTE_DL_USER_TPUT_JCP_NUM_V2, SUM(LTE_DL_USER_TPUT_JCP_DENOM_V2) AS LTE_DL_USER_TPUT_JCP_DENOM_V2,"
          "SUM(LTE_UL_USER_TPUT_JCP_NUM_V2) AS LTE_UL_USER_TPUT_JCP_NUM_V2, SUM(LTE_UL_USER_TPUT_JCP_DENOM_V2) AS LTE_UL_USER_TPUT_JCP_DENOM_V2,"
          "SUM(LTE_S1FAILURES_JCP) AS S1_FAILURES, AVG(RSSI_PUCCH_LTE_5441) AS INTERFERENCE,"
          "SUM(LTE_TA_0_500_JCP) AS TA_500, SUM(LTE_TA_500_1KM_JCP) AS TA_500_1KM,"
          "SUM(LTE_TA_1KM_2KM_JCP) AS TA_1KM_2KM, SUM(LTE_TA_2KM_3500M_JCP) AS TA_2KM_3500M,"
          "SUM(LTE_TA_3500M_ABOVE_JCP) AS TA_3500M_ABV FROM test.lte_kpi "
          # f"WHERE TOWN = {cvrt_town_str[1:-1]} "
          f"WHERE PROVINCE IN ({user_input} {province_default_val})  "
          f"GROUP BY DATE, PROVINCE, TOWN, Tech")

query3 = ("SELECT DATE, Tech, VENDOR, TERRITORY,"
          "SUM(RRC_CONNECTED_UE) AS RRC_CONNECTED_UE, SUM(LTE_DLTRAFFIC_MB_JCP) AS LTE_DLTRAFFIC_MB_JCP,"
          "SUM(LTE_ULTRAFFIC_MB_JCP) AS LTE_ULTRAFFIC_MB_JCP, SUM(LTE_VOLTE_USER_JCP) AS LTE_VOLTE_USER_JCP,"
          "SUM(CELL_AVAIL_LTE_5750_NUM) AS CELL_AVAIL_LTE_5750_NUM, SUM(CELL_AVAIL_LTE_5750_DEN) AS CELL_AVAIL_LTE_5750_DEN,"
          "SUM(RRC_LTE_5218_NUM) AS RRC_LTE_5218_NUM, SUM(RRC_LTE_5218_DEN) AS RRC_LTE_5218_DEN,"
          "SUM(ERAB_SSR_LTE_5017_NUM) AS ERAB_SSR_LTE_5017_NUM, SUM(ERAB_SSR_LTE_5017_DEN) AS ERAB_SSR_LTE_5017_DEN,"
          "SUM(ACT_QCI_DROP_NUM) AS ACT_QCI_DROP_NUM, SUM(ACT_QCI_DROP_DEN) AS ACT_QCI_DROP_DEN,"
          "SUM(IaFHO_SR_LTE_5568_NUM) AS IaFHO_SR_LTE_5568_NUM, SUM(IaFHO_SR_LTE_5568_DEN) AS IaFHO_SR_LTE_5568_DEN,"
          "SUM(LTE_PRBDL_UTIL_JCP_NUM) AS LTE_PRBDL_UTIL_JCP_NUM, SUM(LTE_PRBDL_UTIL_JCP_DENOM) AS LTE_PRBDL_UTIL_JCP_DENOM,"
          "SUM(LTE_PRBUL_UTIL_JCP_NUM) AS LTE_PRBUL_UTIL_JCP_NUM, SUM(LTE_PRBUL_UTIL_JCP_DENOM) AS LTE_PRBUL_UTIL_JCP_DENOM,"
          "SUM(LTE_DL_USER_TPUT_JCP_NUM_V2) AS LTE_DL_USER_TPUT_JCP_NUM_V2, SUM(LTE_DL_USER_TPUT_JCP_DENOM_V2) AS LTE_DL_USER_TPUT_JCP_DENOM_V2,"
          "SUM(LTE_UL_USER_TPUT_JCP_NUM_V2) AS LTE_UL_USER_TPUT_JCP_NUM_V2, SUM(LTE_UL_USER_TPUT_JCP_DENOM_V2) AS LTE_UL_USER_TPUT_JCP_DENOM_V2,"
          "SUM(LTE_S1FAILURES_JCP) AS S1_FAILURES, AVG(RSSI_PUCCH_LTE_5441) AS INTERFERENCE,"
          "SUM(LTE_TA_0_500_JCP) AS TA_500, SUM(LTE_TA_500_1KM_JCP) AS TA_500_1KM,"
          "SUM(LTE_TA_1KM_2KM_JCP) AS TA_1KM_2KM, SUM(LTE_TA_2KM_3500M_JCP) AS TA_2KM_3500M,"
          "SUM(LTE_TA_3500M_ABOVE_JCP) AS TA_3500M_ABV FROM test.lte_kpi "
          f"GROUP BY DATE, Tech, VENDOR, TERRITORY")

# data filter by based on queries
with col2:
    option_filters = ['Tech-SitName-CellName', 'Province-Town-Tech', 'Mindanao-Wide']
    default_value = "Tech-SitName-CellName"
    select_query = st.selectbox("Filter by:", option_filters, index=option_filters.index(default_value))
    if select_query == "Tech-SitName-CellName":
        selected_query = query1
        filter1 = "Tech"
        filter2 = "SITENAME"
        filter3 = "Cell_Name"
        worst_cell_text = "Cells"
    if select_query == "Province-Town-Tech":
        selected_query = query2
        filter1 = "Tech"
        filter2 = "PROVINCE"
        filter3 = "TOWN"
        worst_cell_text = "Towns"
    if select_query == "Mindanao-Wide":
        selected_query = query3
        filter1 = "Tech"
        filter2 = "TERRITORY"
        filter3 = "VENDOR"
        worst_cell_text = "VENDOR"

df = pd.read_sql(selected_query, engine)

df["DATE"] = pd.to_datetime(df["DATE"])

startDate = df["DATE"].min()
endDate = df["DATE"].max()

with col3:
    date1 = pd.to_datetime(st.date_input("Start Date: ", startDate))
with col4:
    date2 = pd.to_datetime(st.date_input("End Date: ", endDate))

df = df[(df["DATE"] >= date1) & (df["DATE"] <= date2)].copy()

# sidebar fitler1, filter2, filter3
sidebar_filter1 = st.sidebar.multiselect(f"Select {filter1}", df[filter1].unique())
if not sidebar_filter1:
    df2 = df.copy()
else:
    df2 = df[df[filter1].isin(sidebar_filter1)]

sidebar_filter2 = st.sidebar.multiselect(f"Select {filter2}", df2[filter2].unique())
if not sidebar_filter2:
    df3 = df2.copy()
else:
    df3 = df2[df2[filter2].isin(sidebar_filter2)]

sidebar_filter3 = st.sidebar.multiselect(f"Select {filter3}", df3[filter3].unique())

# filter by conditions:
if not sidebar_filter1 and not sidebar_filter2 and not sidebar_filter3:
    filtered_df = df
elif not sidebar_filter3 and not sidebar_filter2:
    filtered_df = df[df[filter1].isin(sidebar_filter1)]
elif not sidebar_filter1 and not sidebar_filter3:
    filtered_df = df[df[filter2].isin(sidebar_filter2)]
elif sidebar_filter3 and sidebar_filter2:
    filtered_df = df3[df3[filter3].isin(sidebar_filter3) & df3[filter2].isin(sidebar_filter2)]
elif sidebar_filter1 and sidebar_filter3:
    filtered_df = df3[df3[filter1].isin(sidebar_filter1) & df3[filter3].isin(sidebar_filter3)]
elif sidebar_filter1 and sidebar_filter2:
    filtered_df = df3[df3[filter1].isin(sidebar_filter1) & df3[filter2].isin(sidebar_filter2)]
elif sidebar_filter3:
    filtered_df = df3[df3[filter3].isin(sidebar_filter3)]
else:
    filtered_df = df3[
        df3[filter2].isin(sidebar_filter2) & df3[filter3].isin(sidebar_filter3) & df3[filter1].isin(sidebar_filter1)]


# cards kpi
def card_info():
    card_col1, card_col2, card_col3, card_col4, card_col5 = st.columns(5)
    count_days = filtered_df["DATE"].nunique()

    with card_col1:
        st.info(" RRC Users", icon="🧑‍🤝‍🧑")
        st.metric(label=f"Users for {count_days} days", value=humanize.intword(filtered_df["RRC_CONNECTED_UE"].sum()))

    with card_col2:
        st.info(" Traffic DL", icon="🚥")
        st.metric(label=f"Traffic DL for {count_days} days",
                  value=humanize.intword(filtered_df["LTE_DLTRAFFIC_MB_JCP"].sum()))

    with card_col3:
        rrc_sr = (filtered_df["RRC_LTE_5218_NUM"] / filtered_df["RRC_LTE_5218_DEN"]) * 100
        st.info(" RRC SR", icon="📶")
        st.metric(label=f"Avg RRC SR for {count_days} days", value=f"{rrc_sr.mean():,.2f}%")

    with card_col4:
        erab_sr = (filtered_df["ERAB_SSR_LTE_5017_NUM"] / filtered_df["ERAB_SSR_LTE_5017_DEN"]) * 100
        st.info(" ERAB SR", icon="📶")
        st.metric(label=f"ERAB SR for {count_days} days", value=f"{erab_sr.mean():,.2f}%")

    with card_col5:
        psdrop = (filtered_df["ACT_QCI_DROP_NUM"] / filtered_df["ACT_QCI_DROP_DEN"]) * 100
        st.info(" Service Drop", icon="🔽")
        st.metric(label=f"Avg PSDROP for {count_days} days", value=f"{psdrop.mean():,.2f}%")


# --------------------------traffic and users-----------------------------
def traffc_users():
    with st.expander(":chart: Overall Traffic and Users"):
        st.subheader(":chart: Overall Traffic and Users")
        traffic_user_df = filtered_df.groupby(by=["DATE", filter1], as_index=False)[
            ["RRC_CONNECTED_UE", "LTE_DLTRAFFIC_MB_JCP",
             "LTE_ULTRAFFIC_MB_JCP", "LTE_VOLTE_USER_JCP"]].sum()

        cl1, cl2 = st.columns(2)

        with cl1:
            rrc_user_tab1, rrc_user_tab2 = st.tabs(["Per tech", "Overall"])
            traffic_ul_tab1, traffic_ul_tab2 = st.tabs(["Per tech", "Overall"])

            rrc_user_fig1 = px.bar(traffic_user_df, x="DATE", y="RRC_CONNECTED_UE", color=filter1, template="seaborn",
                                   title="Overall RRC Users")
            rrc_user_fig2 = px.bar(traffic_user_df, x="DATE", y="RRC_CONNECTED_UE", template="seaborn",
                                   title="Overall RRC Users")
            with rrc_user_tab1:
                rrc_user_fig1.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
                st.plotly_chart(rrc_user_fig1, use_container_width=True, height=150)
            with rrc_user_tab2:
                rrc_user_fig2.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
                st.plotly_chart(rrc_user_fig2, use_container_width=True, height=150)

            traffic_ul_fig1 = px.bar(traffic_user_df, x="DATE", y="LTE_ULTRAFFIC_MB_JCP", color=filter1,
                                     template="seaborn",
                                     title="Overall Traffic UL")
            traffic_ul_fig2 = px.bar(traffic_user_df, x="DATE", y="LTE_ULTRAFFIC_MB_JCP",
                                     template="seaborn",
                                     title="Overall Traffic UL")
            with traffic_ul_tab1:
                traffic_ul_fig1.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
                st.plotly_chart(traffic_ul_fig1, use_container_width=True, height=150)
            with traffic_ul_tab2:
                traffic_ul_fig2.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
                st.plotly_chart(traffic_ul_fig2, use_container_width=True, height=150)

        with cl2:
            traffic_dl_tab1, traffic_dl_tab2 = st.tabs(["Per tach", "Overall"])
            volte_ue_tab1, volte_ue_tab2 = st.tabs(["Per tach", "Overall"])

            traffic_dl_fig1 = px.bar(traffic_user_df, x="DATE", y="LTE_DLTRAFFIC_MB_JCP", color=filter1,
                                     template="seaborn",
                                     title="Overall Traffic DL")
            traffic_dl_fig2 = px.bar(traffic_user_df, x="DATE", y="LTE_DLTRAFFIC_MB_JCP",
                                     template="seaborn",
                                     title="Overall Traffic DL")
            with traffic_dl_tab1:
                traffic_dl_fig1.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
                st.plotly_chart(traffic_dl_fig1, use_container_width=True, height=150)
            with traffic_dl_tab2:
                traffic_dl_fig2.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
                st.plotly_chart(traffic_dl_fig2, use_container_width=True, height=150)

            volte_ue_fig1 = px.bar(traffic_user_df, x="DATE", y="LTE_VOLTE_USER_JCP", color=filter1, template="seaborn",
                                   title="Overall VoLTE Users")
            volte_ue_fig2 = px.bar(traffic_user_df, x="DATE", y="LTE_VOLTE_USER_JCP", template="seaborn",
                                   title="Overall VoLTE Users")
            with volte_ue_tab1:
                volte_ue_fig1.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
                st.plotly_chart(volte_ue_fig1, use_container_width=True, height=150)
            with volte_ue_tab2:
                volte_ue_fig2.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
                st.plotly_chart(volte_ue_fig2, use_container_width=True, height=150)


# --------------------------- Major KPI --------------------------------------
def major_kpi():
    with st.expander(":chart: Major KPIs"):
        st.subheader(":chart: Major KPIs")

        sec3_col1, sec3_col2 = st.columns(2)
        sec2_col1, sec2_col2 = st.columns(2)

        major_kpi = filtered_df.groupby(by=
                                        ["DATE", filter1], as_index=False)[
            ["CELL_AVAIL_LTE_5750_NUM", "CELL_AVAIL_LTE_5750_DEN", "RRC_LTE_5218_NUM", "RRC_LTE_5218_DEN",
             "ERAB_SSR_LTE_5017_NUM", "ERAB_SSR_LTE_5017_DEN", "ACT_QCI_DROP_NUM", "ACT_QCI_DROP_DEN",
             "IaFHO_SR_LTE_5568_NUM", "IaFHO_SR_LTE_5568_DEN", "LTE_PRBDL_UTIL_JCP_NUM", "LTE_PRBDL_UTIL_JCP_DENOM",
             "LTE_PRBUL_UTIL_JCP_NUM", "LTE_PRBUL_UTIL_JCP_DENOM", "LTE_DL_USER_TPUT_JCP_NUM_V2",
             "LTE_DL_USER_TPUT_JCP_DENOM_V2",
             "LTE_UL_USER_TPUT_JCP_NUM_V2", "LTE_UL_USER_TPUT_JCP_DENOM_V2",
             ]].sum()

        with sec3_col1:
            rrc_sr = (major_kpi["RRC_LTE_5218_NUM"] / major_kpi["RRC_LTE_5218_DEN"]) * 100
            rrc_sr_fig1 = px.line(major_kpi, x="DATE", y=rrc_sr, color=filter1, template="seaborn",
                                  title="RRC Success Rate")
            rrc_sr_fig1.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
            st.plotly_chart(rrc_sr_fig1, use_container_width=True, height=150)

            psdrop = (major_kpi["ACT_QCI_DROP_NUM"] / major_kpi["ACT_QCI_DROP_DEN"]) * 100
            psdrop_fig1 = px.line(major_kpi, x="DATE", y=psdrop, color=filter1, template="seaborn",
                                  title="Service Drop Rate")
            psdrop_fig1.update_layout(xaxis=dict(showgrid=False), yaxis=dict(showgrid=False))
            st.plotly_chart(psdrop_fig1, use_container_width=True, height=150)

        with sec3_col2:
            erab_sr = (major_kpi["ERAB_SSR_LTE_5017_NUM"] / major_kpi["ERAB_SSR_LTE_5017_DEN"]) * 100
            fig = px.line(major_kpi, x="DATE", y=erab_sr, color=filter1, template="seaborn",
                          title="ERAB Success Rate")
            st.plotly_chart(fig, use_container_width=True, height=150)

            hosr = (major_kpi["IaFHO_SR_LTE_5568_NUM"] / major_kpi["IaFHO_SR_LTE_5568_DEN"]) * 100
            fig = px.line(major_kpi, x="DATE", y=hosr, color=filter1, template="seaborn",
                          title="Handover Success Rate")
            st.plotly_chart(fig, use_container_width=True, height=150)

        with sec2_col1:
            dl_tput = (major_kpi["LTE_DL_USER_TPUT_JCP_NUM_V2"] / major_kpi["LTE_DL_USER_TPUT_JCP_DENOM_V2"])
            fig = px.line(major_kpi, x="DATE", y=dl_tput, color=filter1, template="seaborn",
                          title="Download Throughput")
            st.plotly_chart(fig, use_container_width=True, height=150)

            prb_dl = (major_kpi["LTE_PRBDL_UTIL_JCP_NUM"] / major_kpi["LTE_PRBDL_UTIL_JCP_DENOM"]) * 100
            fig = px.line(major_kpi, x="DATE", y=prb_dl, color=filter1, template="seaborn",
                          title="PRB DL Utilization")
            st.plotly_chart(fig, use_container_width=True, height=150)

        with sec2_col2:
            ul_tput = (major_kpi["LTE_UL_USER_TPUT_JCP_NUM_V2"] / major_kpi["LTE_UL_USER_TPUT_JCP_DENOM_V2"])
            fig = px.line(major_kpi, x="DATE", y=ul_tput, color=filter1, template="seaborn",
                          title="Upload Throughput")
            st.plotly_chart(fig, use_container_width=True, height=150)

            prb_ul = (major_kpi["LTE_PRBUL_UTIL_JCP_NUM"] / major_kpi["LTE_PRBUL_UTIL_JCP_DENOM"]) * 100
            fig = px.line(major_kpi, x="DATE", y=prb_ul, color=filter1, template="seaborn",
                          title="PRB UL Utilization")
            st.plotly_chart(fig, use_container_width=True, height=150)


# --------------------------- Top Worst Cells for this town ---------------------------------------------------------
def worst_cell():
    with st.expander(f":chart: Top Worst {worst_cell_text}"):
        st.subheader(f":chart: Top Worst {worst_cell_text}")

        wc_col1, wc_col2, wc_col3, wc_col4 = st.columns(4)
        wc_sec2_col1, wc_sec2_col2, wc_sec2_col3 = st.columns(3)

        wc_date = pd.to_datetime(df["DATE"].max())

        with wc_col1:
            wc_date = pd.to_datetime(st.date_input("Select Date: ", wc_date))

        with wc_sec2_col1:
            wc_df = df[(df["DATE"] >= wc_date)].copy()
            wc_df["rrc_sr"] = (wc_df["RRC_LTE_5218_NUM"] / wc_df["RRC_LTE_5218_DEN"]) * 100
            wc_rrc_sr = wc_df.groupby(by=["DATE", filter3], as_index=False)[
                ["rrc_sr"]].mean()
            sorted_rrc = wc_rrc_sr.sort_values(by="rrc_sr", ascending=True)
            st.write(sorted_rrc)

        with wc_sec2_col2:
            wc_df = df[(df["DATE"] >= wc_date)].copy()
            wc_df["erab_sr"] = (wc_df["ERAB_SSR_LTE_5017_NUM"] / wc_df["ERAB_SSR_LTE_5017_DEN"]) * 100
            wc_erab_sr = wc_df.groupby(by=["DATE", filter3], as_index=False)[
                ["erab_sr"]].mean()
            sorted_erab = wc_erab_sr.sort_values(by="erab_sr", ascending=True)
            st.write(sorted_erab)

        with wc_sec2_col3:
            wc_df = df[(df["DATE"] >= wc_date)].copy()
            wc_df["psdrop"] = (wc_df["ACT_QCI_DROP_NUM"] / wc_df["ACT_QCI_DROP_DEN"]) * 100
            wc_psdrop = wc_df.groupby(by=["DATE", filter3], as_index=False)[
                ["psdrop"]].mean()
            sorted_psdrop = wc_psdrop.sort_values(by="psdrop", ascending=False)
            st.write(sorted_psdrop)


# --------------------------- Timing advance ---------------------------------------------------------
def timing_advance():
    with st.expander(":chart: Timing Advance"):
        st.subheader(":chart: Timing Advance")

        ta_sec2_col1, ta_sec2_col2 = st.columns(2)
        ta_col1, ta_col2, ta_col3, = st.columns(3)

        ta_500 = filtered_df.groupby(by=["DATE", filter1], as_index=False)["TA_500"].sum()
        ta_500_1km = filtered_df.groupby(by=["DATE", filter1], as_index=False)["TA_500_1KM"].sum()
        ta_1km_2km = filtered_df.groupby(by=["DATE", filter1], as_index=False)["TA_1KM_2KM"].sum()
        ta_2km_3500m = filtered_df.groupby(by=["DATE", filter1], as_index=False)["TA_2KM_3500M"].sum()
        ta_3500m_abv = filtered_df.groupby(by=["DATE", filter1], as_index=False)["TA_3500M_ABV"].sum()

        with ta_sec2_col1:
            fig = px.bar(ta_500, x="DATE", y="TA_500", color=filter1, template="seaborn",
                         title="TA 500m")
            st.plotly_chart(fig, use_container_width=True, height=150)

        with ta_sec2_col2:
            fig = px.bar(ta_500_1km, x="DATE", y="TA_500_1KM", color=filter1, template="seaborn",
                         title="TA 500m to 1km")
            st.plotly_chart(fig, use_container_width=True, height=150)

        with ta_col1:
            fig = px.bar(ta_1km_2km, x="DATE", y="TA_1KM_2KM", color=filter1, template="seaborn",
                         title="TA 1km to 2km")
            st.plotly_chart(fig, use_container_width=True, height=150)

        with ta_col2:
            fig = px.bar(ta_2km_3500m, x="DATE", y="TA_2KM_3500M", color=filter1, template="seaborn",
                         title="TA 2km to 3.5km")
            st.plotly_chart(fig, use_container_width=True, height=150)

        with ta_col3:
            fig = px.bar(ta_3500m_abv, x="DATE", y="TA_3500M_ABV", color=filter1, template="seaborn",
                         title="TA 3.5km above")
            st.plotly_chart(fig, use_container_width=True, height=150)


# --------------------------- PRE and POST ---------------------------------------------------------
def pre_post_kpi():
    with st.expander(":chart: Pre and Post KPIs"):
        st.subheader(":chart: Pre and Post KPIs")

        sec4_col1, sec4_col2, sec4_col3, sec4_col4 = st.columns(4)

        startPreDate = filtered_df["DATE"].min()
        endPreDate = filtered_df["DATE"].min()

        startPostDate = filtered_df["DATE"].max()
        endPostDate2 = filtered_df["DATE"].max()

        with sec4_col1:
            preDate1 = pd.to_datetime(st.date_input("Start Date of Pre KPI", startPreDate))
        with sec4_col2:
            preDate2 = pd.to_datetime(st.date_input("End Date of Pre KPI", endPreDate))
        with sec4_col3:
            postDate1 = pd.to_datetime(st.date_input("Start Date of Post KPI", startPostDate))
        with sec4_col4:
            postDate2 = pd.to_datetime(st.date_input("End Date of Post KPI", endPostDate2))

        pre_df = filtered_df[(filtered_df["DATE"] >= preDate1) & (filtered_df["DATE"] <= preDate2)].copy()
        post_df = filtered_df[(filtered_df["DATE"] >= postDate1) & (filtered_df["DATE"] <= postDate2)].copy()

        def pre_column(row):
            if row[filter2] != "":
                return "Pre"

        def post_column(row):
            if row[filter2] != "":
                return "Post"

        pre_df["pre_post"] = pre_df.apply(pre_column, axis=1)
        post_df["pre_post"] = post_df.apply(post_column, axis=1)

        combine_pre_post = pd.concat([pre_df, post_df])

        major_kpi = combine_pre_post.groupby(by=
                                             ["pre_post"], as_index=False)[
            ["CELL_AVAIL_LTE_5750_NUM", "CELL_AVAIL_LTE_5750_DEN", "RRC_LTE_5218_NUM", "RRC_LTE_5218_DEN",
             "ERAB_SSR_LTE_5017_NUM", "ERAB_SSR_LTE_5017_DEN", "ACT_QCI_DROP_NUM", "ACT_QCI_DROP_DEN",
             "IaFHO_SR_LTE_5568_NUM", "IaFHO_SR_LTE_5568_DEN", "LTE_PRBDL_UTIL_JCP_NUM", "LTE_PRBDL_UTIL_JCP_DENOM",
             "LTE_PRBUL_UTIL_JCP_NUM", "LTE_PRBUL_UTIL_JCP_DENOM", "LTE_DL_USER_TPUT_JCP_NUM_V2",
             "LTE_DL_USER_TPUT_JCP_DENOM_V2",
             "LTE_UL_USER_TPUT_JCP_NUM_V2", "LTE_UL_USER_TPUT_JCP_DENOM_V2", "RRC_CONNECTED_UE",
             "LTE_DLTRAFFIC_MB_JCP", "LTE_ULTRAFFIC_MB_JCP", "LTE_VOLTE_USER_JCP"
             ]].sum()

        # pp_rrc_sr = combine_pre_post.groupby(by="pre_post", as_index=False)["RRC_SR"].mean()
        # pp_erab_sr = combine_pre_post.groupby(by="pre_post", as_index=False)["ERAB_SR"].mean()
        # pp_psdrop = combine_pre_post.groupby(by="pre_post", as_index=False)["PSDROP"].mean()
        # pp_hosr = combine_pre_post.groupby(by="pre_post", as_index=False)["HOSR"].mean()
        # pp_prb_dl = combine_pre_post.groupby(by="pre_post", as_index=False)["LTE_PRB_DL"].mean()
        # pp_prb_ul = combine_pre_post.groupby(by="pre_post", as_index=False)["LTE_PRB_UL"].mean()
        # pp_dl_tput = combine_pre_post.groupby(by="pre_post", as_index=False)["DL_TPUT"].mean()
        # pp_ul_tput = combine_pre_post.groupby(by="pre_post", as_index=False)["UL_TPUT"].mean()
        #
        # pp_rrc_user = combine_pre_post.groupby(by="pre_post", as_index=False)["RRC_CONNECTED_UE"].sum()
        # pp_traffic_dl = combine_pre_post.groupby(by="pre_post", as_index=False)["LTE_DLTRAFFIC_MB_JCP"].sum()
        # pp_traffic_ul = combine_pre_post.groupby(by="pre_post", as_index=False)["LTE_ULTRAFFIC_MB_JCP"].sum()
        # pp_avail = combine_pre_post.groupby(by="pre_post", as_index=False)["AVAILABILITY"].mean()

        with sec4_col1:
            # rrc sr dif
            post_df["rrc_sr"] = (post_df["RRC_LTE_5218_NUM"] / post_df["RRC_LTE_5218_DEN"]) * 100
            pre_df["rrc_sr"] = (pre_df["RRC_LTE_5218_NUM"] / pre_df["RRC_LTE_5218_DEN"]) * 100
            major_kpi["rrc_sr"] = (major_kpi["RRC_LTE_5218_NUM"] / major_kpi["RRC_LTE_5218_DEN"]) * 100

            rrc_sr_diff = round(((post_df["rrc_sr"].mean() - pre_df["rrc_sr"].mean()) / pre_df["rrc_sr"].mean()) * 100,
                                4)
            if rrc_sr_diff < 0:
                rrc_icon = "🔻"
            else:
                rrc_icon = "🔼"
            fig = px.bar(major_kpi, x="pre_post", y="rrc_sr", template="seaborn", color="pre_post",
                         title=f"RRC SR    --- {rrc_sr_diff}% {rrc_icon} ---")
            st.plotly_chart(fig, use_container_width=True, height=60)

            # prbdl_diff
            post_df["prb_dl"] = (post_df["LTE_PRBDL_UTIL_JCP_NUM"] / post_df["LTE_PRBDL_UTIL_JCP_DENOM"]) * 100
            pre_df["prb_dl"] = (pre_df["LTE_PRBDL_UTIL_JCP_NUM"] / pre_df["LTE_PRBDL_UTIL_JCP_DENOM"]) * 100
            major_kpi["prb_dl"] = (major_kpi["LTE_PRBDL_UTIL_JCP_NUM"] / major_kpi["LTE_PRBDL_UTIL_JCP_DENOM"]) * 100

            prbdl_diff = round(
                ((post_df["prb_dl"].mean() - pre_df["prb_dl"].mean()) / pre_df["prb_dl"].mean()) * 100, 4)
            if prbdl_diff < 0:
                prbdl_icon = "🔻"
            else:
                prbdl_icon = "🔼"
            fig = px.bar(major_kpi, x="pre_post", y="prb_dl", template="seaborn", color="pre_post",
                         title=f"PRB DL    --- {prbdl_diff}% {prbdl_icon} ---")
            st.plotly_chart(fig, use_container_width=True, height=60)

            # rrc_user_diff

            rrc_user_diff = round(
                ((post_df["RRC_CONNECTED_UE"].sum() - pre_df["RRC_CONNECTED_UE"].sum()) / pre_df["RRC_CONNECTED_UE"].sum()) * 100, 4)
            if rrc_user_diff < 0:
                user_icon = "🔻"
            else:
                user_icon = "🔼"
            fig = px.bar(major_kpi, x="pre_post", y="RRC_CONNECTED_UE", template="seaborn", color="pre_post",
                         title=f"RRC Users     --- {rrc_user_diff}% {user_icon} ---")
            st.plotly_chart(fig, use_container_width=True, height=60)

        with sec4_col2:
            # erab sr diff
            post_df["erab_sr"] = (post_df["ERAB_SSR_LTE_5017_NUM"] / post_df["ERAB_SSR_LTE_5017_DEN"]) * 100
            pre_df["erab_sr"] = (pre_df["ERAB_SSR_LTE_5017_NUM"] / pre_df["ERAB_SSR_LTE_5017_DEN"]) * 100
            major_kpi["erab_sr"] = (major_kpi["ERAB_SSR_LTE_5017_NUM"] / major_kpi["ERAB_SSR_LTE_5017_DEN"]) * 100

            erab_diff = round(
                ((post_df["erab_sr"].mean() - pre_df["erab_sr"].mean()) / pre_df["erab_sr"].mean()) * 100, 4)
            if erab_diff < 0:
                erab_icon = "🔻"
            else:
                erab_icon = "🔼"
            fig = px.bar(major_kpi, x="pre_post", y="erab_sr", template="seaborn", color="pre_post",
                         title=f"ERAB SR     --- {erab_diff}% {erab_icon} ---")
            st.plotly_chart(fig, use_container_width=True, height=60)

           # lte prb ul diff
            post_df["LTE_PRB_UL"] = (post_df["LTE_PRBUL_UTIL_JCP_NUM"] / post_df["LTE_PRBUL_UTIL_JCP_DENOM"]) * 100
            pre_df["LTE_PRB_UL"] = (pre_df["LTE_PRBUL_UTIL_JCP_NUM"] / pre_df["LTE_PRBUL_UTIL_JCP_DENOM"]) * 100
            major_kpi["LTE_PRB_UL"] = (major_kpi["LTE_PRBUL_UTIL_JCP_NUM"] / major_kpi["LTE_PRBUL_UTIL_JCP_DENOM"]) * 100

            prbul_diff = round(
                ((post_df["LTE_PRB_UL"].mean() - pre_df["LTE_PRB_UL"].mean()) / pre_df[
                    "LTE_PRB_UL"].mean()) * 100, 4)
            if prbul_diff < 0:
                prbul_icon = "🔻"
            else:
                prbul_icon = "🔼"
            fig = px.bar(major_kpi, x="pre_post", y="LTE_PRB_UL", template="seaborn", color="pre_post",
                         title=f"PRB UL     --- {prbul_diff}% {prbul_icon} ---")
            st.plotly_chart(fig, use_container_width=True, height=60)

            # lte traffic dl
            traffic_dl_diff = round(
                ((post_df["LTE_DLTRAFFIC_MB_JCP"].sum() - pre_df["LTE_DLTRAFFIC_MB_JCP"].sum()) / pre_df[
                    "LTE_DLTRAFFIC_MB_JCP"].sum()) * 100, 4)
            if traffic_dl_diff < 0:
                traffic_dl_icon = "🔻"
            else:
                traffic_dl_icon = "🔼"
            fig = px.bar(major_kpi, x="pre_post", y="LTE_DLTRAFFIC_MB_JCP", template="seaborn", color="pre_post",
                         title=f"TRAFFIC DL     --- {traffic_dl_diff}% {traffic_dl_icon} ---")
            st.plotly_chart(fig, use_container_width=True, height=60)
        #
        # with sec4_col3:
        #
        #     # lte drop
        #     psdrop_diff = round(
        #         ((post_df["PSDROP"].mean() - pre_df["PSDROP"].mean()) / pre_df[
        #             "PSDROP"].mean()) * 100, 4)
        #     if psdrop_diff < 0:
        #         psdrop_icon = "🔻"
        #     else:
        #         psdrop_icon = "🔼"
        #     fig = px.bar(pp_psdrop, x="pre_post", y="PSDROP", template="seaborn", color="pre_post",
        #                  title=f"Service Drop     --- {psdrop_diff}% {psdrop_icon} ---")
        #     st.plotly_chart(fig, use_container_width=True, height=60)
        #
        #     # dl tput
        #     dl_tput_diff = round(
        #         ((post_df["DL_TPUT"].mean() - pre_df["DL_TPUT"].mean()) / pre_df[
        #             "DL_TPUT"].mean()) * 100, 4)
        #     if dl_tput_diff < 0:
        #         dltput_icon = "🔻"
        #     else:
        #         dltput_icon = "🔼"
        #     fig = px.bar(pp_dl_tput, x="pre_post", y="DL_TPUT", template="seaborn", color="pre_post",
        #                  title=f"DL Throughput     --- {dl_tput_diff}% {dltput_icon} ---")
        #     st.plotly_chart(fig, use_container_width=True, height=60)
        #
        #     # traffic UL
        #     traffic_ul_diff = round(
        #         ((post_df["LTE_ULTRAFFIC_MB_JCP"].sum() - pre_df["LTE_ULTRAFFIC_MB_JCP"].sum()) / pre_df[
        #             "LTE_ULTRAFFIC_MB_JCP"].sum()) * 100, 4)
        #     if traffic_ul_diff < 0:
        #         traffic_ul_icon = "🔻"
        #     else:
        #         traffic_ul_icon = "🔼"
        #     fig = px.bar(pp_traffic_ul, x="pre_post", y="LTE_ULTRAFFIC_MB_JCP", template="seaborn", color="pre_post",
        #                  title=f"TRAFFIC UL     --- {traffic_ul_diff}% {traffic_ul_icon} ---")
        #     st.plotly_chart(fig, use_container_width=True, height=60)
        #
        # with sec4_col4:
        #
        #     # dl tput
        #     hosr_diff = round(
        #         ((post_df["HOSR"].mean() - pre_df["HOSR"].mean()) / pre_df[
        #             "HOSR"].mean()) * 100, 4)
        #     if hosr_diff < 0:
        #         hosr_icon = "🔻"
        #     else:
        #         hosr_icon = "🔼"
        #     fig = px.bar(pp_hosr, x="pre_post", y="HOSR", template="seaborn", color="pre_post",
        #                  title=f"Handover     --- {hosr_diff}% {hosr_icon} ---")
        #     st.plotly_chart(fig, use_container_width=True, height=60)
        #
        #     # UL TPUT
        #     ul_tput_diff = round(
        #         ((post_df["UL_TPUT"].mean() - pre_df["UL_TPUT"].mean()) / pre_df[
        #             "UL_TPUT"].mean()) * 100, 4)
        #     if ul_tput_diff < 0:
        #         ul_tput_icon = "🔻"
        #     else:
        #         ul_tput_icon = "🔼"
        #     fig = px.bar(pp_ul_tput, x="pre_post", y="UL_TPUT", template="seaborn", color="pre_post",
        #                  title=f"UL Throughput     --- {ul_tput_diff}% {ul_tput_icon} ---")
        #     st.plotly_chart(fig, use_container_width=True, height=60)
        #
        #     # availability
        #     avail_diff = round(
        #         ((post_df["AVAILABILITY"].mean() - pre_df["AVAILABILITY"].mean()) / pre_df[
        #             "AVAILABILITY"].mean()) * 100, 4)
        #     if avail_diff < 0:
        #         avail_icon = "🔻"
        #     else:
        #         avail_icon = "🔼"
        #     fig = px.bar(pp_avail, x="pre_post", y="AVAILABILITY", template="seaborn", color="pre_post",
        #                  title=f"Availability     --- {avail_diff}% {avail_icon} ---")
        #     st.plotly_chart(fig, use_container_width=True, height=60)

    # ----------------- DOWNLOAD SECTION -------------------------------------------

    st.write("\n")
    st.write("\n")
    st.subheader("Download your prefer Data below:")

    csv = combine_pre_post.to_csv(index=False).encode('utf-8')
    st.download_button(label="Download Pre/Post KPI Data", data=csv, file_name="combine_pre_post.csv", mime="txt/csv",
                       help="Click here to download CSV file")

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(label="Download Raw File", data=csv, file_name="combine_pre_post.csv", mime="txt/csv",
                       help="Click here to download CSV file")

    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(label="Download Filtered Data (if filter applied)", data=csv, file_name="combine_pre_post.csv",
                       mime="txt/csv",
                       help="Click here to download CSV file")


# ---------------------------- MAIN DASHBOARD --------------------------------------------------
def main_dashboard():
    currentData = filtered_df["DATE"].max()
    dashboard_df = filtered_df[(filtered_df["DATE"] >= currentData)].copy()

    dashboard_df = dashboard_df.groupby(by=[filter2, filter3, filter1], as_index=False)[
        ["RRC_CONNECTED_UE", "LTE_PRBDL_UTIL_JCP_NUM", "LTE_PRBDL_UTIL_JCP_DENOM",
         "LTE_DL_USER_TPUT_JCP_NUM_V2", "LTE_DL_USER_TPUT_JCP_DENOM_V2",
         "LTE_UL_USER_TPUT_JCP_NUM_V2", "LTE_UL_USER_TPUT_JCP_DENOM_V2"]].sum()
    prb_dl = (dashboard_df["LTE_PRBDL_UTIL_JCP_NUM"] / dashboard_df["LTE_PRBDL_UTIL_JCP_DENOM"]) * 100

    tput_df = dashboard_df.groupby(by=[filter1], as_index=False)[
        ["LTE_DL_USER_TPUT_JCP_NUM_V2", "LTE_DL_USER_TPUT_JCP_DENOM_V2",
         "LTE_UL_USER_TPUT_JCP_NUM_V2", "LTE_UL_USER_TPUT_JCP_DENOM_V2"]].sum()
    dl_tput = (tput_df["LTE_DL_USER_TPUT_JCP_NUM_V2"] / tput_df["LTE_DL_USER_TPUT_JCP_DENOM_V2"])
    ul_tput = (tput_df["LTE_UL_USER_TPUT_JCP_NUM_V2"] / tput_df["LTE_UL_USER_TPUT_JCP_DENOM_V2"])

    dashboard_col1, dashboard_col2 = st.columns(2)

    with dashboard_col1:
        fig = px.scatter(
            dashboard_df,
            x="RRC_CONNECTED_UE",
            y=prb_dl,
            size="RRC_CONNECTED_UE",
            color=prb_dl,
            color_continuous_scale="reds",
            hover_name=filter3,
            log_x=True,
            size_max=30,
            title="PRB DL vs RRC Users",
        )
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)

    with dashboard_col2:
        fig = px.bar(tput_df, x=filter1, y=dl_tput, template="seaborn", title="DL TPUT & Tech")
        fig.add_trace(px.line(tput_df, x=filter1, y=ul_tput, template="seaborn").data[0])

        # Update layout for a dual-axis chart
        fig.update_layout(
            yaxis=dict(title='DL TPUT '),
            yaxis2=dict(title='UL TPUT', overlaying='y', side='right'),
        )
        st.plotly_chart(fig, use_container_width=True)


# with st.sidebar:
#     selected = option_menu(
#         menu_title=None,
#         options=["Home", "KPI", "Counter", "Timing Advance"],
#         icons=["house", "activity", "arrow-counterclockwise", "arrow-left-right"],
#         menu_icon="cast",
#         default_index=0,
#         styles={
#             "container": {"background-color": "transparent"}
#         }
#     )

card_info()
st.markdown("---")
main_dashboard()
traffc_users()
major_kpi()
worst_cell()
timing_advance()
pre_post_kpi()
