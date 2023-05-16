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
    'https://educacao.uol.com.br/bancoderedacoes/propostas/universidade-em-crise-quem-paga-a-conta.htm',
    'https://educacao.uol.com.br/bancoderedacoes/propostas/a-fe-e-decisiva-para-uma-vida-melhor.htm',
    'https://educacao.uol.com.br/bancoderedacoes/propostas/os-ursos-polares-da-russia-e-um-dilema-ecologico.htm',
    'https://educacao.uol.com.br/bancoderedacoes/propostas/cantar-ou-nao-cantar-o-hino-nacional-eis-a-questao.htm',
    'https://educacao.uol.com.br/bancoderedacoes/propostas/posse-de-armas-mais-seguranca-ou-mais-perigo.htm',
    'https://educacao.uol.com.br/bancoderedacoes/propostas/o-brasil-e-os-imigrantes-no-mundo-contemporaneo.htm',
    'https://educacao.uol.com.br/bancoderedacoes/propostas/epidemia-alimentar-sobrepeso-e-obesidade.htm',
    'https://educacao.uol.com.br/bancoderedacoes/propostas/a-onda-conservadora-e-o-brasil-nos-proximos-anos.htm',
    'https://educacao.uol.com.br/bancoderedacoes/propostas/patrimonio-historico-e-cultural-brasileiro-um-caso-de-descaso.htm',
    'https://educacao.uol.com.br/bancoderedacoes/propostas/direitos-humanos-em-defesa-de-quem.htm',
    'https://educacao.uol.com.br/bancoderedacoes/propostas/redes-sociais-e-manipulacao-politica.htm',
    'https://educacao.uol.com.br/bancoderedacoes/propostas/por-que-os-jovens-querem-deixar-o-brasil.htm',
    'https://educacao.uol.com.br/bancoderedacoes/propostas/o-brasil-paralisado-o-que-voce-pensa-sobre-a-greve-dos-caminhoneiros.htm',
    'https://educacao.uol.com.br/bancoderedacoes/propostas/o-direito-ao-foro-privilegiado.htm',
    'https://educacao.uol.com.br/bancoderedacoes/propostas/informacao-no-rotulo-de-produtos-transgenicos.htm',
    'https://educacao.uol.com.br/bancoderedacoes/propostas/violencia-e-drogas-o-papel-do-usuario.htm',
    'https://educacao.uol.com.br/bancoderedacoes/propostas/a-terapia-de-reversao-da-orientacao-sexual.htm',
    'https://educacao.uol.com.br/bancoderedacoes/propostas/como-melhorar-a-educacao-sem-valorizar-o-professor.htm',
    'https://educacao.uol.com.br/bancoderedacoes/propostas/brasileiros-tem-pessima-educacao-argumentativa-segundo-cientista.htm',
    'https://educacao.uol.com.br/bancoderedacoes/propostas/por-que-nao-ha-novas-manifestacoes-nas-ruas.htm',
    'https://educacao.uol.com.br/bancoderedacoes/propostas/internacao-compulsoria-de-dependentes-de-crack.htm',
    'https://educacao.uol.com.br/bancoderedacoes/propostas/perigos-do-universo-digital.htm',
    'https://educacao.uol.com.br/bancoderedacoes/propostas/terceirizacao-avanco-ou-retrocesso.htm',
    'https://educacao.uol.com.br/bancoderedacoes/propostas/direitos-em-conflito-liberdade-de-expressao-e-intimidade.htm',
    'https://educacao.uol.com.br/bancoderedacoes/propostas/artes-e-educacao-fisica-opcionais-ou-obrigatorias.htm',
    'https://educacao.uol.com.br/bancoderedacoes/propostas/voce-faz-parte-da-turma-do-eu-me-acho.htm',
    'https://educacao.uol.com.br/bancoderedacoes/propostas/escola-no-brasil-com-partido-ou-sem-partido.htm',
    'https://educacao.uol.com.br/bancoderedacoes/propostas/escravizar-e-humano.htm',
    'https://educacao.uol.com.br/bancoderedacoes/propostas/estupro-como-prevenir-esse-crime.htm',
    'https://educacao.uol.com.br/bancoderedacoes/propostas/politica-x-ciencia-a-pilula-do-cancer.htm',
    'https://educacao.uol.com.br/bancoderedacoes/propostas/impeachment-a-presidente-deve-perder-o-mandato.htm',
    'https://educacao.uol.com.br/bancoderedacoes/propostas/carta-convite-discutir-discriminacao-na-escola.htm',
    'https://educacao.uol.com.br/bancoderedacoes/propostas/forma-fisica-corpo-perfeito-e-consumismo.htm',
    'https://educacao.uol.com.br/bancoderedacoes/propostas/disciplina-ordem-e-autoridade-favorecem-a-educacao.htm',
    'https://educacao.uol.com.br/bancoderedacoes/propostas/o-sucesso-vem-da-escola-ou-do-esforco-individual.htm',
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
        'points': {
            'writing': points_text[0],
            'theme': points_text[1],
            'knowledge': points_text[2],
            'cohesion': points_text[3],
            'proposal': points_text[4],
            'total': points_text[5],
        },
    })

def init_scraper():
    themes = []
    essays = []

    for page_index, page in enumerate(PAGES_TO_SCRAP):
        theme_percent = (page_index + 1) / len(PAGES_TO_SCRAP) * 100

        print(f'{theme_percent:.2f}% start scrapping theme in: {page}')

        reponse = requests.get(page)

        html_string = reponse.text

        soup = BeautifulSoup(html_string, HTML_PARSER)

        essay_list = soup.select_one(ESSAY_LIST_SELECTOR)

        essay_divs = essay_list.find_all('div')

        for essay_index, essay_div in enumerate(essay_divs):
            essay_percent = (essay_index + 1) / len(essay_divs) * 100

            href = essay_div.select_one('a')['href']

            print(f'--- {essay_percent:.2f}% start scrapping essay in: {href}')

            try:
                scrap_essay_page(href, essays)
            except:
                print('Error on the essay proccessed above, skiping it...')

        essay_theme_element = soup.select_one('i.custom-title')

        essay_theme_text = essay_theme_element.get_text()

        themes.append({
            'theme': essay_theme_text,
            'total': len(essays),
            'essays': essays,
        })

        essays = []

    with open("uol_redacoes.json", "w") as text_file:
        json_string = json.dumps(themes, indent=4, ensure_ascii=False)

        print(json_string, file=text_file)

if __name__ == "__main__":
    init_scraper()
