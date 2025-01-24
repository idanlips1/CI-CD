import pytest
import requests
import time

STOCKS_URL = "http://localhost:5001"

def test_stocks_service_health():
    """Test if stocks service is running"""
    try:
        response = requests.get(f"{STOCKS_URL}/stocks")
        assert response.status_code == 200
    except requests.exceptions.ConnectionError:
        pytest.fail("Stocks service is not running")

def test_add_stock():
    """Test adding a new stock"""
    stock_data = {
        "symbol": "AAPL",
        "shares": 100,
        "purchase_price": 150.0,
        "purchase_date": "2023-01-01"
    }
    
    response = requests.post(f"{STOCKS_URL}/stocks", json=stock_data)
    assert response.status_code == 201
    assert "id" in response.json()
    
    # Clean up - delete the created stock
    stock_id = response.json()["id"]
    delete_response = requests.delete(f"{STOCKS_URL}/stocks/{stock_id}")
    assert delete_response.status_code == 204

def test_get_stock():
    """Test getting a stock"""
    # First create a stock
    stock_data = {
        "symbol": "GOOGL",
        "shares": 50,
        "purchase_price": 2500.0,
        "purchase_date": "2023-01-01"
    }
    
    create_response = requests.post(f"{STOCKS_URL}/stocks", json=stock_data)
    assert create_response.status_code == 201
    stock_id = create_response.json()["id"]
    
    # Get the stock
    get_response = requests.get(f"{STOCKS_URL}/stocks/{stock_id}")
    assert get_response.status_code == 200
    assert get_response.json()["symbol"] == "GOOGL"
    
    # Clean up
    delete_response = requests.delete(f"{STOCKS_URL}/stocks/{stock_id}")
    assert delete_response.status_code == 204