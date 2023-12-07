import random
import string

def generate_id() -> str:
    return "".join(random.choices(string.ascii_uppercase, k=6))
