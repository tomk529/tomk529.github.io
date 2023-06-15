from espn_api.baseball import League
from pybaseball import top_prospects
from pybaseball import statcast_pitcher
from pybaseball import playerid_lookup
from sklearn.preprocessing import MinMaxScaler, StandardScaler

import requests
import pandas as pd
import re
import numpy as np
import webbrowser



def main():
    league = League(league_id=11440, year=2023, espn_s2='AECZ66kDRRhtgUj0GsqKdWZTO5msNBrPmH51Ct1eTuOE9eZGzI0%2Buv0l1kmUN%2FUXRtXu22zeH52Ie3QmgeCykSGgS9plMjJ8ccOrPs%2FoOIQxi2pBL%2FNKLpRUZws7kERpmuJx%2FhA1K%2FssvkMfPM2u8JraTNImdfXBeIr1mjoEIAdIQoEafOWW12sK9KNoQIcAGYCtBmDqKnEBkrA%2Bv7%2FecRD%2FgFerxpUmbn3vQxKr7XqguCvLa8NAW69ihwPxYsan%2BkFiIQXAsAoW4W7pHS0d2U5E', swid='{8A4EEB56-684E-403A-8EEB-56684E603AE9}')
    available_pitchers(league)
    # available_batters(league)
    top_pitching_prospects()
    # top_batting_prospects()
    available_prospect_check(league)
    # available_batter_check(league)
    # advanced_stats(league)
    money_ball(league)
    web_display(league)

def available_pitchers(league):

    pos_map = {
        0: 'C', 1: '1B', 2: '2B', 3: '3B', 4: 'SS', 5: 'OF', 6: '2B/SS', 7: '1B/3B', 8: 'LF', 9: 'CF', 10: 'RF', 11: 'DH', 12: 'UTIL', 13: 'P', 14: 'SP', 15: 'RP', 16: 'BE', 17: 'IL', 19: 'IF' # 1B/2B/SS/3B
        # 18, 21, 22 have appeared but unknown what position they correspond to
    }

    P_raw = league.free_agents(size=500, position_id=14)
    SP_raw = league.free_agents(size=500, position_id=16)
    RP_raw = league.free_agents(size=500, position_id=15)

    p_formatted_waiver = []
    sp_formatted_waiver = []
    rp_formatted_waiver = []
    count = 0

    for pitcher in P_raw:
        count += 1
        formatted_item = pitcher.name
        p_formatted_waiver.append(formatted_item)

    p_list = "\n".join(p_formatted_waiver)

    for pitcher in SP_raw:
        count += 1
        formatted_item = pitcher.name
        sp_formatted_waiver.append(formatted_item)

    sp_list = "\n".join(sp_formatted_waiver)

    for pitcher in RP_raw:
        count += 1
        formatted_item = pitcher.name
        rp_formatted_waiver.append(formatted_item)

    rp_list = "\n".join(rp_formatted_waiver)

    all_pitchers = p_list + "\n" + sp_list + "\n" + rp_list

    num_columns =  1

    all_pitchers = all_pitchers.split('\n')

    rows = [all_pitchers[i:i+num_columns] for i in range(0, len(all_pitchers), num_columns)]
    dict_list = [{f"Column{i}": row[i] for i in range(num_columns)} for row in rows]

    df_all_pitchers = pd.DataFrame(dict_list)

    new_column_names = {
    "Column0": "Available_Pitchers",
    }
    df_all_pitchers = df_all_pitchers.rename(columns=new_column_names)

    return df_all_pitchers

def available_batters(league):
    
    pos_map = {
        0: 'C', 1: '1B', 2: '2B', 3: '3B', 4: 'SS', 5: 'OF', 6: '2B/SS', 7: '1B/3B', 8: 'LF', 9: 'CF', 10: 'RF', 11: 'DH', 12: 'UTIL', 13: 'P', 14: 'SP', 15: 'RP', 16: 'BE', 17: 'IL', 19: 'IF' # 1B/2B/SS/3B
        # 18, 21, 22 have appeared but unknown what position they correspond to
    }

    bat_raw = []

    for pos in range(13):
        bat_raw.append(league.free_agents(size=1000, position_id=pos))

    bat_formatted_waiver = []
    count = 0

    for batter in bat_raw:
        count += 1
        bat_formatted_waiver.append(batter)

    # bat_list = "\n".join(bat_formatted_waiver)
    print(bat_list)
    num_columns =  1

    all_batters = all_batters.split('\n')

    rows = [all_batters[i:i+num_columns] for i in range(0, len(all_batters), num_columns)]
    dict_list = [{f"Column{i}": row[i] for i in range(num_columns)} for row in rows]

    df_all_batters = pd.DataFrame(dict_list)

    new_column_names = {
    "Column0": "Available_Pitchers",
    }
    df_all_batters = df_all_batters.rename(columns=new_column_names)

    return df_all_batters

