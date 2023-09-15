from pydantic import BaseModel, validator
from typing import Optional


class Member(BaseModel):
    mbrExerciseGoal: Optional[int] = 0
    mbrExerciseExperienceLevel: Optional[int] = 0
    mbrExercisePreference: Optional[int] = 0
    mbrKneeHealth: Optional[int] = 0
    mbrNoiseConsideration: Optional[int] = 0
    mbrLongSitter: Optional[int] = 0
    mbrNeckShoulderFocused: Optional[int] = 0
    hasBackDisk: Optional[int] = 0

    @validator('mbrExerciseGoal', 'mbrExercisePreference', 'mbrKneeHealth', 'mbrNoiseConsideration', 'mbrLongSitter', 'mbrNeckShoulderFocused', 'hasBackDisk', pre=True, always=True)
    def set_zero_if_none(cls, value):
        return value if value is not None else 0

    @validator('mbrExerciseExperienceLevel', pre=True, always=True)
    def set_one_if_none(cls, value):
        print(cls)
        return value if value is not None else 1
