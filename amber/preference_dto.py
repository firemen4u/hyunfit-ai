from pydantic import BaseModel
from .member_dto import Member


class Preference(BaseModel):
    exc_type_cardio: int = 0
    exc_type_upper_weight: int = 0
    exc_type_lower_weight: int = 0
    experience_level: int = 1
    noise_consideration: int = 0  # 층별 수음 주의
    knee_health_considered: int = 0  # 무릎운동 안됨
    neck_shoulder_focused: int = 0  # 목과 어깨 위주로 운동
    long_sitter: int = 0  # 앉아있는 시간이 김
    has_back_disk: int = 0  # 허리디스크 있음

    @staticmethod
    def from_member(member: Member):
        return Preference(
            exc_type_cardio=member.mbrExerciseGoal in [0, 1],
            exc_type_lower_weight=member.mbrExerciseGoal in [0, 2],
            exc_type_upper_weight=member.mbrExerciseGoal in [0, 3],
            experience_level=member.mbrExerciseExperienceLevel,
            knee_health_considered=member.mbrKneeHealth,
            noise_consideration=member.mbrNoiseConsideration,
            long_sitter=member.mbrLongSitter,
            has_back_disk=0  # to do
        )
