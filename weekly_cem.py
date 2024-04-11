import pandas as pd
from datetime import datetime
import numpy as np

file = 'C:/Users/ms228909/Downloads/LTE_Capacity_board_JCP_Only_on_Monday-11820-2024_04_08-04_15_00__135/NAC1.CSV'
file_2 = 'C:/Users/ms228909/Downloads/LTE_Capacity_board_JCP_Only_on_Monday-11567-2024_04_08-05_00_00__368/NAC3.CSV'
df_file1 = pd.read_csv(file, delimiter=';')
df_file2 = pd.read_csv(file_2, delimiter=';')

frames = [df_file1, df_file2]

df = pd.concat(frames)

# df = pd.read_csv(file, delimiter=";")


file2 = 'C:/Users/ms228909/Documents/T7 RED/SVC_TYPE_CAT.csv'
df2 = pd.read_csv(file2)


def convert_date(date_str):
    date_object = datetime.strptime(date_str, '%m.%d.%Y %H:%M:%S')
    # date_formatted = date_object.strftime('%Y-%m-%d')
    # time_formatted = date_object.strftime('%H:%M:%S')
    return date_object


vendor = input("Input Vendor: ").upper()
df["VENDOR"] = vendor

if vendor == "NSB":
    df['PERIOD_START_TIME'] = df['PERIOD_START_TIME'].apply(convert_date)
    df["PERIOD_START_TIME"] = pd.to_datetime(df["PERIOD_START_TIME"])
else:
    df["DATETIME"] = df["DATE"] + " " + df["PERIOD_START_TIME"]
    df["DATETIME"] = pd.to_datetime(df["DATETIME"])


def Dayname(row):
    if (row['PERIOD_START_TIME']).weekday() == 0:
        return "Monday"
    if (row['PERIOD_START_TIME']).weekday() == 1:
        return "Tuesday"
    if (row['PERIOD_START_TIME']).weekday() == 2:
        return "Wednesday"
    if (row['PERIOD_START_TIME']).weekday() == 3:
        return "Thursday"
    if (row['PERIOD_START_TIME']).weekday() == 4:
        return "Friday"
    if (row['PERIOD_START_TIME']).weekday() == 5:
        return "Saturday"
    if (row['PERIOD_START_TIME']).weekday() == 6:
        return "Sunday"


df['Dayname'] = df.apply(Dayname, axis=1)


def Weekday(row):
    if row['Dayname'] == "Sunday" or row['Dayname'] == "Saturday":
        return "Weekend"
    else:
        return "Weekday"


def removeBlanksEARFCN(row):
    if row['EARFCN for both Downlink and Uplink (TDD)'] == '----':
        return ""
    else:
        return row['EARFCN for both Downlink and Uplink (TDD)']


def removeBlanksEARFCN2(row):
    if row['EARFCN downlink'] == '----':
        return ""
    else:
        return row['EARFCN downlink']


def removeBlanksBW(row):
    if row['Downlink channel bandwidth'] == '----' and row['Channel bandwidth TDD'] == '----' and row[
        'Tech'] == "L26MM":
        return "20 MHz"
    if row['Downlink channel bandwidth'] == '----' and row['Channel bandwidth TDD'] == '----' and row['Tech'] == "L26":
        return "20 MHz"
    if row['Downlink channel bandwidth'] == '----' and row['Channel bandwidth TDD'] == '----' and row['Tech'] == "L23":
        return "20 MHz"
    if row['Downlink channel bandwidth'] == '----' and row['Channel bandwidth TDD'] == '----' and row['Tech'] == "L21":
        return "10 MHz"
    if row['Downlink channel bandwidth'] == '----' and row['Channel bandwidth TDD'] == '----' and row['Tech'] == "L18":
        return "10 MHz"
    if row['Downlink channel bandwidth'] == '----' and row['Channel bandwidth TDD'] == '----' and row['Tech'] == "L7":
        return "15 MHz"
    if row['Downlink channel bandwidth'] == '----' and row['Channel bandwidth TDD'] == '----' and row['Tech'] == "L9":
        return "10 MHz"
    if row['Downlink channel bandwidth'] == '----' and row['Channel bandwidth TDD'] != '':
        return ""
    else:
        return row['Downlink channel bandwidth']


def removeBlanksBW2(row):
    if row['Channel bandwidth TDD'] == '----':
        return ""
    else:
        return row['Channel bandwidth TDD']


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
    if 'F-' in row['LNCEL name'] or 'F_' in row['LNCEL name'] or 'W-' in row['LNCEL name'] or 'W_' in row[
        'LNCEL name'] or 'L-' in row['LNCEL name'] or 'L_' in row['LNCEL name'] or 'Y-' in row['LNCEL name'] or 'Y_' in \
            row[
                'LNCEL name']:
        return 'FDD'
    else:
        return 'TDD'


def RRC_User(row):

    first_value = row['RRC_CONNECTED_UE_AVG_M8051C55'].nlargest(4).mean()
    sorted_values = np.sort(row['RRC_CONNECTED_UE_AVG_M8051C55'])

    if row[('RRC_CONNECTED_UE_AVG_M8051C55', 'Sunday')] > 0 and np.isnan(row[('RRC_CONNECTED_UE_AVG_M8051C55', 'Saturday')]):
        second_value = row[('RRC_CONNECTED_UE_AVG_M8051C55', 'Sunday')]
        result = max(first_value, second_value)
        return result
    if row[('RRC_CONNECTED_UE_AVG_M8051C55', 'Saturday')] > 0 and np.isnan(row[('RRC_CONNECTED_UE_AVG_M8051C55', 'Sunday')]):
        second_value = row[('RRC_CONNECTED_UE_AVG_M8051C55', 'Saturday')]
        result = max(first_value, second_value)
        return result
    else:
        second_value = (row[('RRC_CONNECTED_UE_AVG_M8051C55', 'Sunday')] + row[
            ('RRC_CONNECTED_UE_AVG_M8051C55', 'Saturday')]) / 2
        result = max(first_value, second_value)
        return result


