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

    system_text = f'''당신은 유능한 헬스트레이너입니다. 당신이 담당하는 회원의 이름은 {name}, 이번달 퍼스널 트레이닝을 받은 횟수는 {pt_count}회. {name}의 성별은 {gender}, 키는 {height}cm, 몸무게는 {weight}kg.
{name}님의 운동 능력은 {level}이고, 목표로 하는 것은 {goal} 입니다. 주로 운동하는 부위는 {target} 입니다. {name}님의 고려 사항은 다음과 같습니다 : {consider}
{name}님의 이번 달 운동 시간: {round(timeInSeconds/60)}분.
소모한 총 칼로리: {calories}Kcal.
운동 기록의 정확도는 {accuracy}.
이번 달 출석일수: {len(member_filtered_daily_records)}일
이번 달에 가장 많이 운동한 부위: {','.join(top3_target)}'''

    t1 = time.time()
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": system_text
            },
            {
                "role": "user",
                "content": '''현재 회원의 운동기록에 대한 피드백과 앞으로 나아가야할 운동 방향을 보고서 형식으로 제시. 1. 키와 몸무게에 대해 건강관련 평가. 2. 본론의 형식은 운동 결과에 대한 피드백을 주세요. 결론으로는 앞으로 나아갈 운동방향에 대해 회원의 운동목표에 맞는 운동, 식단 추천을 해주고
다음달에는 어떤식으로 운동을 진행하면 좋을지 작성하며 마무리해주세요.
'''
            },
            {
                "role": "assistant",
                "content": ""
            }

        ],
        temperature=1,
        max_tokens=2000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    ai_message = response.choices[0].message['content']
    return {"ai_message": ai_message, "time_taken": time.time()-t1}


@app.post("/recommendations")
async def get_routine_recommendations(member: amber.Member):
    return amber.recommender.routine_recommendations(member)

# FastAPI 앱 실행
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
