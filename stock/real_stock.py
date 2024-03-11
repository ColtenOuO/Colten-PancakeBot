import yfinance as yf
df = yf.Ticker("2330.TW").history(period="max")
print(df)