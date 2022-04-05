import pandas as pd
from nba_api.stats.endpoints import scoreboard
from datetime import datetime
import logging
import time


def get_nba_scoreboard_frame(
        date: datetime,
        logger=logging.getLogger(__name__)
) -> pd.DataFrame:
    """_summary_

    Args:
        date (datetime): _description_
        logger (_type_, optional): _description_. Defaults to logging.getLogger(__name__).

    Returns:
        pd.DataFrame: _description_
    """
    try_count = 0
    while try_count < 4:
        try:
            datetime_str: str = date.strftime("%Y-%m-%d")
            data_list: list = scoreboard.Scoreboard(
                game_date=datetime_str
            ).get_data_frames()
            frame = data_list[1]
            if len(frame) != 0:
                frame.loc[:, "date"] = datetime_str
                logger.info(" date {} scoreboard has be collected successfully. ".format(date))
            else:
                logger.info(" date {} has not scoreboard. ".format(date))
            return frame
        except Exception as e:
            try_count += 1
            time.sleep(3)
            if try_count >= 4:
                logger.exception(e)
                return pd.DataFrame()
