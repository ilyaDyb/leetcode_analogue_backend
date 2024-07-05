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

    response = requests.post('http://127.0.0.1:8000/api/interpreter/receive_result/', json={'result': result})
    print(response.status_code, response.reason)