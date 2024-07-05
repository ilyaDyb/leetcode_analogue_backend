import requests
import sys

def execute_user_code(user_code):
    try:
        exec(user_code)
        result = "Code executed successfully"
    except Exception as e:
        result = str(e)
    return result

if __name__ == "__main__":
    user_code = sys.argv[1]
    result = execute_user_code(user_code)
    print(user_code, result)

    response = requests.get('http://web:8000/api/interpreter/receive_result/')
    print(response.status_code, response.reason)
