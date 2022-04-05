import nba_ml.datalib.scoreboard as score
from datetime import datetime


def test_score_success():
    f = score.get_nba_scoreboard_frame(datetime(2022, 4, 2))
    f.to_csv("score.csv")

