# Monitor de Preços Kabum (Bot Telegram)

Este projeto é um script em Python que monitora automaticamente o preço de um produto específico no site da **Kabum**. Quando o preço atinge um valor alvo (target price), ele envia uma notificação imediata para o seu **Telegram**.

O script foi configurado para rodar localmente ou via **GitHub Actions** (na nuvem).

## 🚀 Funcionalidades

- **Web Scraping:** Acessa a página do produto e extrai o preço atual.
- **Alerta de Preço:** Compara o preço atual com o valor desejado (ex: R$ 2.100,00).
- **Notificação Telegram:** Envia mensagem com o link e o novo preço se a meta for atingida.
- **Suporte a GitHub Actions:** Pode ser agendado para rodar automaticamente na nuvem.

## 🛠️ Tecnologias Utilizadas

- Python 3.9+
- [Requests](https://pypi.org/project/requests/) (Requisições HTTP)
- [BeautifulSoup4](https://pypi.org/project/beautifulsoup4/) (Parsing de HTML)
- [Python-dotenv](https://pypi.org/project/python-dotenv/) (Gerenciamento de variáveis de ambiente)
