import os
from dotenv import load_dotenv

# Carrega variáveis do .env
load_dotenv()

# Acessa as chaves de API
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
#HUGGINGFACE_API_KEY = os.getenv("HUGGINGFACE_API_KEY")
