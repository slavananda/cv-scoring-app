import requests
from bs4 import BeautifulSoup

def get_html(url: str):
    return requests.get(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, как Gecko) Chrome/58.0.3029.110 Safari/537.36"
        },
    )

def extract_vacancy_data(html):
    soup = BeautifulSoup(html, "html.parser")

    # Извлечение заголовка вакансии
    title = soup.find("h1", {"data-qa": "vacancy-title"}).text.strip()

    # Извлечение зарплаты
    salary = soup.find(
        "span", {"data-qa": "vacancy-salary-compensation-type-net"}
    ).text.strip()

    # Извлечение опыта работы
    experience = soup.find("span", {"data-qa": "vacancy-experience"}).text.strip()

    # Извлечение типа занятости и режима работы
    employment_mode = soup.find(
        "p", {"data-qa": "vacancy-view-employment-mode"}
    ).text.strip()

    # Извлечение компании
    company = soup.find("a", {"data-qa": "vacancy-company-name"}).text.strip()

    # Извлечение местоположения
    location = soup.find("p", {"data-qa": "vacancy-view-location"}).text.strip()

    # Извлечение описания вакансии
    description = soup.find("div", {"data-qa": "vacancy-description"}).text.strip()

    # Извлечение ключевых навыков
    skills = [
        skill.text.strip()
        for skill in soup.find_all(
            "div", {"class": "magritte-tag__label___YHV-o_3-0-3"}
        )
    ]

    # Формирование строки в формате Markdown
    markdown = """
# {}

**Компания:** {}
**Зарплата:** {}
**Опыт работы:** {}
**Тип занятости и режим работы:** {}
**Местоположение:** {}

## Описание вакансии
{}

## Ключевые навыки
- {}
""".format(
        title,
        company,
        salary,
        experience,
        employment_mode,
        location,
        description,
        "\n- ".join(skills)
    )

    return markdown.strip()

def extract_candidate_data(html):
    soup = BeautifulSoup(html, 'html.parser')

    # Извлечение основных данных кандидата
    name = soup.find('h2', {'data-qa': 'bloko-header-1'}).text.strip()
    gender_age = soup.find('p').text.strip()
    location = soup.find('span', {'data-qa': 'resume-personal-address'}).text.strip()
    job_title = soup.find('span', {'data-qa': 'resume-block-title-position'}).text.strip()
    job_status = soup.find('span', {'data-qa': 'job-search-status'}).text.strip()

    # Извлечение опыта работы
    experience_section = soup.find('div', {'data-qa': 'resume-block-experience'})
    experience_items = experience_section.find_all('div', class_='resume-block-item-gap')
    experiences = []
    for item in experience_items:
        period = item.find('div', class_='bloko-column_s-2').text.strip()
        duration = item.find('div', class_='bloko-text').text.strip()
        period = period.replace(duration, " ({})".format(duration))

        company = item.find('div', class_='bloko-text_strong').text.strip()
        position = item.find('div', {'data-qa': 'resume-block-experience-position'}).text.strip()
        description = item.find('div', {'data-qa': 'resume-block-experience-description'}).text.strip()
        experiences.append("**{}**\n\n*{}*\n\n**{}**\n\n{}\n".format(period, company, position, description))

    # Извлечение ключевых навыков
    skills_section = soup.find('div', {'data-qa': 'skills-table'})
    skills = [skill.text.strip() for skill in skills_section.find_all('span', {'data-qa': 'bloko-tag__text'})]

    # Формирование строки в формате Markdown
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



