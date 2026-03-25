# ETL : Processamento de Dados com Polars & SQLite

## 📌 Sobre o Projeto
Este projeto foi desenvolvido para praticar conceitos fundamentais de Engenharia de Dados, focando em performance e estruturação de ETL. O objetivo foi extrair dados brutos, realizar transformações e carregá-los em um banco de dados local para análise.

## 🛠️ Tecnologias Utilizadas
* **Python**: Linguagem principal.
* **Polars**: Biblioteca de processamento de dados de alta performance (Lazy API e paralelismo).
* **SQLite**: Banco de dados relacional leve para armazenamento da camada final.
* **BeautifulSoup**: Biblioteca para scraping de informações.

## 🏗️ Arquitetura (Medallion-like)
O projeto simula o fluxo de organização de dados:
1.  **Extração**: WebScraping e leitura de arquivos (CSV/JSON) brutos.
2.  **Transformação**: Limpeza, tipagem de colunas e agregações utilizando as expressões otimizadas do Polars.
3.  **Carga**: Persistência dos dados transformados em tabelas SQLite.

## 📈 Aprendizados
* Manipulação de grandes volumes de dados de forma eficiente com a biblioteca Polars.
* Gerenciamento de conexões e execução de queries SQL via Python.
* Aplicação de boas práticas de estruturação de projetos de dados.