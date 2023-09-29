
from pydantic import BaseModel

class Routine(BaseModel):
    rtnSeq: int
    rtnName: str
    rtnContent: str
    rtnTarget: int
    rtnDuration: int
    rtnExperienceLevel: int
    rtnGoal: int
    rtnKneeHealthConsidered: int
    rtnNoiseConsidered: int
    rtnLongSitter: int
    rtnNeckShoulderFocused: int
    rtnBackDiskConsidered: int
    rtnRewardPoint: int