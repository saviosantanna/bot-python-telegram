import requests
from bs4 import BeautifulSoup
import time
import schedule
import telegram

# Configurações do Telegram
TELEGRAM_TOKEN = '8172321886:AAGtqSYWbPj7rBfi0S8EIX_QQm1h9rBhYHo'
CHAT_ID = '447938340'

# URL da página a ser verificada
URL = 'https://www.ifes.edu.br/processosseletivos/servidores/item/3194-concurso-publico-2-2024-tecnicos-administrativos'

# Função para enviar mensagem via Telegram
def send_telegram_message(message):
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    bot.send_message(chat_id=CHAT_ID, text=message)

# Função para verificar a página
def check_page():
    try:
        response = requests.get(URL)
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.get_text()

        if "Etapa de inscrição" in content:
            print("Palavra 'Etapa de Prova' encontrada!")
            send_telegram_message("A palavra 'Etapa de Prova' foi encontrada na página!")
            return True
        else:
            print("Palavra 'Etapa de Prova' não encontrada.")
            return False
    except Exception as e:
        print(f"Erro ao acessar a página: {e}")
        return False

# Agendar a execução a cada 15 minutos
schedule.every(15).minutes.do(check_page)

# Executar o agendador por 24 horas
start_time = time.time()
while time.time() - start_time < 86400:  # 86400 segundos = 24 horas
    schedule.run_pending()
    time.sleep(1)

print("Verificação concluída após 24 horas.")
