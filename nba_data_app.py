!pip install nba_api
import streamlit as st
from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import players
import pandas as pd
import altair as alt

# Define function to get player career stats
def get_player_stats(player_id):
    player_stats = playercareerstats.PlayerCareerStats(player_id=player_id)
    headers = player_stats.get_dict()['resultSets'][0]['headers']
    data = player_stats.get_dict()['resultSets'][0]['rowSet']
    df = pd.DataFrame(data, columns=headers)
    # Extract the year from the SEASON_ID column and convert it to an integer
    df['YEAR'] = df['SEASON_ID'].apply(lambda x: int(x[:4]))
    return df



# Define function to search for player by name
def search_player(player_name):
    player_dict = players.get_players()
    for player in player_dict:
        if player['full_name'].lower() == player_name.lower():
            return player['id']
    return None

def plot_player_stats(df, chart_type, stat):
    df = df.dropna(subset=['YEAR'])
    df['YEAR'] = df['YEAR'].astype(int)
    if chart_type == "Bar Chart":
        chart = alt.Chart(df).mark_bar().encode(
            x=alt.X('YEAR:O', axis=alt.Axis(format='d')), y=alt.Y(stat), color='TEAM_ABBREVIATION'
        ).interactive()
    elif chart_type == "Scatter Plot":
        chart = alt.Chart(df).mark_circle().encode(
            x=alt.X('YEAR:O', axis=alt.Axis(format='d')), y=alt.Y(stat), color='TEAM_ABBREVIATION'
        ).interactive()
    elif chart_type == "Box Plot":
        chart = alt.Chart(df).mark_boxplot().encode(
            x=alt.X('YEAR:O', axis=alt.Axis(format='d')), y=alt.Y(stat), color='TEAM_ABBREVIATION'
        ).interactive()
    else:
        chart = alt.Chart(df).mark_rect().encode(
            x=alt.X('YEAR:O', axis=alt.Axis(format='d')), y=alt.Y(stat), color=alt.Color(stat)
        ).interactive()
    return chart


def app():
    st.title("NBA Player Stats")
    player_name = st.text_input("Enter player name:")
    if player_name:
        player_id = search_player(player_name)
        if player_id:
            st.write(f"Player found: {player_name}")
            df = get_player_stats(player_id)
            chart_type = st.selectbox("Select chart type:", ("Bar Chart", "Scatter Plot", "Box Plot", "Heat Map"))
            # Create radio buttons for chart type and stat
            stat_options = ['PTS', 'AST', 'REB', 'STL', 'BLK', 'FGM', 'FGA', 'FG3M', 'FG3A', 'FTM', 'FTA', 'TOV']
            stat = st.selectbox("Select stat:", stat_options)

            # Plot player stats based on user selections
            st.altair_chart(plot_player_stats(df, chart_type, stat), use_container_width=True)
        else:
            st.write(f"Player not found: {player_name}")

if __name__ == "__main__":
    app()

