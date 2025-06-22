import requests
import streamlit

@streamlit.cache_data
def get_currency_list():
    url = "https://api.frankfurter.app/currencies"
    response = requests.get(url)
    if response.status_code == 200:
        return dict(response.json())
    return {}

def convert_currency(amount, from_currency, to_currency):
    url = f"https://api.frankfurter.app/latest?amount={amount}&from={from_currency}&to={to_currency}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        rate = data["rates"][to_currency]
        date = data["date"]
        return rate, rate / amount, date
    return None, None

streamlit.set_page_config(page_title="Currency Converter", page_icon="💵")
streamlit.title("Currency Converter 💱")

currencies = get_currency_list()
currency_codes = sorted(currencies.keys())

from_currency = streamlit.selectbox("From Currency", currency_codes, index=currency_codes.index("USD"))
to_currency = streamlit.selectbox("To Currency", currency_codes, index=currency_codes.index("GBP"))

amount = streamlit.number_input("Amount", min_value=0.0, value=1.0, step=0.1)

if streamlit.button("Convert"):
    result, rate, date = convert_currency(amount, from_currency, to_currency)
    if result:
        streamlit.success(f"{amount} {from_currency} = {result:.2f} {to_currency}")
        streamlit.caption(f"Exchange Rate: 1 {from_currency} = {rate:.4f} {to_currency}")
        streamlit.caption(f"Date: {date}")
    else:
        streamlit.error("Something went Wrong, Please try again.")
