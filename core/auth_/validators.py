
def validate_password(password: str) -> bool:
    if len(password) < 8:
        return False
    if not any([char.isdigit() for char in password]):
        return False
    return True