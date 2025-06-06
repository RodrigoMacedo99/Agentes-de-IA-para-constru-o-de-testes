"""
Configurações do sistema multi-agente.
"""

import os
from pathlib import Path


# Diretórios
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
INPUT_DIR = DATA_DIR / "input"
OUTPUT_DIR = DATA_DIR / "output"
TEMPLATES_DIR = BASE_DIR / "templates"

# Configurações da API de IA
AI_PROVIDER = os.environ.get("AI_PROVIDER", "deepseek")  # deepseek ou ollama
DEEPSEEK_API_KEY = os.environ.get("AIzaSyB90wp4nTjAmmOv50RJM1t7FPlKJ7xQV9A", "")
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"
OLLAMA_API_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "deepseek-coder:6.7b")

# Configurações do servidor
HOST = "0.0.0.0"
PORT = int(os.environ.get("PORT", 5000))
DEBUG = os.environ.get("DEBUG", "False").lower() == "true"

# Configurações de logging
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
LOG_FILE = BASE_DIR / "logs" / "app.log"

# Configurações de timeout
REQUEST_TIMEOUT = 120  # segundos

