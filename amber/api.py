import requests
from urllib import parse
import config
from .routine_dto import Routine
import pandas as pd
from typing import List


def url_of(endpoint: str):
    return parse.urljoin(config.BACKEND_API_URL, endpoint)


def routines_to_dataframe(routines: List[Routine]):
    return pd.DataFrame([
        [
            r.rtnSeq,
            int(r.rtnGoal in [0, 1]),
            int(r.rtnGoal in [0, 2]),
            r.rtnExperienceLevel,
            int(r.rtnTarget in [0, 1]),
            int(r.rtnTarget in [0, 2]),
            int(r.rtnTarget in [0, 3]),
            int(r.rtnTarget in [0, 4]),
            r.rtnKneeHealthConsidered,
            r.rtnNoiseConsidered,
            r.rtnNeckShoulderFocused,
            r.rtnLongSitter,
            r.rtnBackDiskConsidered
        ]
        for r in routines
    ],
        columns=["rtn_seq", "exc_goal_diet", "exc_goal_healthy",  "experience_level", "exc_type_lower_weight", "exc_type_upper_weight", "exc_type_all_weight", "exc_type_cardio",
                 "noise_considered", "knee_health_considered", "neck_shoulder_focused", "long_sitter", "back_disk_considered"]
    )


def get_routines_dataframe() -> List[Routine]:
    url = url_of('/routines?findExercises=false')
    try:
        response = requests.get(url).json()
        routines = [Routine.model_validate(r) for r in response]
        return routines_to_dataframe(routines)

    except Exception as e:
        print("Error")
        raise e


def get_dummy_data():
    return pd.DataFrame([
        [1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 1],
        [0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 1, 0],
        [1, 1, 1, 0, 1, 1, 0, 1, 1, 1, 0, 0],
        [0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0],
        [0, 0, 2, 0, 0, 0, 0, 0, 1, 0, 0, 0],
        [1, 1, 3, 1, 0, 1, 0, 1, 0, 1, 1, 0],
        [0, 0, 3, 0, 1, 0, 0, 0, 1, 0, 0, 1],
        [1, 1, 4, 0, 0, 1, 0, 1, 0, 0, 1, 0],
        [1, 1, 5, 0, 0, 1, 0, 1, 1, 1, 0, 0],
        [0, 0, 1, 0, 0, 0, 1, 0, 0, 1, 0, 0],
        [0, 0, 3, 1, 0, 0, 0, 0, 0, 0, 1, 0],
        [1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 0, 1],
        [0, 0, 3, 0, 1, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 4, 0, 0, 1, 1, 1, 0, 1, 0, 0],
        [1, 1, 2, 0, 0, 1, 0, 1, 1, 0, 0, 0],
        [0, 0, 5, 0, 0, 0, 0, 0, 0, 1, 1, 0],
        [0, 0, 2, 0, 1, 0, 0, 0, 1, 0, 0, 1],
        [1, 1, 2, 0, 0, 1, 0, 1, 1, 0, 0, 0],
        [0, 0, 5, 0, 0, 0, 1, 0, 1, 1, 0, 1],
        [0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 0, 0],
        [0, 0, 2, 0, 0, 0, 0, 0, 1, 1, 0, 1],
        [1, 1, 3, 1, 0, 1, 0, 1, 0, 1, 1, 0],
        [1, 1, 1, 0, 1, 1, 0, 1, 0, 1, 0, 0],
        [0, 0, 5, 0, 0, 0, 1, 0, 1, 0, 0, 0],
        [0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        [0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0],
        [0, 0, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0],
        [1, 1, 5, 0, 1, 1, 0, 1, 0, 1, 0, 0],
        [1, 1, 2, 0, 0, 1, 1, 1, 0, 0, 1, 0],
        [0, 0, 5, 0, 0, 0, 1, 0, 0, 1, 0, 0],
        [1, 1, 4, 1, 0, 1, 0, 1, 1, 0, 0, 1],
        [1, 1, 5, 1, 1, 1, 1, 1, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0],
        [1, 1, 3, 0, 0, 1, 0, 1, 0, 0, 0, 1],
        [0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 0, 0],
        [0, 0, 3, 0, 0, 0, 0, 0, 1, 0, 1, 0],
        [1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 0, 0],
        [0, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0],
        [1, 1, 2, 1, 1, 1, 1, 1, 1, 0, 0, 1],
        [1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0],
        [0, 0, 1, 0, 0, 0, 1, 0, 1, 1, 0, 0],
        [1, 1, 3, 0, 0, 1, 0, 1, 1, 0, 0, 1],
        [0, 0, 5, 0, 0, 0, 1, 0, 1, 1, 0, 0],
        [1, 1, 5, 0, 0, 1, 0, 1, 0, 0, 0, 0],
        [0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0],
        [1, 1, 5, 1, 0, 1, 0, 1, 0, 0, 0, 0],
        [0, 0, 3, 1, 0, 0, 0, 0, 1, 0, 1, 1],
        [0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 5, 0, 1, 1, 0, 1, 0, 0, 1, 0],
        [0, 0, 4, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 1, 2, 0, 0, 1, 0, 1, 1, 0, 0, 1],
        [0, 0, 3, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 2, 0, 1, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 5, 1, 1, 1, 1, 1, 0, 1, 0, 1],
        [0, 0, 5, 1, 0, 0, 0, 0, 1, 0, 1, 0],
        [1, 1, 5, 0, 0, 1, 0, 1, 0, 0, 0, 0],
        [1, 1, 1, 1, 0, 1, 0, 1, 0, 1, 1, 0],
        [0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 5, 0, 0, 0, 0, 0, 1, 0, 1, 0]
    ],
        columns=["exc_goal_diet", "exc_goal_healthy",  "experience_level", "exc_type_lower_weight", "exc_type_upper_weight", "exc_type_all_weight",
                 "exc_type_cardio", "noise_considered", "knee_health_considered", "neck_shoulder_focused", "long_sitter", "back_disk_considered"]
    )
