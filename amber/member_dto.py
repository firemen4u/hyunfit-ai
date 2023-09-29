from pydantic import BaseModel, validator
from typing import Optional


class Member(BaseModel):
    mbrExerciseGoal: Optional[int] = 0
    mbrExerciseExperienceLevel: Optional[int] = 0
    mbrExerciseTarget: Optional[int] = 0
    mbrKneeHealthConsidered: Optional[int] = 0
    mbrNoiseConsidered: Optional[int] = 0
    mbrNeckShoulderFocused: Optional[int] = 0
    mbrLongSitter: Optional[int] = 0
    mbrBackDiskConsidered: Optional[int] = 0

    @validator('mbrExerciseGoal', 'mbrExerciseTarget', 'mbrKneeHealthConsidered', 'mbrNoiseConsidered', 'mbrLongSitter', 'mbrNeckShoulderFocused', 'mbrBackDiskConsidered', pre=True, always=True)
    def set_zero_if_none(cls, value):
        return value if value is not None else 0

    @validator('mbrExerciseExperienceLevel', pre=True, always=True)
    def set_one_if_none(cls, value):
        return value if value is not None else 1
