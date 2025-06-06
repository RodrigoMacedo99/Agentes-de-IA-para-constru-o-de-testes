"""
Utilitários para manipulação de arquivos.
"""

import os
import json
import shutil
from pathlib import Path
from typing import Dict, Any, List, Optional, Union

import config


def ensure_dir(directory: Union[str, Path]) -> Path:
    """
    Garante que o diretório existe, criando-o se necessário.
    
    Args:
        directory: Caminho do diretório
        
    Returns:
        Objeto Path do diretório
    """
    path = Path(directory)
    path.mkdir(parents=True, exist_ok=True)
    return path


def read_json(file_path: Union[str, Path]) -> Dict[str, Any]:
    """
    Lê um arquivo JSON.
    
    Args:
        file_path: Caminho do arquivo
        
    Returns:
        Dicionário com o conteúdo do arquivo
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (json.JSONDecodeError, FileNotFoundError) as e:
        print(f"Erro ao ler arquivo JSON {file_path}: {e}")
        return {}


def write_json(data: Dict[str, Any], file_path: Union[str, Path], backup: bool = True) -> bool:
    """
    Escreve dados em um arquivo JSON.
    
    Args:
        data: Dados a serem escritos
        file_path: Caminho do arquivo
        backup: Se True, cria um backup do arquivo existente
        
    Returns:
        True se a operação foi bem-sucedida, False caso contrário
    """
    file_path = Path(file_path)
    
    # Cria o diretório se não existir
    ensure_dir(file_path.parent)
    
    # Cria backup se solicitado e o arquivo existir
    if backup and file_path.exists():
        backup_path = file_path.with_suffix(f"{file_path.suffix}.bak")
        shutil.copy2(file_path, backup_path)
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"Erro ao escrever arquivo JSON {file_path}: {e}")
        return False


def read_text(file_path: Union[str, Path]) -> str:
    """
    Lê um arquivo de texto.
    
    Args:
        file_path: Caminho do arquivo
        
    Returns:
        Conteúdo do arquivo
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError as e:
        print(f"Erro ao ler arquivo de texto {file_path}: {e}")
        return ""


def write_text(text: str, file_path: Union[str, Path], backup: bool = True) -> bool:
    """
    Escreve texto em um arquivo.
    
    Args:
        text: Texto a ser escrito
        file_path: Caminho do arquivo
        backup: Se True, cria um backup do arquivo existente
        
    Returns:
        True se a operação foi bem-sucedida, False caso contrário
    """
    file_path = Path(file_path)
    
    # Cria o diretório se não existir
    ensure_dir(file_path.parent)
    
    # Cria backup se solicitado e o arquivo existir
    if backup and file_path.exists():
        backup_path = file_path.with_suffix(f"{file_path.suffix}.bak")
        shutil.copy2(file_path, backup_path)
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(text)
        return True
    except Exception as e:
        print(f"Erro ao escrever arquivo de texto {file_path}: {e}")
        return False


def list_files(directory: Union[str, Path], pattern: str = "*") -> List[Path]:
    """
    Lista arquivos em um diretório que correspondem a um padrão.
    
    Args:
        directory: Caminho do diretório
        pattern: Padrão para filtrar arquivos (glob)
        
    Returns:
        Lista de caminhos de arquivos
    """
    directory = Path(directory)
    return list(directory.glob(pattern))


def copy_file(source: Union[str, Path], destination: Union[str, Path]) -> bool:
    """
    Copia um arquivo.
    
    Args:
        source: Caminho do arquivo de origem
        destination: Caminho do arquivo de destino
        
    Returns:
        True se a operação foi bem-sucedida, False caso contrário
    """
    try:
        source = Path(source)
        destination = Path(destination)
        
        # Cria o diretório de destino se não existir
        ensure_dir(destination.parent)
        
        shutil.copy2(source, destination)
        return True
    except Exception as e:
        print(f"Erro ao copiar arquivo {source} para {destination}: {e}")
        return False


def save_task_data(task_id: str, data: Dict[str, Any]) -> str:
    """
    Salva os dados de uma tarefa.
    
    Args:
        task_id: ID da tarefa
        data: Dados da tarefa
        
    Returns:
        Caminho do arquivo salvo
    """
    file_path = config.DATA_DIR / f"task_{task_id}.json"
    write_json(data, file_path)
    return str(file_path)


def load_task_data(task_id: str) -> Dict[str, Any]:
    """
    Carrega os dados de uma tarefa.
    
    Args:
        task_id: ID da tarefa
        
    Returns:
        Dados da tarefa
    """
    file_path = config.DATA_DIR / f"task_{task_id}.json"
    return read_json(file_path)


def save_questions(task_id: str, questions: List[Dict[str, Any]]) -> str:
    """
    Salva as questões de uma tarefa.
    
    Args:
        task_id: ID da tarefa
        questions: Lista de questões
        
    Returns:
        Caminho do arquivo salvo
    """
    file_path = config.OUTPUT_DIR / f"questions_{task_id}.json"
    write_json({"questions": questions}, file_path)
    return str(file_path)


def save_report(task_id: str, report_type: str, report_content: str) -> str:
    """
    Salva um relatório.
    
    Args:
        task_id: ID da tarefa
        report_type: Tipo do relatório
        report_content: Conteúdo do relatório
        
    Returns:
        Caminho do arquivo salvo
    """
    file_path = config.OUTPUT_DIR / f"{report_type}_{task_id}.md"
    write_text(report_content, file_path)
    return str(file_path)


def save_final_document(task_id: str, document_content: str) -> str:
    """
    Salva o documento final.
    
    Args:
        task_id: ID da tarefa
        document_content: Conteúdo do documento
        
    Returns:
        Caminho do arquivo salvo
    """
    file_path = config.OUTPUT_DIR / f"final_document_{task_id}.md"
    write_text(document_content, file_path)
    return str(file_path)

