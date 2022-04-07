import yaml
import nba_ml.datalib.constants as constants
from datetime import timedelta
import nba_ml.utils.log as log
import os
import datetime
import pandas as pd
import tensorflow as tf
import numpy as np
import xgboost as xgb
from colorama import Fore, Style, init, deinit


if __name__ == "__main__":

    logger = log.create_logger(logger_name='predict_wins_xgboost',
                               log_path=datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S.log"))

    with open("config.yaml") as file:
        cfg = yaml.load(file, Loader=yaml.SafeLoader)

    # if we do not have an all data csv and want to use raw combined data files
    if cfg["read_from_combined_data"]:
        all_frames_list = []
        for season_name in cfg['seasons']:
            season_str = constants.Seasons[season_name].value
            logger.info("Reading data from season: {}".format(season_str))
            start_date = constants.SEASONS_START_END_DATES[season_str][0]
            end_date = constants.SEASONS_START_END_DATES[season_str][1]

            delta = end_date - start_date

            # Loop through all days in this season
            for i in range(delta.days + 1):
                date = start_date + timedelta(days=i)
                date_str = date.strftime("%Y-%m-%d")
                # do not create date if the time is beyond today
                today = datetime.datetime.today()
                if date > today:
                    continue
                # do not create data if it is start of seasons
                if date < start_date + timedelta(days=20):
                    continue
                combined_data_path = os.path.join(cfg["combined_data_folder"], date_str + ".csv")
                # do no read data if data not exists
                if not os.path.exists(combined_data_path):
                    continue
                else:
                    all_frames_list.append(pd.read_csv(combined_data_path))
        combined_f = pd.concat(all_frames_list)
        combined_f.reset_index(drop=True, inplace=True)
        combined_f.to_csv(cfg['all_combined_data_path'], index=False)
    else:
        combined_f = pd.read_csv(cfg['all_combined_data_path'])

    train_f = combined_f.drop(
        #['Home-Team-Win', 'Unnamed: 0', 'TEAM_NAME', 'date', 'TEAM_NAME.1', 'season', 'Unnamed: 0'],
        ['Home-Team-Win', 'Unnamed: 0', 'TEAM_NAME', 'date', 'TEAM_NAME.1', 'season', 'Unnamed: 0'],
        axis=1,
    )
    train_f.to_csv(cfg['train_data_path'], index=False)

    # Start training

    try:
        init()
        xgb_ml = xgb.Booster()
        # xgb_ml.load_model('Models/XGBoost_Models/XGBoost_74.5%_ML.json')
        xgb_ml.load_model(cfg["model_path"])
        logger.info('Start normalizing data')
        train_arrays = train_f.values
        train_arrays = train_arrays.astype(float)
        train_arrays = tf.keras.utils.normalize(train_arrays, axis=1)

        predictions_array = []

        total_counts = len(train_arrays)
        count = 0
        logger.info('Start predictions')
        for row in train_arrays:

            if (count % (total_counts / 10)) == 0:
                logger.info("progress: {}/{}".format(count, total_counts))
            predictions_array.append(xgb_ml.predict(xgb.DMatrix(np.array([row]))))
            count += 1

        result_dict = {"winprob_home": [], "winprob_away": []}
        for item in predictions_array:
            result_dict["winprob_home"].append(item[0][1])
            result_dict["winprob_away"].append(item[0][0])
        pd.DataFrame(result_dict).to_csv(cfg["predict_data_path"], index=False)
        predict_data_with_combined_f = pd.concat([combined_f, pd.DataFrame(result_dict)], axis=1)
        predict_data_with_combined_f.to_csv(cfg['predict_data_with_combined_path'], index=False)
    except Exception as e:
        logger.exception(e)


