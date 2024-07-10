import subprocess
from celery import shared_task
import json
import logging

logging.basicConfig(level=logging.INFO)

@shared_task
def run_user_code(user_id: str, user_code, test_cases_json):
    network_name = "leetcode_network"

    command = [
        'timeout', '2s',
        'docker', 'run', '--rm', '--network', network_name,
        'code_interpreter_image', 'python', 'executor.py',
        user_id, user_code, json.dumps(test_cases_json)
    ]

    logging.info(f"Running command: {' '.join(command)}")

    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        logging.error(f"Command failed with error: {e.stderr}")
        return {'error': e.stderr}
    except subprocess.TimeoutExpired:
        logging.error("Command timed out")
        return {'error': 'Runtime error: Code execution exceeded the time limit'}

    if result.returncode != 0:
        logging.error(f"Command error: {result.stderr}")
        return {'error': result.stderr}
    else:
        logging.info(f"Command output: {result.stdout}")
        try:
            # Проверяем, что результат является валидным JSON
            output = json.loads(result.stdout)
            logging.info(f"JSON output: {output}")
            return output
        except json.JSONDecodeError as e:
            logging.error(f"JSON decode error: {e}")
            return {'error': f"JSON decode error: {e}"}
