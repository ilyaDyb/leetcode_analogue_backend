import sys
import json
import importlib.util
import os

def run_user_code(user_id: str, user_code, test_cases_str):
    filename = f'user_code_{user_id}.py'

    with open(filename, 'w') as f:
        f.write(user_code)
    
    spec = importlib.util.spec_from_file_location("user_module", filename)
    user_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(user_module)
    
    function_name = 'solution'
    function = getattr(user_module, function_name)

    try:
        test_cases = json.loads(test_cases_str)
    except json.JSONDecodeError as e:
        print(f"JSON decode error: {e}")
        os.remove(filename)
        return {'error': str(e)}

    results = []
    for case in test_cases:
        input_data = case['fields']['input_data']
        expected_output = case['fields']['expected_output']
        try:
            result = function(input_data)
            results.append({
                'input': input_data,
                'expected': expected_output,
                'result': result,
                'passed': result == expected_output
            })
        except Exception as e:
            results.append({
                'input': input_data,
                'expected': expected_output,
                'result': str(e),
                'passed': False
            })
    
    os.remove(filename)

    return results

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python executor.py <user_id> <user_code> <test_cases>")
        sys.exit(1)
    
    user_id = sys.argv[3]
    user_code = sys.argv[4]
    test_cases_str = sys.argv[5]
    print(user_id, user_code, test_cases_str)

    results = run_user_code(user_id, user_code, test_cases_str)
    print(results)
