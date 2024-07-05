import subprocess
from celery import shared_task

@shared_task
def run_user_code(user_code):
    # Используем массив строк для команды и аргументов, чтобы избежать проблем с кавычками
    command = ['docker', 'run', '--rm', 'code_interpreter_image', 'python', 'executor.py', user_code]
    result = subprocess.run(command, capture_output=True, text=True)
    
    print(result.stdout)
    if result.returncode != 0:
        print(result.stderr)
        return result.stderr
    return result.stdout