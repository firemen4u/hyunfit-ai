from pydantic import BaseModel
from typing import Optional


class GptMemberDto(BaseModel):
    mbrName: Optional[str] = ""
    mbrPastPtCount: Optional[int] = 0
    mbrGender: Optional[int] = 0
    mbrHeight: Optional[int] = 0
    mbrWeight: Optional[int] = 0
    mbrExerciseGoal: Optional[int] = 0
    mbrExerciseExperienceLevel: Optional[int] = 0
    mbrExerciseTarget: Optional[int] = 0
    mbrKneeHealthConsidered: Optional[int] = 0
    mbrNoiseConsidered: Optional[int] = 0
    mbrLongSitter: Optional[int] = 0
    mbrNeckShoulderFocused: Optional[int] = 0
    mbrBackDiskConsidered: Optional[int] = 0
    exerciseHistory: Optional[dict] = {}