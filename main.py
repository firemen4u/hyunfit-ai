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
    member_filtered_daily_records = []
    # 필터링
    for record in data.exerciseHistory['dailyRecords']:
        timestamp_in_ms = record['day']
        timestamp_in_s = timestamp_in_ms // 1000  # 밀리세컨드를 초로 변환
        normal_date = datetime.fromtimestamp(timestamp_in_s).strftime('%Y-%m-%d')

        calories = record['calories']

        member_filtered_daily_records.append({'운동한 날짜': normal_date, '날짜에 소모한 칼로리': calories})

    targets = {target_mapping[item['targetArea']]: item['totalCalories'] for item in exercise_targets}
    targets = sorted(targets.items(), key=lambda x: x[1], reverse=True)

    top3_target = [t[0] for t in targets[:2]]

    messages = [
        {
            "role": "system",
            "content": "당신은 헬스트레이너입니다."
        },
        {
            "role": "system",
            "content": f'''{name}회원의 10월 홈트레이닝 기록을 보고 다음 형식에 맞춰 응답. 600자 제한.
- 권장하는 홈트레이닝 습관
- 목표에 맞는 홈트레이닝 운동과 식단 추천'''
        },
        {
            "role": "user",
            "content": f'''인적사항: 운동 능력={level}, 운동 목표={goal}, 고려 사항={consider}. 
                10월 운동기록: personal training 횟수={pt_count}, 운동한 부위={target}-{",".join(top3_target)}, 운동시간={round(timeInSeconds/60)}분, 소모칼로리={calories}Kcal, 운동정확도={accuracy}, 출석일수={len(member_filtered_daily_records)}'''
        },
        {
            "role": "assistant",
            "content": ""
        }

    ]
    t1 = time.time()
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages,
        temperature=0.3,
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
