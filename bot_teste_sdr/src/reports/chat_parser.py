# src/reports/chat_parser.py

import os
import re
import glob
from datetime import datetime

def parse_line(line):
    """
    Formato: [DD/MM/YYYY, HH:MM:SS] Nome: Mensagem
    """
    pattern = r"^\[(.*?)\]\s*(.*?):\s*(.*)$"
    match = re.match(pattern, line.strip())
    if not match:
        return None

    raw_datetime = match.group(1)
    raw_name = match.group(2)
    message = match.group(3)

    dt_iso = raw_datetime
    try:
        dt_parsed = datetime.strptime(raw_datetime, "%d/%m/%Y, %H:%M:%S")
        dt_iso = dt_parsed.strftime("%Y-%m-%d %H:%M:%S")
    except:
        pass

    # Determina se é lead ou assistente
    sender = "lead"
    if any(k in raw_name.lower() for k in ["dra", "assistente", "médico"]):
        sender = "assistente"

    return {
        "timestamp": dt_iso,
        "from": sender,
        "text": message
    }

def extract_lead_id_from_folder(folder_name):
    """
    Ex.: "WhatsApp Chat - +55 11 95349-0366"
    Retorna "+55 11 95349-0366"
    """
    base = os.path.basename(folder_name)
    prefix = "WhatsApp Chat - "
    if base.startswith(prefix):
        return base[len(prefix):].strip()
    return base

def parse_chat_file(file_path, label, lead_id):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    msgs = []
    for line in lines:
        parsed = parse_line(line)
        if parsed:
            msgs.append(parsed)

    return {
        "label": label,
        "lead_id": lead_id,
        "mensagens": msgs
    }

def load_labeled_history(base_dir="assets/chatbase"):
    """
    Percorre success_cases e fail_cases, parseia cada _chat.txt
    """
    all_conversations = []

    success_path = os.path.join(base_dir, "success_cases")
    fail_path = os.path.join(base_dir, "fail_cases")

    # success => label = "agendou"
    success_folders = glob.glob(os.path.join(success_path, "WhatsApp Chat - *"))
    for folder in success_folders:
        chat_file = os.path.join(folder, "_chat.txt")
        if os.path.exists(chat_file):
            lead_id = extract_lead_id_from_folder(folder)
            conv = parse_chat_file(chat_file, "agendou", lead_id)
            all_conversations.append(conv)

    # fail => label = "nao_agendou"
    fail_folders = glob.glob(os.path.join(fail_path, "WhatsApp Chat - *"))
    for folder in fail_folders:
        chat_file = os.path.join(folder, "_chat.txt")
        if os.path.exists(chat_file):
            lead_id = extract_lead_id_from_folder(folder)
            conv = parse_chat_file(chat_file, "nao_agendou", lead_id)
            all_conversations.append(conv)

    return all_conversations
