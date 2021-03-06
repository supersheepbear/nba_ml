import enum
from datetime import datetime


class Seasons(enum.Enum):
    SEASON_2007 = "2007-08"
    SEASON_2008 = "2008-09"
    SEASON_2009 = "2009-10"
    SEASON_2010 = "2010-11"
    SEASON_2011 = "2011-12"
    SEASON_2012 = "2012-13"
    SEASON_2013 = "2013-14"
    SEASON_2014 = "2014-15"
    SEASON_2015 = "2015-16"
    SEASON_2016 = "2016-17"
    SEASON_2017 = "2017-18"
    SEASON_2018 = "2018-19"
    SEASON_2019 = "2019-20"
    SEASON_2020 = "2020-21"
    SEASON_2021 = "2021-22"


SEASONS_YEARS_MAPPING = {
    "2007-08": [2007, 2008],
    "2008-09": [2008, 2009],
    "2009-10": [2009, 2010],
    "2010-11": [2010, 2011],
    "2011-12": [2011, 2012],
    "2012-13": [2012, 2013],
    "2013-14": [2013, 2014],
    "2014-15": [2014, 2015],
    "2015-16": [2015, 2016],
    "2016-17": [2016, 2017],
    "2017-18": [2017, 2018],
    "2018-19": [2018, 2019],
    "2019-20": [2019, 2020],
    "2020-21": [2020, 2021],
    "2021-22": [2021, 2022],
}


SEASONS_START_END_DATES = {
    "2007-08": [datetime(2007, 10, 30), datetime(2008, 4, 16)],
    "2008-09": [datetime(2008, 10, 28), datetime(2009, 4, 15)],
    "2009-10": [datetime(2009, 10, 27), datetime(2010, 4, 14)],
    "2010-11": [datetime(2010, 10, 27), datetime(2011, 4, 14)],
    "2011-12": [datetime(2011, 12, 26), datetime(2012, 4, 26)],
    "2012-13": [datetime(2012, 10, 30), datetime(2013, 4, 17)],
    "2013-14": [datetime(2013, 10, 29), datetime(2014, 4, 16)],
    "2014-15": [datetime(2014, 10, 28), datetime(2015, 4, 15)],
    "2015-16": [datetime(2015, 10, 28), datetime(2016, 4, 13)],
    "2016-17": [datetime(2016, 10, 25), datetime(2017, 4, 12)],
    "2017-18": [datetime(2017, 10, 18), datetime(2018, 4, 15)],
    "2018-19": [datetime(2018, 10, 17), datetime(2019, 4, 11)],
    "2019-20": [datetime(2019, 10, 22), datetime(2020, 8, 14)],
    "2020-21": [datetime(2020, 12, 23), datetime(2021, 5, 16)],
    "2021-22": [datetime(2021, 10, 19), datetime(2022, 4, 10)],
}
