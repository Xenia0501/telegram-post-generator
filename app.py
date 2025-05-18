import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import openai

app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    raise ValueError("Требуется переменная окружения OPENAI_API_KEY")

class Topic(BaseModel):
    topic: str

def generate_post(topic: str):
    try:
        # Заголовок
        prompt_title = f"Придумайте привлекательный заголовок для поста на тему: {topic}"
        title_resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt_title}],
            max_tokens=60,
            temperature=0.7
        )
        title = title_resp.choices[0].message.content.strip()

        # Мета-описание
        prompt_meta = f"Напишите краткое мета-описание для поста с заголовком: {title}"
        meta_resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt_meta}],
            max_tokens=120,
            temperature=0.7
        )
        meta = meta_resp.choices[0].message.content.strip()

        # Пост
        prompt_post = f"Напишите подробный пост на тему: {topic}. Используйте короткие абзацы, подзаголовки, ключевые слова и примеры."
        post_resp = openai.ChatCompletion.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt_post}],
            max_tokens=1500,
            temperature=0.7
        )
        content = post_resp.choices[0].message.content.strip()

        return {
            "title": title,
            "meta_description": meta,
            "post_content": content
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-post")
async def generate_post_api(data: Topic):
    return generate_post(data.topic)

@app.get("/")
def root():
    return {"message": "Сервис работает"}