def top_pitching_prospects():

    url = f"https://www.mlb.com/prospects/stats/top-prospects?type=all&dateRange=Year2023&minPA=1#pitchers"
    res = requests.get(url, timeout=None).content
    prospectList = pd.read_html(res)
    return prospectList[1]

def top_batting_prospects():
    
    url = f"https://www.mlb.com/prospects/stats/top-prospects?type=all&dateRange=Year2023&minPA=1#pitchers"
    res = requests.get(url, timeout=None).content
    battingProspectList = pd.read_html(res)
    return battingProspectList[0]

def available_prospect_check(league):
    
    var1=top_pitching_prospects()
    var2=available_pitchers(league)
    
    top_available_df = pd.merge(var2, var1, left_on='Available_Pitchers', right_on='Player', how='inner')

    top_available_df['K/9'] = top_available_df['SO'] / 9
    top_available_df['BB/9'] = top_available_df['BB'] / 9
    top_available_df['FIP'] = ((13*top_available_df['HRA']+3*(top_available_df['BB'])-2*top_available_df['SO'])/top_available_df['IP']) + 3.2

    sorted_FIP_df = top_available_df.sort_values(by=['FIP'],ascending=False)
    sorted_K9_df = top_available_df.sort_values(by=['K/9'],ascending=False)

    sorted_FIP_df = sorted_FIP_df[sorted_FIP_df['IP'] > 18]
    sorted_K9_df = sorted_K9_df[sorted_K9_df['IP'] > 18]
    sorted_K9_df = sorted_K9_df.reset_index(drop=True)
    sorted_FIP_df = sorted_FIP_df.reset_index(drop=True)
    sorted_K9_df.index += 1
    sorted_FIP_df.index += 1

    columns_to_print = ['Player', 'Age', 'G', 'IP', 'FIP', 'K/9','BB/9', 'H',  'R',  'ER',  'BB',  'SO',  'HRA',  'Outs', 'ERA',  'WHIP']

    # print("\n\nTop 20 Pitchers by K/9\n\n")
    # print(sorted_K9_df[columns_to_print].head(20))
    # print("\n\n------------------------------------------------------------------------------------\n\n")
    # print("Top 20 Pitchers by FIP\n\n")
    # print(sorted_FIP_df[columns_to_print].head(20))
    # print("\n\n")
    sorted_K9_df = sorted_K9_df[columns_to_print]
    sorted_FIP_df = sorted_FIP_df[columns_to_print]
    
    return sorted_K9_df
    # sorted_FIP_df.to_csv("/Users/tomkatsaros/Desktop/top_prospects_FIP.csv")
    # sorted_K9_df.to_csv("/Users/tomkatsaros/Desktop/top_prospects_k9.csv")


def available_batter_check(league):
    
    var1=top_batting_prospects()
    var2=available_batters(league)
    
    top_available_df = pd.merge(var2, var1, left_on='Available_Pitchers', right_on='Player', how='inner')

    top_available_df['K/9'] = top_available_df['SO'] / 9
    top_available_df['BB/9'] = top_available_df['BB'] / 9
    top_available_df['FIP'] = ((13*top_available_df['HRA']+3*(top_available_df['BB'])-2*top_available_df['SO'])/top_available_df['IP']) + 3.2

    sorted_FIP_df = top_available_df.sort_values(by=['FIP'],ascending=False)
    sorted_K9_df = top_available_df.sort_values(by=['K/9'],ascending=False)

    sorted_FIP_df = sorted_FIP_df[sorted_FIP_df['IP'] > 18]
    sorted_K9_df = sorted_K9_df[sorted_K9_df['IP'] > 18]
    sorted_K9_df = sorted_K9_df.reset_index(drop=True)
    sorted_FIP_df = sorted_FIP_df.reset_index(drop=True)
    sorted_K9_df.index += 1
    sorted_FIP_df.index += 1

    columns_to_print = ['Player', 'Age', 'G', 'IP', 'FIP', 'K/9','BB/9', 'H',  'R',  'ER',  'BB',  'SO',  'HRA',  'Outs', 'ERA',  'WHIP']

