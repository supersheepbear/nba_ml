import yaml
import nba_ml.datalib.constants as constants
import nba_ml.datalib.stats as stats
from datetime import timedelta
import nba_ml.utils.log as log
import os
import datetime


if __name__ == "__main__":

    logger = log.create_logger(logger_name="stats_collector",
                               log_path=datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S.log"))

    with open("config.yaml") as file:
        cfg = yaml.load(file, Loader=yaml.SafeLoader)

    for season_name in cfg['seasons']:

        logger.info("collecting data from season: {}".format(season_name))

        season_str = constants.Seasons[season_name].value

        start_date = constants.SEASONS_START_END_DATES[season_str][0]
        end_date = constants.SEASONS_START_END_DATES[season_str][1]

        delta = end_date - start_date  # returns timedelta
        try:
            for i in range(delta.days + 1):
                date = start_date + timedelta(days=i)

                today = datetime.datetime.today()
                if date > today:
                    continue

                date_str = date.strftime("%Y-%m-%d")
                output_path = os.path.join(cfg["output_folder"], date_str + ".csv")
                if os.path.exists(output_path):
                    continue
                frame = stats.get_nba_per_game_stats_frame(
                    season=constants.Seasons[season_name],
                    date=date
                )
                if frame is None:
                    logger.warning(" date {} requests returns None. Please check why. ".format(date))
                elif len(frame) == 0:
                    logger.warning(" date {} does not have data. Please check why. ".format(date))
                else:
                    frame.loc[:, "date"] = [date_str] * len(frame)
                    frame.loc[:, "season"] = [season_str] * len(frame)
                    frame.to_csv()
                    logger.info(" date {} data has be collected successfully. ".format(date))
        except Exception as e:
            logger.exception(e)
            continue
