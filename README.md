<h1 align="center">
  Web Scraper - Banco de Redações UOL
</h1>

<h4 align="center">Um Web Scraper para transformar os dados do banco de radações da UOL em JSON</h4>

<p align="center">
  <a href="#sobre">Sobre</a> •
  <a href="#uso">Uso</a> •
  <a href="#créditos">Créditos</a> •
  <a href="#licença">Licença</a>
</p>

## Sobre

Esse projeto tem como objetivo pegar os dados de [https://educacao.uol.com.br/bancoderedacoes/](https://educacao.uol.com.br/bancoderedacoes/) e transformar em um único arquivo JSON.

Os dados estão disponibilizados no arquivo [uol_redacoes.json](uol_redacoes.json)

## Uso

- Docker
  - ``docker compose up -d``
- Python 3 nativo
  - ``python -m venv venv``
  - Ative o ambiente virtual:
    - Windows: ``.\venv\Scripts\Activate.ps1``
    - Linux: ``source venv/bin/activate``
  - ``pip install -r requirements.txt``
  - ``python uol_redacoes_scraper.py``

## Créditos

- [Python](https://github.com/python)
  - Dependencias listadas no arquivo [requirements.txt](requirements.txt)
- [UOL](https://educacao.uol.com.br/bancoderedacoes/)

## Licença

MIT
