import requests
import json
from datetime import datetime
import os

STOCKS_URL = "http://localhost:5001"
CAPITAL_GAINS_URL = "http://localhost:5003"

def post_initial_stocks():
    """Post the 6 required stocks"""
    stocks = [
        {
            "name": "NVIDIA Corporation",
            "symbol": "NVDA",
            "purchase price": 134.66,
            "purchase date": "18-06-2024",
            "shares": 7
        },
        {
            "name": "Apple Inc.",
            "symbol": "AAPL",
            "purchase price": 183.63,
            "purchase date": "22-02-2024",
            "shares": 19
        },
        {
            "name": "Alphabet Inc.",
            "symbol": "GOOG",
            "purchase price": 140.12,
            "purchase date": "24-10-2024",
            "shares": 14
        },
        {
            "name": "Tesla, Inc.",
            "symbol": "TSLA",
            "purchase price": 194.58,
            "purchase date": "28-11-2022",
            "shares": 32
        },
        {
            "name": "Microsoft Corporation",
            "symbol": "MSFT",
            "purchase price": 420.55,
            "purchase date": "09-02-2024",
            "shares": 35
        },
        {
            "name": "Intel Corporation",
            "symbol": "INTC",
            "purchase price": 19.15,
            "purchase date": "13-01-2025",
            "shares": 10
        }
    ]
    
    for stock in stocks:
        response = requests.post(f"{STOCKS_URL}/stocks", json=stock)
        if response.status_code != 201:
            print(f"Failed to post stock {stock['symbol']}: {response.text}")
        else:
            print(f"Successfully posted stock {stock['symbol']}")

def execute_query(service, query_string):
    """Execute a query and return the response"""
    if service.strip() == "stocks":
        url = f"{STOCKS_URL}/stocks?{query_string}"
    else:  # capital-gains
        url = f"{CAPITAL_GAINS_URL}/capital-gains?{query_string}"
    
    print(f"Executing query: {url}")
    response = requests.get(url)
    print(f"Response status: {response.status_code}")
    return response

def process_queries():
    """Process queries from query.txt and write results to response.txt"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    query_path = os.path.join(script_dir, 'query.txt')
    response_path = os.path.join(script_dir, 'response.txt')
    
    with open(query_path, 'r') as query_file, open(response_path, 'w') as response_file:
        for line in query_file:
            if not line.strip():  # Skip empty lines
                continue
                
            service, query = line.strip().split(':', 1)
            
            # Write query to response file
            response_file.write(f"query: {line.strip()}\n")
            response_file.write("response: ")
            
            # Execute query
            response = execute_query(service, query)
            
            # Write response
            try:
                json_response = response.json()
                response_file.write(json.dumps(json_response, indent=2))
            except:
                response_file.write(response.text)
            response_file.write("\n\n")

def main():
    """Main function to run the query execution process"""
    print("Starting query execution process...")
    
    #print("\nPosting initial stocks...")
    #post_initial_stocks()
    
    print("\nProcessing queries...")
    process_queries()
    
    print("\nQuery execution completed. Check response.txt for results.")

if __name__ == "__main__":
    main() 