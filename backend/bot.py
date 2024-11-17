import ccxt

exchanges = {
    "binance": ccxt.binance(),
    "coinbase": ccxt.coinbase(),
}

fees = {
    "binance": 0.001,  # 0.1% de taxa
    "coinbase": 0.005, # 0.5% de taxa
}

def fetch_prices(pair="BTC/USDT"):
    """
    Busca os preços do par fornecido em todas as exchanges configuradas.

    Args:
        pair (str): Par de moedas, ex: "BTC/USDT".

    Returns:
        dict: Preços por exchange.
    """
    prices = {}
    for name, exchange in exchanges.items():
        try:
            ticker = exchange.fetch_ticker(pair)
            prices[name] = ticker['last']  
        except Exception as e:
            print(f"Erro ao buscar preços na {name}: {e}")
    return prices

# Função para calcular oportunidades de arbitragem
def calculate_arbitrage(prices):
    """
    Calcula oportunidades de arbitragem com base nos preços fornecidos.

    Args:
        prices (dict): Dicionário com os preços das exchanges.

    Returns:
        dict | None: Detalhes da arbitragem ou None se não houver oportunidades.
    """
    if len(prices) < 2:
        return None

    # Ordenar preços da menor para a maior
    sorted_prices = sorted(prices.items(), key=lambda x: x[1])
    cheapest = sorted_prices[0]  # Exchange com o preço mais baixo
    most_expensive = sorted_prices[-1]  # Exchange com o preço mais alto

    # Calcular taxas
    buy_fee = cheapest[1] * fees[cheapest[0]]
    sell_fee = most_expensive[1] * fees[most_expensive[0]]

    # Calcular lucro líquido
    profit = (most_expensive[1] - cheapest[1]) - (buy_fee + sell_fee)

    if profit > 0:
        return {
            "buy_from": cheapest[0],
            "buy_price": cheapest[1],
            "sell_on": most_expensive[0],
            "sell_price": most_expensive[1],
            "profit": profit,
        }
    return None
