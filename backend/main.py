from flask import Flask, jsonify
from bot import fetch_prices, calculate_arbitrage

app = Flask(__name__)

@app.route("/api/arbitrage", methods=["GET"])
def api_arbitrage():
    
    pair = "BTC/USDT"  
    prices = fetch_prices(pair)  
    opportunity = calculate_arbitrage(prices)  
    return jsonify({
        "prices": prices,
        "opportunity": opportunity
    })

@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Backend is running. Access /api/arbitrage for data."})

if __name__ == "__main__":
    app.run(debug=True)
