import pandas as pd
from datetime import datetime
import streamlit as st
import plotly.express as px
import win32api

file = 'C:/Users/ms228909/Downloads/NAC1_LTE_KPIS_2023_sched_rbt-rp006082-2024_04_11-08_52_44__239/NAC1.csv'
df = pd.read_csv(file, delimiter=";")
# df = pd.read_csv(file)

st.set_page_config(page_title="LTE", page_icon=":earth_asia:", layout="wide")


def Tech(row):
    if 'F-' in row['LNCEL name'] or 'F_' in row['LNCEL name']:
        return 'L18'
    elif 'W-' in row['LNCEL name'] or 'W_' in row['LNCEL name']:
        return 'L21'
    elif 'L-' in row['LNCEL name'] or 'L_' in row['LNCEL name']:
        return 'L7'
    elif 'Y-' in row['LNCEL name'] or 'Y_' in row['LNCEL name']:
        return 'L9'
    elif 'H-' in row['LNCEL name'] or 'H_' in row['LNCEL name']:
        return 'L26'
    elif 'K-' in row['LNCEL name'] or 'K_' in row['LNCEL name']:
        return 'L23'
    elif 'V-' in row['LNCEL name'] or 'V_' in row['LNCEL name']:
        return 'L26MM'
    elif 'G-' in row['LNCEL name'] or 'G_' in row['LNCEL name']:
        return 'L18MM'
    elif 'Q-' in row['LNCEL name'] or 'Q_' in row['LNCEL name']:
        return 'L21MM'
    else:
        return 'error'


def Duplex(row):
    if 'F-' in row['Tech'] or 'F_' in row['Tech'] or 'W-' in row['Tech'] or 'W_' in row[
        'LNCEL name'] or 'L-' in row['Tech'] or 'L_' in row['Tech'] or 'Y-' in row['Tech'] or 'Y_' in \
            row[
                'LNCEL name']:
        return 'FDD'
    else:
        return 'TDD'


def convert_date(date_str):
    # date_object = datetime.strptime(date_str, '%m.%d.%Y %H:%M:%S')
    date_object = datetime.strptime(date_str, '%m.%d.%Y')
    # date_formatted = date_object.strftime('%Y-%m-%d')
    # time_formatted = date_object.strftime('%H:%M:%S')
    return date_object

def cell_no_4rfs(row):
    if row["LNCEL name"].endswith("4RFS"):
        return row["LNCEL name"][:-5]
    if row["LNCEL name"].endswith("4TRFS"):
        return row["LNCEL name"][:-6]
    else:
        return row["LNCEL name"]


# vendor = input("Input Vendor: ").upper()
# df["VENDOR"] = vendor
df['cell_no_4rfs'] = df.apply(cell_no_4rfs, axis=1)

df['DATETIME'] = df['PERIOD_START_TIME'].apply(convert_date)
df["DATETIME"] = pd.to_datetime(df["DATETIME"])

df['Tech'] = df.apply(Tech, axis=1)
df['Duplex'] = df.apply(Duplex, axis=1)
df['Sector'] = df['cell_no_4rfs'].str[-1:]

result_strings = [s.rsplit("-", 1)[0] for s in df["LNCEL name"]]
sitename = [s[:-1] if s else s for s in result_strings]
df['SITENAME'] = sitename

numeric_columns = ['RRC_CONNECTED_UE_AVG',
                   'LTE_DLTRAFFIC_MB_JCP',
                   'LTE_ULTRAFFIC_MB_JCP',
                   'LTE_VOLTE_USER_JCP',
                   'CELL_AVAIL_LTE_DEN',
                   'CELL_AVAIL_LTE_NUM',
                   'RRC_LTE_5218_DEN',
                   'RRC_LTE_5218_NUM',
                   'ERAB_SSR_LTE_5017_DEN',
                   'ERAB_SSR_LTE_5017_NUM',
                   'ACTIV_QCI_DROP_DEN',
                   'ACTIV_QCI_DROP_NUM',
                   'IaFHO_SR_LTE_5568_DEN',
                   'IaFHO_SR_LTE_5568_NUM',
                   'LTE_PRBDL_UTIL_JCP_DEN',
                   'LTE_PRBDL_UTIL_JCP_NUM',
                   'LTE_PRBUL_UTIL_JCP_DEN',
                   'LTE_PRBUL_UTIL_JCP_NUM',
                   'LTE_DL_USER_TPUT_JCP_DENOM_V2',
                   'LTE_DL_USER_TPUT_JCP_NUM_V2',
                   'LTE_UL_USER_TPUT_JCP_DENOM_V2',
                   'LTE_UL_USER_TPUT_JCP_NUM_V2',
                   'LTE_S1_TNL_FAILURES_JCP',
                   'AvgRSSIforPUCCH_LTE_5441',
                   'LTE_TA_0_500_JCP',
                   'LTE_TA_500_1KM_JCP',
                   'LTE_TA_1KM_2KM_JCP', 'LTE_TA_2KM_3500M_JCP', 'LTE_TA_3500M_ABOVE_JCP',
                   ]

