import requests
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import telegram
import os

# Configurações
api_key = os.getenv('ALPHA_VANTAGE_API_KEY')
symbol = 'ITSA.SA'
outputsize = 'full'
datatype = 'json'
interval = 'daily'

# Token do Bot do Telegram e ID do chat
telegram_token = os.getenv('TELEGRAM_BOT_TOKEN')
chat_id = os.getenv('TELEGRAM_CHAT_ID')

# URL da API Alpha Vantage
url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&outputsize={outputsize}&apikey={api_key}'

# Obter dados da API
response = requests.get(url)
data = response.json()

# Preparar dados
df = pd.DataFrame(data['Time Series (Daily)']).T
df = df.rename(columns={'1. open': 'Open', '2. high': 'High', '3. low': 'Low', '4. close': 'Close', '5. adjusted close': 'Adjusted Close', '6. volume': 'Volume', '7. dividend amount': 'Dividend Amount', '8. split coefficient': 'Split Coefficient'})
df.index = pd.to_datetime(df.index)
df = df.sort_index()
df['Adjusted Close'] = pd.to_numeric(df['Adjusted Close'])

# Dividir em treino e teste
train_data = df['Adjusted Close'][:-7]
test_data = df['Adjusted Close'][-7:]

# Ajustar modelo ARIMA
model = ARIMA(train_data, order=(5, 1, 0))
model_fit = model.fit()

# Fazer previsões
forecast = model_fit.forecast(steps=7)
forecast_dates = [df.index[-1] + timedelta(days=i) for i in range(1, 8)]

# Plotar resultados
plt.figure(figsize=(12, 6))
plt.plot(df.index, df['Adjusted Close'], label='Real')
plt.plot(forecast_dates, forecast, label='Previsão', color='red')
plt.xlabel('Data')
plt.ylabel('Preço Ajustado de Fechamento')
plt.title('Previsão ARIMA para ITSA')
plt.legend()
plt.grid()
plt.savefig('forecast_plot.png')

# Enviar mensagem para o Telegram
bot = telegram.Bot(token=telegram_token)

message = f'Previsão para o próximo dia ({forecast_dates[0].date()}): {forecast[0]:.2f}\n'
message += 'Previsões para os próximos 7 dias:\n'
for date, value in zip(forecast_dates, forecast):
    message += f'{date.date()}: {value:.2f}\n'

# Enviar texto
bot.send_message(chat_id=chat_id, text=message)

# Enviar gráfico
bot.send_photo(chat_id=chat_id, photo=open('forecast_plot.png', 'rb'))
