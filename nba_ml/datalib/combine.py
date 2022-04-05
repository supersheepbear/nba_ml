"""
This module contains function to combine score data and stats data
into training data that is able to be fed to models.
"""
import pandas as pd


def combine_score_and_stats_data(
        score_f: pd.DataFrame,
        stats_f: pd.DataFrame,
) -> pd.DataFrame:
    # Create a time series for if how team wins
    away_team_ids = score_f.iloc[::2].loc[:, "TEAM_ID"]
    home_team_ids = score_f.iloc[1::2].loc[:, "TEAM_ID"]
    home_team_win_series = score_f.iloc[::2].loc[:, "PTS"].reset_index(drop=True)
    home_team_win_series -= score_f.iloc[1::2].loc[:, "PTS"].reset_index(drop=True)
    home_team_win_series = (home_team_win_series < 0).astype(int)

    # clean up data before combining
    stats_f.set_index("TEAM_ID", drop=True, inplace=True)
    home_frame = stats_f.loc[home_team_ids, :]
    away_frame = stats_f.loc[away_team_ids, :]
    home_frame.reset_index(inplace=True)

    home_frame.drop(["Unnamed: 0", 'TEAM_ID', 'CFID', 'CFPARAMS', "date"], axis=1, inplace=True)
    away_frame.reset_index(inplace=True)
    away_frame.drop(["Unnamed: 0", "date", "season", 'TEAM_ID', 'CFID', 'CFPARAMS'], axis=1, inplace=True)

    # combine data
    combine_f = pd.concat([home_frame, away_frame], axis=1)

    # append if home team wins to the combined frame
    combine_f.loc[:, "Home-Team-Win"] = home_team_win_series
    return combine_f
