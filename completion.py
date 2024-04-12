import openai

# OpenAI API 키 설정
openai.api_key = ''


def ask_openai_gpt(question):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0125",  # GPT-3.5 Turbo 모델 사용
        messages=[{"role": "user", "content": question}]
    )
    return response.choices[0].message['content']


#print(ask_openai_gpt('안녕하세요'))
