import random
import string

def generate_payload(payload_type, size=1024):
    """Генерация полезной нагрузки."""
    if payload_type == "random_file":
        filename = "random_file.txt"
        with open(filename, "w") as f:
            f.write("".join(random.choice(string.ascii_letters) for i in range(size)))
        return filename
    elif payload_type == "html_iframe":
        return "<iframe src='http://malicious.site' width='600' height='400'></iframe>"
    # Добавьте другие типы нагрузки по необходимости
    return None