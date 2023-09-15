from fastapi import FastAPI, Header
from typing import Annotated
import openai
import config
import gpt
import amber

openai.api_key = config.OPENAI_API_KEY  # 여기에 실제 API 키를 입력하시거나 외부에서 불러오십시오.

app = FastAPI()


@app.post("/generate_fitness_report1/")
async def generate_report(data: gpt.GptData):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a health trainer"
            },
            {
                "role": "user",
                "content": data.content
            },
            {
                "role": "assistant",
                "content": ""
            }
        ],
        temperature=1,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    ai_message = response.choices[0].message['content']
    return {"ai_message": ai_message}


@app.get("/recommendations/{mbrId}")
async def get_routine_recommendations(mbrId: str, authorization: Annotated[str | None, Header()] = None):
    header = {"Authorization": authorization} if authorization else None
    member = amber.api.get_member(mbrId, header)
    return amber.recommender.routine_recommendations(member)


# FastAPI 앱 실행
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
