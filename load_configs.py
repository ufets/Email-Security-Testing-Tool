
def parse_recipients(filename="recipients.txt"):
    """Парсинг списка получателей из файла."""
    recipients = []
    try:
        with open(filename, "r") as f:
            for line in f:
                email = line.strip()
                if email:  # Проверка на пустые строки
                    recipients.append(email)
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None
    return recipients

def parse_sender(filename="sender.txt"):
    """Парсинг данных отправителя из файла."""
    try:
        with open(filename, "r") as f:
            sender_email = f.readline().strip()
            sender_password = f.readline().strip()
            return sender_email, sender_password
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        return None, None
    except IndexError:
        print(f"Error: Incorrect format in '{filename}'. Should be two lines: email and password.")
        return None, None