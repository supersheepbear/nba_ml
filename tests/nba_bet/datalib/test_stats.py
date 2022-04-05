import nba_ml.datalib.stats as stats
from datetime import datetime
import nba_ml.datalib.constants as constants


def test_stats_success():
    f = stats.get_nba_per_game_stats_frame(
        season=constants.Seasons.SEASON_2021,
        date=datetime(2022, 4, 2)
    )
    f.to_csv("stats.csv")


