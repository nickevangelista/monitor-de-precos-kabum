import requests
from bs4 import BeautifulSoup
import time
import re

url = 'https://www.kabum.com.br/produto/777077/placa-de-video-gigabyte-rtx-5060-windforce-8g-nvidia-geforce-8gb-gddr7-128bits-dlss-ray-tracing-gv-n5060wf2-8gd'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def verificar_preco():
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"Erro ao acessar a página: {response.status_code}")
            return

        soup = BeautifulSoup(response.content, 'html.parser')

        preco_element = soup.find('h4', class_='text-4xl text-secondary-500 font-bold transition-all duration-500')

        if preco_element:
            preco_texto = preco_element.get_text()
            
            preco_limpo = re.sub(r'[^\d,]', '', preco_texto)
            preco_float = float(preco_limpo.replace(',', '.'))
            
            print(f"--- Monitoramento ---")
            print(f"Produto: RTX 5060 Gigabyte")
            print(f"Preço Atual: R$ {preco_float}")
            
            target_price = 2100.00
            if preco_float <= target_price:
                print("🚨 OPA! O PREÇO CAIU! HORA DE COMPRAR! 🚨")
            else:
                print(f"Ainda está caro (Meta: R$ {target_price})")
                
        else:
            print("Não consegui encontrar o elemento de preço. O site pode ter mudado a estrutura HTML.")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")

while True:
    verificar_preco()
    time.sleep(1800)