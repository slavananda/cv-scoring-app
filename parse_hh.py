import requests
from bs4 import BeautifulSoup

def get_html(url: str):
    response = requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
        },
    )
    response.raise_for_status()
    return response

def extract_vacancy_data(html):
    soup = BeautifulSoup(html, "html.parser")

    def get_text_or_none(selector):
        element = soup.select_one(selector)
        return element.text.strip() if element else "Не найдено"

    title = get_text_or_none("h1[data-qa='vacancy-title']")
    salary = get_text_or_none("span[data-qa='vacancy-salary-compensation-type-net']")
    experience = get_text_or_none("span[data-qa='vacancy-experience']")
    employment_mode = get_text_or_none("p[data-qa='vacancy-view-employment-mode']")
    company = get_text_or_none("a[data-qa='vacancy-company-name']")
    location = get_text_or_none("p[data-qa='vacancy-view-location']")
    description = get_text_or_none("div[data-qa='vacancy-description']")
    skills_elements = soup.select("div.magritte-tag__label___YHV-o_3-0-3")
    skills = [skill.text.strip() for skill in skills_elements] if skills_elements else []

    markdown = """
# {title}

**Компания:** {company}
**Зарплата:** {salary}
**Опыт работы:** {experience}
**Тип занятости и режим работы:** {employment_mode}
**Местоположение:** {location}

## Описание вакансии
{description}

## Ключевые навыки
- {skills}
""".format(
        title=title,
        company=company,
        salary=salary,
        experience=experience,
        employment_mode=employment_mode,
        location=location,
        description=description,
        skills='\n- '.join(skills)
    )

    return markdown.strip()

def extract_candidate_data(html):
    soup = BeautifulSoup(html, 'html.parser')

    def get_text_or_none(selector):
        element = soup.select_one(selector)
        return element.text.strip() if element else "Не найдено"

    name = get_text_or_none('h2[data-qa="bloko-header-1"]')
    gender_age = get_text_or_none('p')
    location = get_text_or_none('span[data-qa="resume-personal-address"]')
    job_title = get_text_or_none('span[data-qa="resume-block-title-position"]')
    job_status = get_text_or_none('span[data-qa="job-search-status"]')

    experience_section = soup.select_one('div[data-qa="resume-block-experience"]')
    experience_items = experience_section.find_all('div', class_='resume-block-item-gap') if experience_section else []
    experiences = []
    for item in experience_items:
        period = item.find('div', class_='bloko-column_s-2').text.strip()
        duration = item.find('div', class_='bloko-text').text.strip()
        period = period.replace(duration, " ({})".format(duration))

        company = item.find('div', class_='bloko-text_strong').text.strip()
        position = item.find('div', {'data-qa': 'resume-block-experience-position'}).text.strip()
        description = item.find('div', {'data-qa': 'resume-block-experience-description'}).text.strip()
        experiences.append("**{}**\n\n*{}*\n\n**{}**\n\n{}\n".format(period, company, position, description))

    skills_section = soup.select_one('div[data-qa="skills-table"]')
    skills = [skill.text.strip() for skill in skills_section.find_all('span', {'data-qa': 'bloko-tag__text'})] if skills_section else []

    markdown = "# {}\n\n".format(name)
    markdown += "**{}**\n\n".format(gender_age)
    markdown += "**Местоположение:** {}\n\n".format(location)
    markdown += "**Должность:** {}\n\n".format(job_title)
    markdown += "**Статус:** {}\n\n".format(job_status)
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

