import os
import shutil
import json
import random
from src.reports.chat_parser import load_labeled_history

BASE_RAW = "assets/chatbase"
BASE_PROCESSED = "database"
TRAIN_DIR = os.path.join(BASE_PROCESSED, "train")
TEST_DIR = os.path.join(BASE_PROCESSED, "test")
VALIDATE_DIR = os.path.join(BASE_PROCESSED, "validate")

DEFAULT_SPLIT = {
    "agendou": [4, 2, 1],  # Exemplo: 4 train, 2 test, 1 validate
    "nao_agendou": [4, 2, 2]
}

def ensure_directories():
    """ Garante que as pastas de treino, teste e validação existam. """
    for directory in [TRAIN_DIR, TEST_DIR, VALIDATE_DIR]:
        if os.path.exists(directory):
            shutil.rmtree(directory)  # Remove diretório se já existir
        os.makedirs(directory, exist_ok=True)

def split_by_labels(conversations, split_config):
    """ 
    Divide a base mantendo o equilíbrio dos rótulos.
    Exemplo de `split_config`: { "agendou": [4,2,1], "nao_agendou": [4,2,2] } 
    """
    partitions = {"train": [], "test": [], "validate": []}

    for label, (train_size, test_size, validate_size) in split_config.items():
        subset = [conv for conv in conversations if conv["label"] == label]
        random.shuffle(subset)

        train_split = subset[:train_size]
        test_split = subset[train_size:train_size + test_size]
        validate_split = subset[train_size + test_size:train_size + test_size + validate_size]

        partitions["train"].extend(train_split)
        partitions["test"].extend(test_split)
        partitions["validate"].extend(validate_split)

    return partitions

def save_partitions(partitions):
    """ Salva cada partição na pasta correta dentro de `database/` """
    for part, data in partitions.items():
        file_path = os.path.join(BASE_PROCESSED, part, "conversations.json")
        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"✅ {len(data)} conversas salvas em {file_path}")

def split_chatbase(split_config=DEFAULT_SPLIT):
    """ Organiza os chats mantendo o equilíbrio dos rótulos """
    ensure_directories()

    # Carrega todas as conversas da base RAW
    conversations = load_labeled_history(base_dir=BASE_RAW)

    # Divide conforme a configuração passada
    partitions = split_by_labels(conversations, split_config)

    # Salva os arquivos formatados na `database/`
    save_partitions(partitions)

    print(f"✅ Base dividida equilibradamente entre treino, teste e validação!")

if __name__ == "__main__":
    split_chatbase()
