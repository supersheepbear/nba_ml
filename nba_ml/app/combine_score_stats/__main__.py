import yaml
import nba_ml.datalib.constants as constants
import nba_ml.datalib.combine as combine
from datetime import timedelta
import nba_ml.utils.log as log
import os
import datetime
import pandas as pd


if __name__ == "__main__":

    logger = log.create_logger(logger_name='combine_score_stats',
                               log_path=datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S.log"))

    with open("config.yaml") as file:
        cfg = yaml.load(file, Loader=yaml.SafeLoader)

    for season_name in cfg['seasons']:

        logger.info("combine data from season: {}".format(season_name))

        season_str = constants.Seasons[season_name].value

        start_date = constants.SEASONS_START_END_DATES[season_str][0]
        end_date = constants.SEASONS_START_END_DATES[season_str][1]

        delta = end_date - start_date

        # Loop through all days in this season
        for i in range(delta.days + 1):
            try:
                # get date and previous day date
                date = start_date + timedelta(days=i)
                predate = date - timedelta(1)
                date_str = date.strftime("%Y-%m-%d")
                predate_str = predate.strftime("%Y-%m-%d")

                # do not create date if the time is beyond today
                today = datetime.datetime.today()
                if date > today:
                    continue
                # do not create data if it is start of seasons
                if date < start_date + timedelta(days=10):
                    continue

                output_path = os.path.join(cfg["output_folder"], date_str + ".csv")

                # do no create date if data already exists
                if os.path.exists(output_path):
                    continue

                # start to combine data for this day
                logger.info(" date {} data is being combined. ".format(date))

                score_path = os.path.join(cfg["score_folder"], date_str + ".csv")
                stats_path = os.path.join(cfg["stats_folder"], predate_str + ".csv")

                # do no create date if data already exists
                if not os.path.exists(score_path):
                    logger.info(" date {} score data does not exist. ".format(date))
                    continue
                if not os.path.exists(stats_path):
                    logger.info(" date {} stats data does not exist. ".format(predate))
                    continue

                score_f = pd.read_csv(score_path)
                stats_f = pd.read_csv(stats_path)
                frame = combine.combine_score_and_stats_data(
                    score_f,
                    stats_f
                )
                if len(frame) != 0:
                    frame.loc[:, "date"] = date_str
                    frame.to_csv(output_path)

            except Exception as e:
                logger.exception(e)
                continue
