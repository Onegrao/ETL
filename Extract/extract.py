#Extract the data from the source and save it in 'raw' db csv files.
import sqlite3
import requests as rq

link = "http://compras.dados.gov.br/docs/lista-metodos-licitacoes.html"
dbfile = "raw_data.db"


def extract_data(link,dbfile):

    #Pull data from link
    print("Extrancting data from source...")
    data = rq.get(link).text
    print(data)


if __name__ == "__main__":
    extract_data(link,dbfile)
