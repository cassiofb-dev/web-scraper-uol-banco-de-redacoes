import copy

import json

import pprint

import requests

from bs4 import BeautifulSoup

PAGES_TO_SCRAP = [
    'https://educacao.uol.com.br/bancoderedacoes/propostas/carnaval-e-apropriacao-cultural.htm',
    'https://educacao.uol.com.br/bancoderedacoes/propostas/qualificacao-e-o-futuro-do-emprego.htm',
    'https://educacao.uol.com.br/bancoderedacoes/propostas/supremo-tribunal-federal-e-opiniao-publica.htm',
    'https://educacao.uol.com.br/bancoderedacoes/propostas/ciencia-tecnologia-e-superacao-dos-limites-humanos.htm',
    'https://educacao.uol.com.br/bancoderedacoes/propostas/um-reu-deve-ou-nao-ser-preso-apos-a-condenacao-em-2-instancia.htm',
    'https://educacao.uol.com.br/bancoderedacoes/propostas/agrotoxicos-ou-defensivos-agricolas-dois-nomes-e-uma-polemica.htm',
    'https://educacao.uol.com.br/bancoderedacoes/propostas/preservacao-da-amazonia-desafio-brasileiro-ou-internacional.htm',
    'https://educacao.uol.com.br/bancoderedacoes/propostas/criptomoeda-tecnologia-e-revolucao-economica.htm',
    'https://educacao.uol.com.br/bancoderedacoes/propostas/a-ciencia-na-era-da-pos-verdade.htm',
]

HTML_PARSER = 'html.parser'

ESSAY_SELECTOR = '.text-composition'

POINTS_SELECTOR = '.points'

ESSAY_LIST_SELECTOR = '.rt-body'

def scrap_essay_page(href, essays):
    reponse = requests.get(href)

    html_string = reponse.text

    soup = BeautifulSoup(html_string, HTML_PARSER)

    essay_element = soup.select_one(ESSAY_SELECTOR)

    original_essay_element = copy.copy(essay_element)

    correction_elements = original_essay_element.find_all(attrs={'style' : 'color:#00b050'})

    for element in correction_elements:
        element.decompose()

    original_essay_text = original_essay_element.get_text()

    corrected_essay_element = copy.copy(essay_element)

    wrong_elements = corrected_essay_element.find_all('strong')

    for element in wrong_elements:
        element.decompose()

    corrected_essay_text = corrected_essay_element.get_text()

    essay_title_element = soup.select_one('.container-composition > h2:nth-child(1)')

    essay_title_text = essay_title_element.get_text()

    points_elements = soup.select(POINTS_SELECTOR)

    points_text = [element.get_text() for element in points_elements]

    essays.append({
        'title': essay_title_text,
        'original_text': original_essay_text,
        'corrected_text': corrected_essay_text,
        'points': points_text[:6],
    })

def init_scraper():
    themes = []
    essays = []

    for page in PAGES_TO_SCRAP:
        reponse = requests.get(page)

        html_string = reponse.text

        soup = BeautifulSoup(html_string, HTML_PARSER)

        essay_list = soup.select_one(ESSAY_LIST_SELECTOR)

        essay_divs = essay_list.find_all('div')

        for essay_div in essay_divs:
            href = essay_div.select_one('a')['href']

            scrap_essay_page(href, essays)

            print(f'finished scrapping essay in: {href}')

        essay_theme_element = soup.select_one('i.custom-title')

        essay_theme_text = essay_theme_element.get_text()

        themes.append({
            'theme': essay_theme_text,
            'essays': essays,
        })

        essays = []

        print(f'finished scrapping theme in: {page}')

    with open("uol_redacoes.json", "w") as text_file:
        print(json.dumps(themes, indent=4), file=text_file)

if __name__ == "__main__":
    init_scraper()
