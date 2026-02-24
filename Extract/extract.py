import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Configurações de retry para lidar com falhas temporárias de rede
def create_session_with_retry():
    session = requests.Session()

    retry = Retry(
        total=5,                # tenta até 5 vezes
        backoff_factor=2,       # tempo exponencial (2, 4, 8...)
        status_forcelist=[500, 502, 503, 504],
        allowed_methods=["GET"]
    )

    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    return session



def extract_zips(url, folder):
    print(f"Accessing url {url}")

    #Inicia sessão 
    session = create_session_with_retry()

    try:
        #Faz a requisição para o site
        response = session.get(url, stream=True, timeout=30)
        response.raise_for_status()

        #Web scraping para encontrar os links dos arquivos zip
        soup = BeautifulSoup(response.content, 'html.parser')
        links = soup.find_all('a')

        #Encontra os arquivos zip e baixa
        for link in links:
            href = link.get('href')

            if href and href.endswith('.zip'):
                zip_url = urljoin(url, href)
                archive_name = os.path.join(folder, href.split('/')[-1])

                if os.path.exists(archive_name):
                    print(f"{archive_name} already exists. Skipping.")
                    continue

                print(f"Downloading {archive_name}...")

                with session.get(zip_url, stream=True, timeout=60) as r:
                    r.raise_for_status()
                    with open(archive_name, 'wb') as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            if chunk:
                                f.write(chunk)

        print("All files processed.")

    #Tratamento de exceções para falhas de rede
    except requests.RequestException as e:
        print(f"Failed after retries: {e}")

def extract():
    print("Starting the extraction process...")
    # 1. Config
    url = "https://arquivos.receitafederal.gov.br/index.php/s/YggdBLfdninEJX9?dir=/2026-01"
    folder = "raw_data"

    # Criar pasta se não existir
    if not os.path.exists(folder):
       os.makedirs(folder)

    extract_zips(url,folder)
