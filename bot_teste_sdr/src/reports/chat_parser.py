# src/reports/chat_parser.py
import os
import re
import glob
from datetime import datetime

def parse_line(line):
    """
    Exemplo de parsing de linha do chat:
    [DD/MM/YYYY, HH:MM:SS] Nome: Mensagem
    Retorna dicionário {timestamp, from, text}, ou None.
    """
    pattern = r"^\[(.*?)\]\s*(.*?):\s*(.*)$"
    match = re.match(pattern, line.strip())
    if not match:
        return None

    raw_datetime = match.group(1)  # Ex: "11/02/2025, 11:46:30"
    raw_name = match.group(2)
    message = match.group(3)

    # Converter data/hora
    dt_iso = raw_datetime
    try:
        dt_parsed = datetime.strptime(raw_datetime, "%d/%m/%Y, %H:%M:%S")
        dt_iso = dt_parsed.strftime("%Y-%m-%d %H:%M:%S")
    except:
        pass

    # Determinar se é assistente ou lead (critério simples)
    if "Dra Cristal" in raw_name:
        sender = "assistente"
    else:
        sender = "lead"

    return {
        "timestamp": dt_iso,
        "from": sender,
        "text": message
    }

def parse_chat_file(file_path, label):
    """
    Lê um _chat.txt e retorna:
    {
      'label': 'agendou' ou 'nao_agendou',
      'mensagens': [ {timestamp, from, text}, ... ]
    }
    """
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    msgs = []
    for line in lines:
        parsed = parse_line(line)
        if parsed:
            msgs.append(parsed)

    return {
        "label": label,
        "mensagens": msgs
    }

def load_labeled_history(base_dir="chatbase"):
    """
    Percorre success_cases e fail_cases, parseia cada _chat.txt.
    Retorna lista de conversas rotuladas.
    """
    all_conversations = []

    success_path = os.path.join(base_dir, "success_cases")
    fail_path = os.path.join(base_dir, "fail_cases")

    success_folders = glob.glob(os.path.join(success_path, "WhatsApp Chat - *"))
    for folder in success_folders:
        chat_file = os.path.join(folder, "_chat.txt")
        if os.path.exists(chat_file):
            conv = parse_chat_file(chat_file, label="agendou")
            all_conversations.append(conv)

    fail_folders = glob.glob(os.path.join(fail_path, "WhatsApp Chat - *"))
    for folder in fail_folders:
        chat_file = os.path.join(folder, "_chat.txt")
        if os.path.exists(chat_file):
            conv = parse_chat_file(chat_file, label="nao_agendou")
            all_conversations.append(conv)

    return all_conversations
