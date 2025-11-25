import requests
from bs4 import BeautifulSoup
import time
import re
import os # Necessário para ler variáveis de ambiente
from dotenv import load_dotenv # Importa a função que lê o arquivo .env

# Carrega as variáveis do arquivo .env
load_dotenv()

# Agora o código puxa do sistema, e não mais do texto escrito aqui
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

url = 'https://www.kabum.com.br/produto/777077/placa-de-video-gigabyte-rtx-5060-windforce-8g-nvidia-geforce-8gb-gddr7-128bits-dlss-ray-tracing-gv-n5060wf2-8gd'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def enviar_telegram(mensagem):
    # Verificação de segurança: Se não achar o token, avisa
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ ERRO: Token ou Chat ID não encontrados no arquivo .env")
        return

    try:
        url_api = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        
        data = {"chat_id": TELEGRAM_CHAT_ID, "text": mensagem}
        
        requests.post(url_api, data=data)
        print("✅ Notificação enviada para o Telegram!")
    except Exception as e:
        print(f"❌ Erro ao enviar Telegram: {e}")

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
                
                msg = f"🚨 BAIXOU!\nRTX 5060 Gigabyte\nNovo Preço: R$ {preco_float}\nLink: {url}"
                enviar_telegram(msg)
                
            else:
                print(f"Ainda está caro (Meta: R$ {target_price})")
                
        else:
            print("Não consegui encontrar o elemento de preço. O site pode ter mudado a estrutura HTML.")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")

print("Iniciando monitoramento seguro...")
while True:
    verificar_preco()
    time.sleep(1800)