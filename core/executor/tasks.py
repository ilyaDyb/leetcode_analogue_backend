import subprocess
from celery import shared_task
import logging

@shared_task
def run_user_code(user_code):

    network_name = "leetcode_network"
    command = ['docker', 'run', '--rm', '--network', network_name, 'code_interpreter_image', 'python', 'executor.py', user_code]
    logging.info(f"Running command: {' '.join(command)}")
    result = subprocess.run(command, capture_output=True, text=True)
    
    logging.info(f"Command output: {result.stdout}")
    if result.returncode != 0:
        logging.error(f"Command error: {result.stderr}")
        return result.stderr
    return result.stdout