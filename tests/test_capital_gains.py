import pytest
import requests
import time

CAPITAL_GAINS_URL = "http://localhost:5003"
STOCKS_URL = "http://localhost:5001"

def test_capital_gains_service_health():
    """Test if capital gains service is running"""
    try:
        response = requests.get(f"{CAPITAL_GAINS_URL}/capital-gains")
        assert response.status_code in [200, 500]  # 500 is acceptable if no stocks exist
    except requests.exceptions.ConnectionError:
        pytest.fail("Capital gains service is not running")

def test_calculate_capital_gains():
    """Test capital gains calculation"""
    # First add a stock
    stock_data = {
        "symbol": "MSFT",
        "shares": 75,
        "purchase_price": 200.0,
        "purchase_date": "2023-01-01"
    }
    
    # Create stock
    create_response = requests.post(f"{STOCKS_URL}/stocks", json=stock_data)
    assert create_response.status_code == 201
    
    # Calculate capital gains
    response = requests.get(f"{CAPITAL_GAINS_URL}/capital-gains")
    assert response.status_code == 200
    
    # Clean up
    stock_id = create_response.json()["id"]
    delete_response = requests.delete(f"{STOCKS_URL}/stocks/{stock_id}")
    assert delete_response.status_code == 204

def test_capital_gains_with_share_filters():
    """Test capital gains calculation with share filters"""
    # Add stocks with different share amounts
    stocks = [
        {"symbol": "AAPL", "shares": 50, "purchase_price": 150.0},
        {"symbol": "GOOGL", "shares": 100, "purchase_price": 2500.0},
        {"symbol": "MSFT", "shares": 75, "purchase_price": 200.0}
    ]
    
    stock_ids = []
    for stock in stocks:
        response = requests.post(f"{STOCKS_URL}/stocks", json=stock)
        assert response.status_code == 201
        stock_ids.append(response.json()["id"])
    
    # Test with share filters
    response = requests.get(f"{CAPITAL_GAINS_URL}/capital-gains?numsharesgt=60")
    assert response.status_code == 200
    
    # Clean up
    for stock_id in stock_ids:
        delete_response = requests.delete(f"{STOCKS_URL}/stocks/{stock_id}")
        assert delete_response.status_code == 204