def advanced_stats(league):
    
    df = available_pitchers(league)
    df1 = pd.DataFrame(df)
    df1[['First_Name', 'Last_Name']] = df1['Available_Pitchers'].str.split(' ', n=1, expand=True)
    # only top 25 for speed sake
    df1=df1.head(25)

    csv_df = pd.DataFrame()

    for index, row in df1.iterrows():
        first_name = row['First_Name']
        last_name = row['Last_Name']
        
        first_name_lower = first_name.lower()
        last_name_lower = last_name.lower()
        
        key = playerid_lookup(last_name_lower, first_name_lower)

        count = 0

        if not key.empty:
            key = pd.DataFrame(key)
            player_id = key['key_mlbam'].values[0]
            # Example of grouping by pitch type for average release speed for arbitrary date range
            data = statcast_pitcher('2023-04-01', '2023-06-01', player_id=player_id)
            group_data = data.groupby('pitch_type')['release_speed'].mean()
            group_data['Name'] = f"{first_name} {last_name}"
            csv_df = csv_df._append(group_data)
        else:
            print(f"No matching player found for {first_name} {last_name}")

    print('\n\nSample Average Pitch Speed\n\n')
    print(csv_df)
    csv_df.to_csv("/Users/tomkatsaros/Desktop/pitch_speeds.csv")

def money_ball(league):

    df = available_prospect_check(league)
    print(df)
    print('\n\n')

    # 1. Negative Transformation -- higher FIP & K/9 are better while the inverse is true for other variables
    df['FIP'] = -1 * df['FIP']
    df['K/9'] = -1 * df['K/9']

    # 2. Standardization
    standard_scaler = StandardScaler()  
    standardized_data = standard_scaler.fit_transform(df[['ERA', 'WHIP', 'K/9', 'BB/9', 'FIP']])  
    df_standardized = pd.DataFrame(standardized_data, columns=['ERA', 'WHIP', 'K/9', 'BB/9', 'FIP'])
    new_column_names = {'ERA': 'ERA_Std', 'WHIP': 'WHIP_Std', 'K/9': 'K/9_Std', 'BB/9': 'BB/9_Std', 'FIP': 'FIP_Std'}
    df_standardized = df_standardized.rename(columns=new_column_names)
    merged_df = pd.merge(df, df_standardized, left_index=True, right_index=True)

    column_names = ['ERA_Std', 'WHIP_Std', 'K/9_Std', 'BB/9_Std', 'FIP_Std']
    ranking_df = merged_df
    ranking_df['Total'] = merged_df[column_names].sum(axis=1)

    columns_to_include = ['Player', 'Age', 'ERA', 'WHIP', 'K/9', 'BB/9', 'FIP', 'Total'] 
    ranking_df = ranking_df[columns_to_include]
    ranking_df['FIP'] = -1 * ranking_df['FIP']
    ranking_df['K/9'] = -1 * ranking_df['K/9']
    ranking_df['K/9'] = ranking_df['K/9'].apply(lambda x: round(x, 2))
    ranking_df['BB/9'] = ranking_df['BB/9'].apply(lambda x: round(x, 2))
    ranking_df['FIP'] = ranking_df['FIP'].apply(lambda x: round(x, 2))
    ranking_df['Total'] = ranking_df['Total'].apply(lambda x: round(x, 2))

    print(ranking_df.head(25).sort_values('Total'))

    return ranking_df

    # turn FIP & K/9 into negative scores, then stae the scores and sum them creating a new aggregated score
    
def web_display(league):
        
    df = money_ball(league)
    df = pd.DataFrame(df)
    df = df.head(25).sort_values('Total')

    # Convert DataFrame to HTML table with modified CSS
    table_html = df.to_html(index=False, classes='spaced-table')

    # HTML template with updated CSS styling
    html_template = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            /* Center the table on the screen */
            .spaced-table {{
                margin-left: auto;
                margin-right: auto;
                border-collapse: separate;
                border-spacing: 10px;
            }}
            /* Center-align the column headers */
            .spaced-table th {{
                text-align: center;
            }}
            /* Add lines to separate each row */
            .spaced-table tr:nth-child(even) {{
                background-color: #f2f2f2;
            }}
            .spaced-table td, .spaced-table th {{
                border-bottom: 1px solid #ddd;
                padding: 8px;
            }}
        </style>
    </head>
    <body>
        {table_html}
    </body>
    </html>
    """

    with open('/Users/tomkatsaros/Documents/testpython/prospects.html', 'w') as f:
        f.write(html_template)

    webbrowser.open('file:///Users/tomkatsaros/Documents/testpython/prospects.html')

main()