for column in df.columns:
    if column in numeric_columns:
        df[column] = pd.to_numeric(df[column], errors='coerce')

sidebar_filter1 = st.sidebar.multiselect(f"Select Sitename", df['SITENAME'].unique())
if not sidebar_filter1:
    df2 = df.copy()
else:
    df2 = df[df['SITENAME'].isin(sidebar_filter1)]

sidebar_filter2 = st.sidebar.multiselect(f"Select Tech", df2['Tech'].unique())
if not sidebar_filter2:
    df3 = df2.copy()
else:
    df3 = df2[df2['Tech'].isin(sidebar_filter2)]

sidebar_filter3 = st.sidebar.multiselect(f"Select Sector", df3['Sector'].unique())

# filter by conditions:
if not sidebar_filter1 and not sidebar_filter2 and not sidebar_filter3:
    filtered_df = df
elif not sidebar_filter3 and not sidebar_filter2:
    filtered_df = df[df['SITENAME'].isin(sidebar_filter1)]
elif not sidebar_filter1 and not sidebar_filter3:
    filtered_df = df[df['Tech'].isin(sidebar_filter2)]
elif sidebar_filter3 and sidebar_filter2:
    filtered_df = df3[df3['Sector'].isin(sidebar_filter3) & df3['Tech'].isin(sidebar_filter2)]
elif sidebar_filter1 and sidebar_filter3:
    filtered_df = df3[df3['SITENAME'].isin(sidebar_filter1) & df3['Sector'].isin(sidebar_filter3)]
elif sidebar_filter1 and sidebar_filter2:
    filtered_df = df3[df3['SITENAME'].isin(sidebar_filter1) & df3['Tech'].isin(sidebar_filter2)]
elif sidebar_filter3:
    filtered_df = df3[df3['Sector'].isin(sidebar_filter3)]
else:
    filtered_df = df3[
        df3['Tech'].isin(sidebar_filter2) & df3['Sector'].isin(sidebar_filter3) & df3['SITENAME'].isin(sidebar_filter1)]

col1, col2 = st.columns(2)
kpi_df = filtered_df.groupby(by=["DATETIME", "Tech"], as_index=False)[['RRC_LTE_5218_DEN',
                                                                                 'RRC_LTE_5218_NUM',
                                                                                 'ERAB_SSR_LTE_5017_DEN',
                                                                                 'ERAB_SSR_LTE_5017_NUM',
                                                                                 'ACTIV_QCI_DROP_DEN',
                                                                                 'ACTIV_QCI_DROP_NUM',
                                                                                 'IaFHO_SR_LTE_5568_DEN',
                                                                                 'IaFHO_SR_LTE_5568_NUM',
                                                                                 'LTE_PRBDL_UTIL_JCP_DEN',
                                                                                 'LTE_PRBDL_UTIL_JCP_NUM',
                                                                                 'LTE_PRBUL_UTIL_JCP_DEN',
                                                                                 'LTE_PRBUL_UTIL_JCP_NUM',
                                                                                 'LTE_DL_USER_TPUT_JCP_DENOM_V2',
                                                                                 'LTE_DL_USER_TPUT_JCP_NUM_V2',
                                                                                 'LTE_UL_USER_TPUT_JCP_DENOM_V2',
                                                                                 'LTE_UL_USER_TPUT_JCP_NUM_V2', ]].sum()

