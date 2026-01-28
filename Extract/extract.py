import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# 1. Config
url = "https://arquivos.receitafederal.gov.br/dados/cnpj/dados_abertos_cnpj/2026-01/"
folder = "raw_data"

def extract_zips(url):
        print(f"Acessing url {url}")

        #Make a request to the URL
        response = requests.get(url)
        if response.status_code != 200:
            print(f"The request has failed with status code {response.status_code}")
            return

        # busca por links dentro da pagina HTML
        soup = BeautifulSoup(response.text, 'html.parser')#Organiza os dados encontrados na pahia HTML
        links = soup.find_all('a')#Encontra todos os links na página HTML

        for link in links:
            href = link.get('href')

            # Check if the link ends with .zip
            if href and href.endswith('.zip'):
                # Create the full URL
                zip_url = urljoin(url, href)
                print(f"Found zip file: {zip_url}")

                archive_name = os.path.join(folder, href.split('/')[-1])
                if os.path.exists(archive_name):
                    print(f"{archive_name} already exists. Skipping download.")
                    continue
                print(f"Starting download of {archive_name}...")

                # Download the zip file
                with requests.get(zip_url, stream=True) as r:
                    r.raise_for_status()
                    with open(archive_name, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            f.write(chunk)
        print("All files have been downloaded.")

# Create folder if it doesn't exist
if not os.path.exists(folder):
    os.makedirs(folder)

extract_zips(url)