def PRB_DL(row):
    first_value = row['E-UTRAN Avg PRB usage per TTI DL'].nlargest(4).mean()
    sorted_values = np.sort(row['E-UTRAN Avg PRB usage per TTI DL'])

    # Calculate the second value
    if row[('E-UTRAN Avg PRB usage per TTI DL', 'Sunday')] > 0 and np.isnan(row[('E-UTRAN Avg PRB usage per TTI DL', 'Saturday')]):
        second_value = row[('E-UTRAN Avg PRB usage per TTI DL', 'Sunday')]
        result = max(first_value, second_value)
        return result
    if row[('E-UTRAN Avg PRB usage per TTI DL', 'Saturday')] > 0 and  np.isnan(row[('E-UTRAN Avg PRB usage per TTI DL', 'Sunday')]):
        second_value = row[('E-UTRAN Avg PRB usage per TTI DL', 'Saturday')]
        result = max(first_value, second_value)
        return result
    else:
        second_value = (row[('E-UTRAN Avg PRB usage per TTI DL', 'Sunday')] + row[
            ('E-UTRAN Avg PRB usage per TTI DL', 'Saturday')]) / 2
        result = max(first_value, second_value)
        return result


def cell_no_4rfs(row):
    if row["LNCEL name"].endswith("4RFS"):
        return row["LNCEL name"][:-5]
    if row["LNCEL name"].endswith("4TRFS"):
        return row["LNCEL name"][:-6]
    else:
        return row["LNCEL name"]

def Sitename(row):
    if '_D' in row['SITENAME']:
        return  row['SITENAME'][:-2]
    if '_' in row['SITENAME']:
        return  row['SITENAME'][:-2]
    else:
        return  row['SITENAME']


df['Tech'] = df.apply(Tech, axis=1)
df['Duplex'] = df.apply(Duplex, axis=1)

df['LNCEL name'] = df.apply(cell_no_4rfs, axis=1)

df['Sector'] = df['LNCEL name'].str[-1:]

result_strings = [s.rsplit("-", 1)[0] for s in df["LNCEL name"]]
sitename = [s[:-1] if s else s for s in result_strings]
df['SITENAME'] = sitename
df['SITENAME'] = df.apply(Sitename, axis=1)

df['BCF-Sector'] = df['SITENAME'].astype(str) + "-" + df['Sector'].astype(str)

df['Weekday'] = df.apply(Weekday, axis=1)
df['EARFCN for both Downlink and Uplink (TDD)'] = df.apply(removeBlanksEARFCN, axis=1)
df['EARFCN downlink'] = df.apply(removeBlanksEARFCN2, axis=1)
df['Downlink channel bandwidth'] = df.apply(removeBlanksBW, axis=1)
df['Channel bandwidth TDD'] = df.apply(removeBlanksBW2, axis=1)

df['Combine_EARFCN'] = df['EARFCN for both Downlink and Uplink (TDD)'].astype(str) + df['EARFCN downlink'].astype(str)

df['Combine_BW'] = df['Downlink channel bandwidth'].astype(str) + df['Channel bandwidth TDD'].astype(str)
df['Combine_BW'] = df['Combine_BW'].str.replace(' MHz', '')

df['EARFCN_BW'] = (df['Combine_EARFCN'].astype(str) + "_" + df['Combine_BW'].astype(str))

df["Duplex_BW"] = df["Duplex"].astype(str) + "_" + df["Combine_BW"].astype(str)
merge_df = pd.merge(df, df2[['LNCEL name', 'DUPLEX_TECH_BW']], on='LNCEL name', how='left')

pivot_df = merge_df.pivot_table(index=['DUPLEX_TECH_BW', 'Duplex_BW', 'SITENAME', 'BCF-Sector', 'LNCEL name'],
                                columns=['Dayname'],
                                values=['RRC_CONNECTED_UE_AVG_M8051C55', 'E-UTRAN Avg PRB usage per TTI DL'])

numeric_columns = ['RRC_CONNECTED_UE_AVG_M8051C55', 'E-UTRAN Avg PRB usage per TTI DL']

for column in pivot_df.columns:
    if column in numeric_columns:
        pivot_df[column] = pd.to_numeric(pivot_df[column], errors='coerce')

pivot_df['RRC_User'] = pivot_df.apply(RRC_User, axis=1)
pivot_df['RRC_User'] = pd.to_numeric(pivot_df['RRC_User'], errors='coerce')

pivot_df['PRB_DL'] = pivot_df.apply(PRB_DL, axis=1)
pivot_df['PRB_DL'] = pd.to_numeric(pivot_df['PRB_DL'], errors='coerce')

# print(pivot_df['RRC_User'].dtype)

# pivot_df['PRB_Score'] = pivot_df.apply(PRB_Score, axis=1)
# pivot_df['RRC_Score'] = pivot_df.apply(rrc_score, axis=1)

today = datetime.today()
week_num = today.isocalendar()[1]

pivot_df.to_csv(
    f'C:/Users/ms228909/Downloads/CEM_{week_num - 1}.csv')