with col1:
    tab1, tab2 = st.tabs({"Per Tech", "Overall"})

    with tab1:
        rrc_users = filtered_df.groupby(by=["DATETIME", "Tech"], as_index=False)['RRC_CONNECTED_UE_AVG'].sum()
        fig = px.line(rrc_users, x="DATETIME", y="RRC_CONNECTED_UE_AVG", color="Tech", title="RRC USERS")
        st.plotly_chart(fig, use_container_width=True)

        kpi_df['rrc_sr'] = (kpi_df['RRC_LTE_5218_NUM'] / kpi_df['RRC_LTE_5218_DEN']) * 100
        rrc_sr_fig = px.line(kpi_df, x="DATETIME", y="rrc_sr", color="Tech", title="RRC_SR")
        st.plotly_chart(rrc_sr_fig, use_container_width=True)

        kpi_df['lte_drop'] = (kpi_df['ACTIV_QCI_DROP_NUM'] / kpi_df['ACTIV_QCI_DROP_DEN']) * 100
        lte_drop = px.line(kpi_df, x="DATETIME", y="lte_drop", color="Tech", title="LTE_DROP")
        st.plotly_chart(lte_drop, use_container_width=True)



    with tab2:
        rrc_users = filtered_df.groupby(by=["DATETIME"], as_index=False)['RRC_CONNECTED_UE_AVG'].sum()
        fig = px.line(rrc_users, x="DATETIME", y="RRC_CONNECTED_UE_AVG", title="RRC USERS")
        st.plotly_chart(fig, use_container_width=True)

        rrc_sr_df = filtered_df.groupby(by=["DATETIME"], as_index=False)[['RRC_LTE_5218_NUM', 'RRC_LTE_5218_DEN']].sum()
        rrc_sr_df['rrc_sr'] = (rrc_sr_df['RRC_LTE_5218_NUM']/rrc_sr_df['RRC_LTE_5218_DEN']) * 100
        fig = px.line(rrc_sr_df, x="DATETIME", y="rrc_sr", title="RRC_SR")
        st.plotly_chart(fig, use_container_width=True)

        lte_drop = filtered_df.groupby(by=["DATETIME"], as_index=False)[['ACTIV_QCI_DROP_NUM', 'ACTIV_QCI_DROP_DEN']].sum()
        lte_drop['lte_drop'] = (lte_drop['ACTIV_QCI_DROP_NUM'] / lte_drop['ACTIV_QCI_DROP_DEN']) * 100
        fig = px.line(lte_drop, x="DATETIME", y="lte_drop", title="LTE_DROP")
        st.plotly_chart(fig, use_container_width=True)





with col2:
    tab1, tab2 = st.tabs({"Per Tech", "Overall"})

    with tab1:
        prb_dl_df = filtered_df.groupby(by=["DATETIME", "Tech"], as_index=False)[
            ['LTE_PRBDL_UTIL_JCP_NUM', 'LTE_PRBDL_UTIL_JCP_DEN']].sum()
        prb_dl_df['prb_dl'] = (prb_dl_df['LTE_PRBDL_UTIL_JCP_NUM'] / prb_dl_df['LTE_PRBDL_UTIL_JCP_DEN']) * 100
        fig = px.line(prb_dl_df, x="DATETIME", y='prb_dl', color="Tech", title="LTE_PRB_DL")
        st.plotly_chart(fig, use_container_width=True)

        erab_sr_df = filtered_df.groupby(by=["DATETIME", "Tech"], as_index=False)[
            ['ERAB_SSR_LTE_5017_NUM', 'ERAB_SSR_LTE_5017_DEN']].sum()
        erab_sr_df['erab_sr'] = (erab_sr_df['ERAB_SSR_LTE_5017_NUM'] / erab_sr_df['ERAB_SSR_LTE_5017_DEN']) * 100
        fig = px.line(erab_sr_df, x="DATETIME", y='erab_sr', color="Tech", title="ERAB_SR")
        st.plotly_chart(fig, use_container_width=True)

        kpi_df['hosr'] = (kpi_df['IaFHO_SR_LTE_5568_NUM'] / kpi_df['IaFHO_SR_LTE_5568_DEN']) * 100
        hosr = px.line(kpi_df, x="DATETIME", y="hosr", color="Tech", title="HOSR")
        st.plotly_chart(hosr, use_container_width=True)


    with tab2:
        prb_dl_df = filtered_df.groupby(by=["DATETIME"], as_index=False)[
            ['LTE_PRBDL_UTIL_JCP_NUM', 'LTE_PRBDL_UTIL_JCP_DEN']].sum()
        prb_dl_df['prb_dl'] = (prb_dl_df['LTE_PRBDL_UTIL_JCP_NUM'] / prb_dl_df['LTE_PRBDL_UTIL_JCP_DEN']) * 100
        fig = px.line(prb_dl_df, x="DATETIME", y='prb_dl', title="LTE_PRB_DL")
        st.plotly_chart(fig, use_container_width=True)

        erab_sr_df = filtered_df.groupby(by=["DATETIME"], as_index=False)[
            ['ERAB_SSR_LTE_5017_NUM', 'ERAB_SSR_LTE_5017_DEN']].sum()
        erab_sr_df['erab_sr'] = (erab_sr_df['ERAB_SSR_LTE_5017_NUM'] / erab_sr_df['ERAB_SSR_LTE_5017_DEN']) * 100
        fig = px.line(erab_sr_df, x="DATETIME", y='erab_sr', title="ERAB_SR")
        st.plotly_chart(fig, use_container_width=True)

        hosr = filtered_df.groupby(by=["DATETIME"], as_index=False)[
            ['IaFHO_SR_LTE_5568_NUM', 'IaFHO_SR_LTE_5568_DEN']].sum()
        hosr['hosr'] = (hosr['IaFHO_SR_LTE_5568_NUM'] / hosr['IaFHO_SR_LTE_5568_DEN']) * 100
        fig = px.line(hosr, x="DATETIME", y="hosr", title="HOSR")
        st.plotly_chart(fig, use_container_width=True)

