import os
import openai
import streamlit as st
from parse_hh import get_candidate_info, get_job_description

# Установка API ключа из переменной окружения
api_key = os.getenv("OPENAI_API_KEY")
if api_key is None:
    raise ValueError("API key is not set. Please set the OPENAI_API_KEY environment variable.")

client = openai.Client(api_key=api_key)

SYSTEM_PROMPT = """
Проскорь кандидата, насколько он подходит для данной вакансии.

Сначала напиши короткий анализ, который будет пояснять оценку.
Отдельно оцени качество заполнения резюме (понятно ли, с какими задачами сталкивался кандидат и каким образом их решал?). Эта оценка должна учитываться при выставлении финальной оценки - нам важно нанимать таких кандидатов, которые могут рассказать про свою работу
Потом представь результат в виде оценки от 1 до 10.
""".strip()

def request_gpt(system_prompt, user_prompt):
    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=1000,
            temperature=0,
        )
        return response.choices[0].message.content
    except Exception as e:
        st.error(f"Ошибка при запросе к OpenAI API: {e}")
        return None

st.title("CV Scoring App")

job_description_url = st.text_area("Enter the job description URL")

cv_url = st.text_area("Enter the CV URL")

if st.button("Score CV"):
    with st.spinner("Scoring CV..."):
        try:
            job_description = get_job_description(job_description_url)
            cv = get_candidate_info(cv_url)

            st.write("Job description:")
            st.write(job_description)
            st.write("CV:")
            st.write(cv)

            user_prompt = "# ВАКАНСИЯ\n{}\n\n# РЕЗЮМЕ\n{}".format(job_description, cv)
            response = request_gpt(SYSTEM_PROMPT, user_prompt)

            if response:
                st.write(response)
            else:
                st.error("Не удалось получить ответ от OpenAI API.")
        except Exception as e:
            st.error(f"Ошибка при обработке данных: {e}")
