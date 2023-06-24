

import requests
import time

API_URL = "https://api-inference.huggingface.co/models/bigcode/starcoder"
API_KEY = "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"  # Replace with your actual API key
headers = {"Authorization": f"Bearer {API_KEY}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

def review_code(code: str, retries=3, wait_time=20):
    for _ in range(retries):
        payload = {"inputs": code}
        output = query(payload)

        if "error" in output and output["error"].startswith("Model"):
            print("Model is loading, waiting and retrying...")
            time.sleep(wait_time)
        else:
            return output
    return None

code_to_review = """
def factorial_recursive(n):
    if n == 0:
        return 1
    else:
        return n * factorial_recursive(n-1)

def factorial_iterative(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result

def main():
    num = 5
    num = 5
    print(f"Recursive Factorial of {num}: {factorial_recursive(num)}")
    print(f"Iterative Factorial of {num}: {factorial_iterative(num)}")

if __name__ == "__main__":
    main()

"""

review_result = review_code(code_to_review)
print(review_result)

