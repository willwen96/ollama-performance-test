import requests
import time
import sys

def test_response_time(url, payload):
    start_time = time.time()
    try:
        response = requests.post(url, json=payload, timeout=300)
    except requests.Timeout:
        return None, None
    end_time = time.time()
    response_time = end_time - start_time
    return response, response_time

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <ip_address>")
        sys.exit(1)
    
    ip_address = sys.argv[1]
    url = f"http://{ip_address}/api/generate"
    payload = {
        "model": "llama3",
        "prompt": "Why is the sky blue?",
        "stream": False,
        "options": {"seed": 123, "temperature": 0}
    }
    response, response_time = test_response_time(url, payload)
    if response is None:
        print("Request timed out.")
    else:
        print("Response:", response.json())
        print("Response Time:", response_time, "seconds")

