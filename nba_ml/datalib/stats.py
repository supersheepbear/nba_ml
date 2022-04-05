import pandas as pd
from nba_api.stats.endpoints import leaguedashteamstats
from nba_api.stats.library.parameters import PerModeDetailed
from nba_ml.datalib.constants import Seasons
from datetime import datetime
import time
import logging


def get_nba_per_game_stats_frame(
        season: Seasons,
        date: datetime,
        logger=logging.getLogger(__name__)
) -> pd.DataFrame:

    try_count = 0
    while try_count < 4:
        try:
            datetime_str: str = date.strftime("%Y-%m-%d")
            data_list: list = leaguedashteamstats.LeagueDashTeamStats(
                season=season.value,
                season_type_all_star='Regular Season',
                per_mode_detailed=PerModeDetailed.per_game,
                date_to_nullable=datetime_str
            ).get_data_frames()
            return data_list[0]
        except Exception as e:
            try_count += 1
            time.sleep(3)
            if try_count >= 4:
                logger.exception(e)
                return pd.DataFrame()
