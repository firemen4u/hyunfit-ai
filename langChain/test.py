from datetime import datetime
import json
from langchain.prompts import ChatPromptTemplate
from langchain.llms import OpenAI
from langchain.chains import LLMChain
import config

# JSON 데이터 불러오기 (실제로는 API 요청 등을 통해 받을 수 있습니다.)
json_data = '''
{
    "mbrSeq": 2,
    "mbrId": "member",
    "mbrPw": null,
    "mbrName": "우진우",
    "mbrTotalPoint": 1000,
    "mbrTotalExp": 1000,
    "mbrPastPtCount": 0,
    "mbrBirthdate": 1695373200000,
    "mbrGender": "1",
    "mbrHeight": 175,
    "mbrWeight": 65,
    "mbrExerciseGoal": 2,
    "mbrExerciseExperienceLevel": 5,
    "mbrExerciseTarget": 3,
    "mbrKneeHealthConsidered": 0,
    "mbrNoiseConsidered": 1,
    "mbrLongSitter": 1,
    "mbrNeckShoulderFocused": 0,
    "mbrBackDiskConsidered": 0,
    "mbrProfileUrl": "https://fs.hyunfit.life/api/hyunfit/file/trn_1_profile.png",
    "personalTrainingDTOList": null,
    "exerciseHistory": {
    "mbrId": null,
    "totalCalories": 683,
    "totalExerciseTimeSeconds": 2580,
    "totalExcellentCount": 173,
    "totalGoodCount": 64,
    "totalBadCount": 16,
    "exerciseTargets": [
        {
        "targetArea": 1,
        "totalCalories": 296.1
        },
        {
        "targetArea": 2,
        "totalCalories": 126.9
        }
    ],
    "exercisedDays": [
        "2023-09-24",
        "2023-09-25"
    ],
    "dailyRecords": [
        {
        "day": 1695513600000,
        "calories": 176,
        "exp": 0,
        "cumulativeExpSum": 0
        },
        {
        "day": 1695600000000,
        "calories": 531,
        "exp": 1000,
        "cumulativeExpSum": 1000
        }
    ]
    },
    "trainerFeedbacks": null,
    "trainerFeedback": null
    }
'''
parsed_json = json.loads(json_data)


# JSON 데이터에서 필요한 정보 추출
# 멤버 데이터
member_name = parsed_json['mbrName']
member_past_pt_count = parsed_json['mbrPastPtCount']
mbr_gender = parsed_json['mbrGender']
member_gender = {0: "중성", 1: "남성", 2: "여성"}[int(mbr_gender)]
member_height = parsed_json['mbrHeight']
member_weight = parsed_json['mbrWeight']
print(f'멤버 데이터 : {member_name, member_past_pt_count, member_gender, member_height, member_weight}')
# 목표
exercise_goal = parsed_json['mbrExerciseGoal']
member_exercise_goal = {1: "체중 관리", 2: "건강 관리"}[exercise_goal]
exercise_target = parsed_json['mbrExerciseTarget']
member_exercise_target = {1: "상체", 2: "하체", 3: "전신", 4: "유산소", 5: "상관없음"}[exercise_target]
mbr_experience_level = parsed_json['mbrExerciseExperienceLevel']
member_exercise_experience = {1: "초보", 2: "초중급", 3: "중급", 4: "중고급", 5: "고급"}[mbr_experience_level]
print(f'멤버 목표 : {member_exercise_goal, member_exercise_target, member_exercise_experience}')
# 멤버별 고려사항
knee_considered = parsed_json['mbrKneeHealthConsidered']
noise_considered = parsed_json['mbrNoiseConsidered']
long_sitter = parsed_json['mbrLongSitter']
neck_shoulder_focused = parsed_json['mbrNeckShoulderFocused']
back_disk_considered = parsed_json['mbrBackDiskConsidered']
# 고려사항 합치는 배열
health_conditions = []
if knee_considered: health_conditions.append("무릎 건강을 고려")
if noise_considered: health_conditions.append("층간 소음을 고려")
if long_sitter: health_conditions.append("장시간 앉아있는 사람")
if neck_shoulder_focused: health_conditions.append("목/어깨에 집중된 운동을 원함")
if back_disk_considered: health_conditions.append("허리 디스크가 있음")
member_consider_health = ", ".join(health_conditions)
print(f'멤버 별 고려 사항 : {member_consider_health}')

# 해당 월 운동 기록 배열
exercise_history = parsed_json['exerciseHistory']
# print(f'해당 월 운동 기록 배열 : {exercise_history}')
# 해당 월에 소모한 총 칼로리
total_calories = exercise_history['totalCalories']
print(f'해당 월에 소모한 총 칼로리 : {total_calories}')
# 해당 월에 운동한 총 시간 (초)
total_time = exercise_history['totalExerciseTimeSeconds']
print(f'해당 월에 운동한 총 시간 (초) : {total_time}')
# 해당 월에 운동한 동작의 정확도
excellent_count = exercise_history['totalExcellentCount']
good_count = exercise_history['totalGoodCount']
bad_count = exercise_history['totalBadCount']
print(f'해당 월에 운동한 동작의 정확도 : {excellent_count, good_count, bad_count}')
# 해당 월에 운동한 부위
exercise_targets = exercise_history['exerciseTargets']
print(f'해당 월에 운동한 부위 : {exercise_targets}')
# 운동 부위에 대한 매핑
target_mapping = {
    1: '광배근',
    2: '기립근',
    3: '대퇴사두',
    4: '대흉근',
    5: '둔근',
    6: '삼두',
    7: '승모근',
    8: '이두근',
    9: '전면어깨',
    10: '측면어깨',
    11: '코어',
    12: '햄스트링',
    13: '후면어깨'
}

mapped_exercise_targets = [
    {
        "운동 타겟부위": target_mapping[item['targetArea']],
        "타겟부위 소모한 칼로리": item['totalCalories']
    }
    for item in exercise_targets
]

print(f'매핑된 해당 월에 운동한 부위 : {mapped_exercise_targets}')

# 해당월의 날짜 별 기록
daily_records = exercise_history['dailyRecords']
print(f'날짜 별 기록 : {daily_records}')
filtered_daily_records = []
# 필터링
for record in daily_records:
    timestamp_in_ms = record['day']
    timestamp_in_s = timestamp_in_ms // 1000  # 밀리세컨드를 초로 변환
    normal_date = datetime.fromtimestamp(timestamp_in_s).strftime('%Y-%m-%d')

    calories = record['calories']

    filtered_daily_records.append({'운동한 날짜': normal_date, '날짜에 소모한 칼로리': calories})

# 변환된 데이터 확인
print(f'필터링된 데이터: {filtered_daily_records}')


# system_template 설정
# ChatPromptTemplate을 사용하여 LLM에게 역할 부여 system, human, ai
system_template = f"당신은 {member_name}님의 운동 목표를 {goal_str}로, 타겟은 {target_str}로 설정하는 헬스 트레이너입니다. 추가로 고려할 사항은 {health_str}이며, 주로 집중하는 부위는 {target_areas_str}입니다."
human_template = "{text}"

print(system_template)

# chat_prompt = ChatPromptTemplate.from_messages([
#     ("system", system_template),
#     ("human", human_template),
# ])
#
# # LLM과 LLMChain 초기화
# llm = OpenAI(openai_api_key=config.OPENAI_API_KEY)
# chain = LLMChain(llm=llm, prompt=chat_prompt)
#
# # LLMChain 실행
# result = chain.run(name=member_name, goal=exercise_goal, text="어떤 운동을 추천해주세요?")
# print(result)
