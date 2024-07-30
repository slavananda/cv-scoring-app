import requests
from bs4 import BeautifulSoup

def get_html(url: str):
    response = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        },
    )
    return response

def extract_vacancy_data(html):
    soup = BeautifulSoup(html, "html.parser")

    title = soup.find("h1", {"data-qa": "vacancy-title"})
    title = title.text.strip() if title else "Не найдено"

    salary = soup.find("span", {"data-qa": "vacancy-salary-compensation-type-net"})
    salary = salary.text.strip() if salary else "Не найдено"

    experience = soup.find("span", {"data-qa": "vacancy-experience"})
    experience = experience.text.strip() if experience else "Не найдено"

    employment_mode = soup.find("p", {"data-qa": "vacancy-view-employment-mode"})
    employment_mode = employment_mode.text.strip() if employment_mode else "Не найдено"

    company = soup.find("a", {"data-qa": "vacancy-company-name"})
    company = company.text.strip() if company else "Не найдено"

    location = soup.find("p", {"data-qa": "vacancy-view-location"})
    location = location.text.strip() if location else "Не найдено"

    description = soup.find("div", {"data-qa": "vacancy-description"})
    description = description.text.strip() if description else "Не найдено"

    skills = [skill.text.strip() for skill in soup.find_all("div", {"class": "magritte-tag__label___YHV-o_3-0-3"})]

    markdown = f"""
# {title}

**Компания:** {company}
**Зарплата:** {salary}
**Опыт работы:** {experience}
**Тип занятости и режим работы:** {employment_mode}
**Местоположение:** {location}

## Описание вакансии
{description}

## Ключевые навыки
- {chr(10).join(skills)}
"""

    return markdown.strip()

def extract_candidate_data(html):
    soup = BeautifulSoup(html, 'html.parser')

    name = soup.find('h2', {'data-qa': 'bloko-header-1'})
    name = name.text.strip() if name else "Не найдено"

    gender_age = soup.find('p')
    gender_age = gender_age.text.strip() if gender_age else "Не найдено"

    location = soup.find('span', {'data-qa': 'resume-personal-address'})
    location = location.text.strip() if location else "Не найдено"

    job_title = soup.find('span', {'data-qa': 'resume-block-title-position'})
    job_title = job_title.text.strip() if job_title else "Не найдено"

    job_status = soup.find('span', {'data-qa': 'job-search-status'})
    job_status = job_status.text.strip() if job_status else "Не найдено"

    experience_section = soup.find('div', {'data-qa': 'resume-block-experience'})
    experience_items = experience_section.find_all('div', class_='resume-block-item-gap') if experience_section else []
    experiences = []
    for item in experience_items:
        period = item.find('div', class_='bloko-column_s-2')
        duration = item.find('div', class_='bloko-text')
        period_text = period.text.strip() if period else "Не найдено"
        duration_text = duration.text.strip() if duration else "Не найдено"
        period_text = period_text.replace(duration_text, f" ({duration_text})")

        company = item.find('div', class_='bloko-text_strong')
        company_text = company.text.strip() if company else "Не найдено"

        position = item.find('div', {'data-qa': 'resume-block-experience-position'})
        position_text = position.text.strip() if position else "Не найдено"

        description = item.find('div', {'data-qa': 'resume-block-experience-description'})
        description_text = description.text.strip() if description else "Не найдено"

        experiences.append(f"**{period_text}**\n\n*{company_text}*\n\n**{position_text}**\n\n{description_text}\n")

    skills_section = soup.find('div', {'data-qa': 'skills-table'})
    skills = [skill.text.strip() for skill in skills_section.find_all('span', {'data-qa': 'bloko-tag__text'})] if skills_section else []

    markdown = f"# {name}\n\n"
    markdown += f"**{gender_age}**\n\n"
    markdown += f"**Местоположение:** {location}\n\n"
    markdown += f"**Должность:** {job_title}\n\n"
    markdown += f"**Статус:** {job_status}\n\n"
    markdown += "## Опыт работы\n\n"
    for exp in experiences:
        markdown += exp + "\n"
    markdown += "## Ключевые навыки\n\n"
    markdown += ', '.join(skills) + "\n"

    return markdown

def get_candidate_info(url: str):
    response = get_html(url)
    return extract_candidate_data(response.text)

def get_job_description(url: str):
    response = get_html(url)
    return extract_vacancy_data(response.text)
