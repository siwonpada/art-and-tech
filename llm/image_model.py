from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()


def make_image(emotion):
    response = client.images.generate(
        model="dall-e-3",
        prompt=f"다음 감정을 가지고 있는 인공지능의 이미지를 그려줘. {emotion}",
        size="1024x1024",
        quality="standard",
        n=1,
    )
    return response.data[0].url
