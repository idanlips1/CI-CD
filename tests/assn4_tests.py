import pytest
import requests
import time

STOCKS_URL = "http://localhost:5001"

# Test data
stock1 = {
    "name": "NVIDIA Corporation",
    "symbol": "NVDA",
    "purchase price": 134.66,
    "purchase date": "18-06-2024",
    "shares": 7
}

stock2 = {
    "name": "Apple Inc.",
    "symbol": "AAPL",
    "purchase price": 183.63,
    "purchase date": "22-02-2024",
    "shares": 19
}

stock3 = {
    "name": "Alphabet Inc.",
    "symbol": "GOOG",
    "purchase price": 140.12,
    "purchase date": "24-10-2024",
    "shares": 14
}

stock4 = {
    "name": "Tesla, Inc.",
    "symbol": "TSLA",
    "purchase price": 194.58,
    "purchase date": "28-11-2022",
    "shares": 32
}

stock5 = {
    "name": "Microsoft Corporation",
    "symbol": "MSFT",
    "purchase price": 420.55,
    "purchase date": "09-02-2024",
    "shares": 35
}

stock6 = {
    "name": "Intel Corporation",
    "symbol": "INTC",
    "purchase price": 19.15,
    "purchase date": "13-01-2025",
    "shares": 10
}

stock7 = {
    "name": "Amazon.com, Inc.",
    "purchase price": 134.66,
    "purchase date": "18-06-2024",
    "shares": 7
    # Missing symbol field intentionally
}

stock8 = {
    "name": "Amazon.com, Inc.",
    "symbol": "AMZN",
    "purchase price": 134.66,
    "purchase date": "Tuesday, June 18, 2024",  # Invalid date format
    "shares": 7
}

# Store IDs for use across tests
stock_ids = {}

def test_1_post_stocks():
    """Test POST /stocks for three stocks"""
    # Post stock1
    response1 = requests.post(f"{STOCKS_URL}/stocks", json=stock1)
    assert response1.status_code == 201
    stock_ids['stock1'] = response1.json()['id']

    # Post stock2
    response2 = requests.post(f"{STOCKS_URL}/stocks", json=stock2)
    assert response2.status_code == 201
    stock_ids['stock2'] = response2.json()['id']

    # Post stock3
    response3 = requests.post(f"{STOCKS_URL}/stocks", json=stock3)
    assert response3.status_code == 201
    stock_ids['stock3'] = response3.json()['id']

    # Verify unique IDs
    assert len({stock_ids['stock1'], stock_ids['stock2'], stock_ids['stock3']}) == 3

def test_2_get_stock_by_id():
    """Test GET /stocks/{ID} for stock1"""
    response = requests.get(f"{STOCKS_URL}/stocks/{stock_ids['stock1']}")
    assert response.status_code == 200
    assert response.json()['symbol'] == "NVDA"

def test_3_get_all_stocks():
    """Test GET /stocks"""
    response = requests.get(f"{STOCKS_URL}/stocks")
    assert response.status_code == 200
    stocks = response.json()
    assert len(stocks) == 3

def test_4_get_stock_values():
    """Test GET /stock-value/{ID} for all stocks"""
    global stock_values
    stock_values = {}
    
    # Get stock1 value
    response1 = requests.get(f"{STOCKS_URL}/stock-value/{stock_ids['stock1']}")
    assert response1.status_code == 200
    assert response1.json()['symbol'] == "NVDA"
    stock_values['sv1'] = response1.json()['ticker']

    # Get stock2 value
    response2 = requests.get(f"{STOCKS_URL}/stock-value/{stock_ids['stock2']}")
    assert response2.status_code == 200
    assert response2.json()['symbol'] == "AAPL"
    stock_values['sv2'] = response2.json()['ticker']

    # Get stock3 value
    response3 = requests.get(f"{STOCKS_URL}/stock-value/{stock_ids['stock3']}")
    assert response3.status_code == 200
    assert response3.json()['symbol'] == "GOOG"
    stock_values['sv3'] = response3.json()['ticker']

def test_5_portfolio_value():
    """Test GET /portfolio-value"""
    response = requests.get(f"{STOCKS_URL}/portfolio-value")
    assert response.status_code == 200
    pv = response.json()['portfolio value']
    
    total_stock_value = stock_values['sv1'] + stock_values['sv2'] + stock_values['sv3']
    assert pv * 0.97 <= total_stock_value <= pv * 1.03

def test_6_post_invalid_stock():
    """Test POST /stocks with missing symbol"""
    response = requests.post(f"{STOCKS_URL}/stocks", json=stock7)
    assert response.status_code == 400

def test_7_delete_stock():
    """Test DELETE /stocks/{ID} for stock2"""
    response = requests.delete(f"{STOCKS_URL}/stocks/{stock_ids['stock2']}")
    assert response.status_code == 204

def test_8_get_deleted_stock():
    """Test GET /stocks/{ID} for deleted stock2"""
    response = requests.get(f"{STOCKS_URL}/stocks/{stock_ids['stock2']}")
    assert response.status_code == 404

def test_9_post_invalid_date():
    """Test POST /stocks with invalid date format"""
    response = requests.post(f"{STOCKS_URL}/stocks", json=stock8)
    assert response.status_code == 400 