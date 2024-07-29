import streamlit as st
from parse_hh import get_candidate_info, get_job_description

st.title("CV Scoring App")

job_description_url = st.text_input("Введите URL описания вакансии:")
if job_description_url:
    job_description = get_job_description(job_description_url)
    st.markdown(job_description)

candidate_info_url = st.text_input("Введите URL резюме кандидата:")
if candidate_info_url:
    candidate_info = get_candidate_info(candidate_info_url)
    st.markdown(candidate_info)



