import requests
from bs4 import BeautifulSoup
import re
import os

# Tenta importar dotenv para uso local (no seu PC). 
# No GitHub Actions, isso vai falhar ou não fazer nada, mas não tem problema.
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Pega as variáveis de ambiente (Configuradas nas Secrets do GitHub)
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

url = 'https://www.kabum.com.br/produto/460434/air-cooler-para-processador-deepcool-ak400-bk-preto'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def enviar_telegram(mensagem):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        print("❌ ERRO: Token ou Chat ID não encontrados.")
        return

    try:
        url_api = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        data = {"chat_id": TELEGRAM_CHAT_ID, "text": mensagem}
        requests.post(url_api, data=data)
        print("✅ Notificação enviada para o Telegram!")
    except Exception as e:
        print(f"❌ Erro ao enviar Telegram: {e}")

def verificar_preco():
    print("Iniciando verificação...")
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code != 200:
            print(f"Erro ao acessar a página: {response.status_code}")
            return

        soup = BeautifulSoup(response.content, 'html.parser')

        # Classe atualizada da Kabum
        preco_element = soup.find('h4', class_='text-4xl text-secondary-500 font-bold transition-all duration-500')

        if preco_element:
            preco_texto = preco_element.get_text()
            preco_limpo = re.sub(r'[^\d,]', '', preco_texto)
            preco_float = float(preco_limpo.replace(',', '.'))
            
            print(f"Produto: Cooler DeepCool AK 400")
            print(f"Preço Atual: R$ {preco_float}")
            
            target_price = 167
            
            if preco_float <= target_price:
                print("🚨 PREÇO ALVO ATINGIDO!")
                msg = f"🚨 BAIXOU!\nCooler DeepCool AK 400\nNovo Preço: R$ {preco_float}\nLink: {url}"
                enviar_telegram(msg)
            else:
                print(f"Ainda acima da meta de R$ {target_price}")
        else:
            print("Elemento de preço não encontrado.")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")

# Executa apenas uma vez
if __name__ == "__main__":
    verificar_preco()