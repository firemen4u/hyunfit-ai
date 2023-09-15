import requests
from urllib import parse
import config
from .member_dto import Member
import pandas as pd


def url_of(endpoint: str):
    return parse.urljoin(config.BACKEND_API_URL, endpoint)


def get_member(mbrId: str, header: str) -> Member:
    url = url_of(f'/members/{mbrId}')
    try:
        member = requests.get(url, headers=header).json()
        print('member', member)
        print("type ", type(member))
        validated = Member.model_validate(member)

        print('validated', validated)
        return validated
    except Exception as e:
        print("Error")
        raise e


def get_dummy_data():
    return pd.DataFrame([
        [1, 0, 0, 1, 1, 0, 1, 0, 1],
        [0, 1, 0, 1, 0, 1, 0, 1, 0],
        [0, 0, 1, 1, 1, 1, 1, 0, 0],
        [1, 0, 0, 1, 0, 1, 1, 0, 0],
        [0, 0, 0, 2, 0, 1, 0, 0, 0],
        [0, 1, 0, 3, 1, 0, 1, 1, 0],
        [0, 0, 1, 3, 0, 1, 0, 0, 1],
        [0, 0, 0, 4, 1, 0, 0, 1, 0],
        [0, 0, 0, 5, 1, 1, 1, 0, 0],
        [1, 0, 0, 1, 0, 0, 1, 0, 0],
        [0, 1, 0, 3, 0, 0, 0, 1, 0],
        [1, 0, 0, 1, 1, 1, 0, 0, 1],
        [0, 0, 1, 3, 0, 0, 0, 0, 0],
        [1, 0, 0, 4, 1, 0, 1, 0, 0],
        [0, 0, 0, 2, 1, 1, 0, 0, 0],
        [0, 0, 0, 5, 0, 0, 1, 1, 0],
        [0, 0, 1, 2, 0, 1, 0, 0, 1],
        [0, 0, 0, 2, 1, 1, 0, 0, 0],
        [1, 0, 0, 5, 0, 1, 1, 0, 1],
        [0, 0, 0, 2, 0, 0, 0, 0, 0],
        [0, 1, 0, 1, 1, 0, 1, 0, 0],
        [0, 0, 0, 2, 0, 1, 1, 0, 1],
        [0, 1, 0, 3, 1, 0, 1, 1, 0],
        [0, 0, 1, 1, 1, 0, 1, 0, 0],
        [1, 0, 0, 5, 0, 1, 0, 0, 0],
        [0, 0, 0, 3, 0, 0, 0, 0, 1],
        [0, 0, 0, 1, 0, 1, 1, 0, 0],
        [0, 1, 0, 1, 0, 0, 1, 0, 0],
        [0, 0, 1, 5, 1, 0, 1, 0, 0],
        [1, 0, 0, 2, 1, 0, 0, 1, 0],
        [1, 0, 0, 5, 0, 0, 1, 0, 0],
        [0, 1, 0, 4, 1, 1, 0, 0, 1],
        [1, 1, 1, 5, 1, 0, 0, 0, 0],
        [0, 0, 0, 1, 1, 0, 0, 1, 0],
        [0, 0, 0, 3, 1, 0, 0, 0, 1],
        [0, 1, 1, 1, 0, 1, 1, 0, 0],
        [0, 0, 0, 3, 0, 1, 0, 1, 0],
        [1, 0, 0, 1, 1, 0, 1, 0, 0],
        [0, 1, 0, 1, 0, 1, 0, 0, 0],
        [1, 1, 1, 2, 1, 1, 0, 0, 1],
        [0, 0, 0, 1, 1, 0, 1, 0, 0],
        [1, 0, 0, 1, 0, 1, 1, 0, 0],
        [0, 0, 0, 3, 1, 1, 0, 0, 1],
        [1, 0, 0, 5, 0, 1, 1, 0, 0],
        [0, 0, 0, 5, 1, 0, 0, 0, 0],
        [1, 0, 0, 1, 0, 1, 0, 1, 0],
        [0, 1, 0, 5, 1, 0, 0, 0, 0],
        [0, 1, 0, 3, 0, 1, 0, 1, 1],
        [0, 0, 0, 2, 0, 0, 0, 0, 0],
        [0, 0, 1, 5, 1, 0, 0, 1, 0],
        [1, 0, 0, 4, 0, 0, 0, 0, 1],
        [0, 0, 0, 2, 1, 1, 0, 0, 1],
        [0, 1, 0, 3, 0, 0, 0, 0, 0],
        [0, 0, 1, 2, 0, 0, 0, 0, 1],
        [1, 1, 1, 5, 1, 0, 1, 0, 1],
        [0, 1, 0, 5, 0, 1, 0, 1, 0],
        [0, 0, 0, 5, 1, 0, 0, 0, 0],
        [0, 1, 0, 1, 1, 0, 1, 1, 0],
        [0, 0, 0, 3, 0, 0, 0, 0, 0],
        [0, 0, 0, 5, 0, 1, 0, 1, 0]
    ],
        columns=["exc_type_cardio", "exc_type_lower_weight", "exc_type_upper_weight", "experience_level",
                 "noise_consideration", "knee_health_considered", "neck_shoulder_focused", "long_sitter", "has_back_disk"]
    )
