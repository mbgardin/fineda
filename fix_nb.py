import nbformat

with open('get_data.ipynb', 'r') as f:
    nb = nbformat.read(f, as_version=4)

# Cell 1: get_earnings
nb.cells[0].source = '''import requests\nimport pandas as pd\nfrom dotenv import load_dotenv\nimport os\nimport time\n\nload_dotenv()\n\nAV_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY")\n\ndef get_earnings(symbol):\n    url = f"https://www.alphavantage.co/query?function=EARNINGS&symbol={symbol}&apikey={AV_API_KEY}"\n    r = requests.get(url)\n    data = r.json()\n    \n    if "quarterlyEarnings" not in data:\n        print(f"Warning: No earnings data for {symbol}. Response: {data}")\n        return pd.DataFrame()\n        \n    quarterly = pd.DataFrame(data["quarterlyEarnings"])\n    quarterly["symbol"] = symbol\n    \n    # rate limit is 5 per minute\n    time.sleep(12.5)\n    return quarterly\n\n# example\ndf_earnings = get_earnings("AAPL")\ndf_earnings.head()'''

# Cell 5: main loop
before_loop = '''symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "META"]\nall_data = []\n\nfor sym in symbols:\n    print(f"Fetching data for {sym}...")\n    earnings = get_earnings(sym)\n    if earnings.empty:\n        continue\n        \n    # Processing earnings\n    earnings["reportedDate"] = pd.to_datetime(earnings["reportedDate"])\n    earnings["reportedEPS"] = pd.to_numeric(earnings["reportedEPS"], errors="coerce")\n    earnings["estimatedEPS"] = pd.to_numeric(earnings["estimatedEPS"], errors="coerce")\n    earnings["surprise_pct_calc"] = (earnings["reportedEPS"] - earnings["estimatedEPS"]) / earnings["estimatedEPS"]\n    earnings = earnings.dropna(subset=["reportedDate", "reportedEPS", "estimatedEPS", "surprise_pct_calc"])\n    \n    prices = get_prices(sym)\n    merged = compute_returns(prices, earnings)\n    \n    # Fetch additional company context via yfinance\n    try:\n        ticker = yf.Ticker(sym)\n        info = ticker.info\n        merged["Sector"] = info.get("sector", "Unknown")\n        merged["MarketCap"] = info.get("marketCap", pd.NA)\n    except:\n        merged["Sector"] = "Unknown"\n        merged["MarketCap"] = pd.NA\n        \n    all_data.append(merged)\n\nif all_data:\n    df_all = pd.concat(all_data, ignore_index=True)\n    display(df_all.head())\nelse:\n    df_all = pd.DataFrame()\n    print("No data gathered.")'''

nb.cells[4].source = before_loop

with open('get_data.ipynb', 'w') as f:
    nbformat.write(nb, f)
print("Notebook successfully updated")
