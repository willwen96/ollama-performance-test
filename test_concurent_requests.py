# import requests
# import time
# import sys
# import json
#
# def convert_nanoseconds_to_seconds(nanoseconds):
#     return nanoseconds / 1e9
#
# def process_response_packet(response_json, packet_number, final_packet, prompt_index):
#     if final_packet:
#         print("Final Response Packet:")
#         print("Total Duration:", convert_nanoseconds_to_seconds(response_json.get('total_duration', 0)), "seconds")
#         print("Load Duration:", convert_nanoseconds_to_seconds(response_json.get('load_duration', 0)), "seconds")
#         print("Prompt Evaluation Duration:", convert_nanoseconds_to_seconds(response_json.get('prompt_eval_duration', 0)), "seconds")
#         print("Prompt Evaluation Count:", response_json.get('prompt_eval_count', "N/A"))
#         print("Response Evaluation Duration:", convert_nanoseconds_to_seconds(response_json.get('eval_duration', 0)), "seconds")
#         print("Response Evaluation Count:", response_json.get('eval_count', "N/A"))
#         print("Context:", response_json.get('context', "N/A"))
#     elif packet_number % 25 == 0:
#         print(f"Index {prompt_index} Packet {packet_number}")
#
# def test_response_time(url, payload):
#     try:
#         response = requests.post(url, json=payload, timeout=300, stream=True)
#     except requests.Timeout:
#         print("Request timed out.")
#         return
#
#     if response is not None and response.status_code == 200:
#         packet_number = 1
#         for line in response.iter_lines():
#             if line:
#                 response_json = json.loads(line)
#                 final_packet = response_json.get('done', False)
#                 process_response_packet(response_json, packet_number, final_packet, prompt_index)
#                 packet_number += 1
#         end_time = time.time()
#         response_time = end_time - start_time
#         print(f"Request {prompt_index} Response Time:", response_time, "seconds")
#         print("\n")
#
# if __name__ == "__main__":
#     if len(sys.argv) != 3:
#         print("Usage: python script.py <ip_address> <prompt_index>")
#         sys.exit(1)
#
#     ip_address = sys.argv[1]
#     prompt_index = int(sys.argv[2])
#     url = f"http://{ip_address}/api/generate"
#
#     prompts = [
#         "Why is the sky blue?",
#         "How does LLM get better and better in recent years? Why it can replace many ML tasks that are not related to language?",
#         "Help me write a wedding HTML template. Add some styles and effects to make it look pretty."
#     ]
#
#     prompt = prompts[prompt_index]
#     payload = {
#         "model": "llama3",
#         "prompt": prompt,
#         "stream": True,
#         "options": {"seed": 123, "temperature": 0}
#     }
#
#     start_time = time.time()
#     test_response_time(url, payload)

import requests
import time
import sys
import json
from concurrent.futures import ThreadPoolExecutor

def convert_nanoseconds_to_seconds(nanoseconds):
    return nanoseconds / 1e9

def process_response_packet(response_json, packet_number, final_packet, index):
    if final_packet:
        print("Final Response Packet:")
        print("Total Duration:", convert_nanoseconds_to_seconds(response_json.get('total_duration', 0)), "seconds")
        print("Load Duration:", convert_nanoseconds_to_seconds(response_json.get('load_duration', 0)), "seconds")
        print("Prompt Evaluation Duration:", convert_nanoseconds_to_seconds(response_json.get('prompt_eval_duration', 0)), "seconds")
        print("Prompt Evaluation Count:", response_json.get('prompt_eval_count', "N/A"))
        print("Response Evaluation Duration:", convert_nanoseconds_to_seconds(response_json.get('eval_duration', 0)), "seconds")
        print("Response Evaluation Count:", response_json.get('eval_count', "N/A"))
        print("Context:", response_json.get('context', "N/A"))
    elif packet_number == 0 or packet_number%25 == 0:
        print(f"Index {index} Packet {packet_number}")

def test_response_time(url, payload, prompt_index):
    try:
        response = requests.post(url, json=payload, timeout=600, stream=True)
    except requests.Timeout:
        print(f"Request {prompt_index} timed out.")
        return

    if response is not None and response.status_code == 200:
        packet_number = 1
        for line in response.iter_lines():
            if line:
                response_json = json.loads(line)
                final_packet = response_json.get('done', False)
                process_response_packet(response_json, packet_number, final_packet, prompt_index)
                packet_number += 1
        end_time = time.time()
        response_time = end_time - start_time
        print(f"Request {prompt_index} Response Time:", response_time, "seconds")
        print("\n")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py <ip_address>")
        sys.exit(1)

    ip_address = sys.argv[1]
    url = f"http://{ip_address}/api/generate"

    # Define prompts for each request
    prompts = [
        "Why is the sky blue?",
        "How does LLM get better and better in recent years? Why it can replace many ML tasks that are not language-related?",
        "Help me write a wedding HTML template. Add some styles and effects to make it look pretty."
    ]

    # Function to send requests concurrently
    def send_request(prompt, prompt_index):
        payload = {
            "model": "llama3",
            "prompt": prompt,
            "stream": True,
            "options": {"seed": 123, "temperature": 0}
        }
        start_time = time.time()
        test_response_time(url, payload, prompt_index)
        end_time = time.time()
        response_time = end_time - start_time
        if response_time is None:
            print("Request timed out.")
        else:
            print("Response Time:", response_time, "seconds")
        print("\n")

    # Send multiple requests concurrently
    with ThreadPoolExecutor(max_workers=len(prompts)) as executor:
        for index, prompt in enumerate(prompts):
            executor.submit(send_request, prompt, index)
