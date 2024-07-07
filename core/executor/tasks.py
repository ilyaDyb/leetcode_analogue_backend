import subprocess
from celery import shared_task
import json
import logging

logging.basicConfig(level=logging.INFO)

@shared_task
def run_user_code(user_id: str, user_code, test_cases_json):
    network_name = "leetcode_network"

    command = [
        'docker', 'run', '--rm', '--network', network_name,
        'code_interpreter_image', 'python', 'executor.py',
        user_id, user_code, json.dumps(test_cases_json)
    ]

    # logging.info(f"Running command: {' '.join(command)}")
    logging.info(command)

    result = subprocess.run(command, capture_output=True, text=True)

    if result.returncode != 0:
        logging.error(f"Command error: {result.stderr}")
        return {'error': result.stderr}
    else:
        logging.info(f"Command output: {result.stdout}")
        return result.stdout
