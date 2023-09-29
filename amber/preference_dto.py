from pydantic import BaseModel
from .member_dto import Member


class Preference(BaseModel):
    exc_goal_diet: int = 0
    exc_goal_healthy: int = 0
    experience_level: int = 1
    exc_type_upper_weight: int = 0
    exc_type_lower_weight: int = 0
    exc_type_all_weight: int = 0
    exc_type_cardio: int = 0
    noise_considered: int = 0  # 층별 수음 주의
    knee_health_considered: int = 0  # 무릎운동 안됨
    neck_shoulder_focused: int = 0  # 목과 어깨 위주로 운동
    long_sitter: int = 0  # 앉아있는 시간이 김
    back_disk_considered: int = 0  # 허리디스크 있음

    @staticmethod
    def from_member(member: Member):
        return Preference(
            exc_goal_diet=member.mbrExerciseGoal in [0, 1],
            exc_goal_healthy=member.mbrExerciseGoal in [0, 2],
            experience_level=member.mbrExerciseExperienceLevel,
            exc_type_lower_weight=member.mbrExerciseTarget in [0, 1],
            exc_type_upper_weight=member.mbrExerciseTarget in [0, 2],
            exc_type_all_weight=member.mbrExerciseTarget in [0, 3],
            exc_type_cardio=member.mbrExerciseTarget in [0, 4],
            knee_health_considered=member.mbrKneeHealthConsidered,
            noise_considered=member.mbrNoiseConsidered,
            neck_shoulder_focused=member.mbrNeckShoulderFocused,
            long_sitter=member.mbrLongSitter,
            back_disk_considered=member.mbrBackDiskConsidered
        )
