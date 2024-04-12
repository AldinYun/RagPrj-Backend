import openai
import google.generativeai as genai

# OpenAI API 키 설정
openai.api_key = ''
# Gemini API 키 설정
genai.configure(api_key='')

def ask_openai_gpt(question):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0125",  # GPT-3.5 Turbo 모델 사용
        messages=[{"role": "user", "content": question}]
    )
    return response.choices[0].message['content']


def ask_gemini(question):
    model = genai.GenerativeModel('gemini-pro')
    chat = model.start_chat(history=[]
    )
    response = chat.send_message(question)
    return response.text
