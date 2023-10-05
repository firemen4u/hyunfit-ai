from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import openai
import config
from gpt import GptMemberDto
import amber
import time

openai.api_key = config.OPENAI_API_KEY

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/generate_fitness_report/")
async def generate_report(data: GptMemberDto):
    # print(data)
    name = data.mbrName
    pt_count = data.mbrPastPtCount
    gender = {0: "중성", 1: "남성", 2: "여성"}[int(data.mbrGender)]
    goal = {1: "체중 관리", 2: "건강 관리"}[data.mbrExerciseGoal]
    height = data.mbrHeight
    weight = data.mbrWeight
    level = {1: "초보", 2: "초중급", 3: "중급", 4: "중고급", 5: "고급"}[data.mbrExerciseExperienceLevel]
    target = {1: "상체", 2: "하체", 3: "전신", 4: "유산소", 5: "상관없음"}[data.mbrExerciseTarget]

    # 고려사항
    health_conditions = []
    if data.mbrKneeHealthConsidered:
        health_conditions.append("무릎 건강을 고려")
    if data.mbrNoiseConsidered:
        health_conditions.append("층간 소음을 고려")
    if data.mbrLongSitter:
        health_conditions.append("장시간 앉아있는 사람")
    if data.mbrNeckShoulderFocused:
        health_conditions.append("목/어깨에 집중된 운동을 원함")
    if data.mbrBackDiskConsidered:
        health_conditions.append("허리 디스크가 있음")
    consider = ", ".join(health_conditions)

    # 해당 월에 운동한 동작의 정확도
    excellent_count = data.exerciseHistory['totalExcellentCount']
    good_count = data.exerciseHistory['totalGoodCount']
    bad_count = data.exerciseHistory['totalBadCount']
    accuracy = {'excellent': excellent_count, 'good': good_count, 'bad': bad_count}
    # 해당 월에 운동한 부위
    exercise_targets = data.exerciseHistory['exerciseTargets']
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

    mapped_target = [
        {
            "운동 타겟부위": target_mapping[item['targetArea']],
            "타겟부위 소모한 칼로리": item['totalCalories']
        }
        for item in exercise_targets
    ]

    timeInSeconds = data.exerciseHistory['totalExerciseTimeSeconds']
    calories = data.exerciseHistory['totalCalories']

    # 해당월의 날짜 별 기록
    daily_records = data.exerciseHistory['dailyRecords']
    member_filtered_daily_records = []
    # 필터링
    for record in daily_records:
        timestamp_in_ms = record['day']
        timestamp_in_s = timestamp_in_ms // 1000  # 밀리세컨드를 초로 변환
        normal_date = datetime.fromtimestamp(timestamp_in_s).strftime('%Y-%m-%d')

        calories = record['calories']

        member_filtered_daily_records.append({'운동한 날짜': normal_date, '날짜에 소모한 칼로리': calories})

    targets = {target_mapping[item['targetArea']]: item['totalCalories'] for item in exercise_targets}
    targets = sorted(targets.items(), key=lambda x: x[1], reverse=True)

    top3_target = [t[0] for t in targets[:2]]

    system_text = f'''당신은 헬스트레이너입니다. 회원이름:{name}, 이번달 personal training을 받은 횟수:{pt_count}회.
{name}의 성별,키,몸무게: {gender},{height}cm,{weight}kg.
운동 능력:{level}
운동 목표:{goal}
고려 사항:{consider}
한달 간 운동한 부위:{target}
이번 달 운동 시간:{round(timeInSeconds/60)}분.
소모한 총 칼로리:{calories}Kcal.
운동 기록의 정확도:{accuracy}.
이번 달 출석일수:{len(member_filtered_daily_records)}일
이번 달 많이 운동한 부위:{','.join(top3_target)}'''


    t1 = time.time()
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": system_text
            },
            {
                "role": "user",
                "content": '''현재 회원의 운동기록입니다. 아래형태로 간단히 대답해주세요.
1. 키와 몸무게에 대해 건강관련 평가. : BMI 지수
2. 운동 결과에 대한 피드백. : 정확도에 대한 평가(좋음, 나쁨) / BMI 지수에 따른 칼로리 소모량
3. 앞으로 나아갈 운동방향에 대해 회원의 운동목표에 맞는 운동, 식단 추천
응답을 500자 내외로 제한합니다.
'''
            },
            {
                "role": "assistant",
                "content": ""
            }

        ],
        temperature=0.1,
        max_tokens=700,
        top_p=0.9
    )

    ai_message = response.choices[0].message['content']
    return {"ai_message": ai_message, "time_taken": time.time()-t1}


@app.post("/recommendations")
async def get_routine_recommendations(member: amber.Member):
    return amber.recommender.routine_recommendations(member)

# FastAPI 앱 실행
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, timeout_keep_alive=120)
