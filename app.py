"""
Aplicação principal do sistema multi-agente.
"""

import os
import json
from typing import Dict, Any, List, Optional, Tuple
from flask import Flask, request, jsonify
from flask_cors import CORS

from agents.manager_agent import ManagerAgent
from utils.file_handler import read_text, ensure_dir

import config


# Inicializa a aplicação Flask
app = Flask(__name__)
CORS(app)  # Habilita CORS para todas as rotas

# Inicializa o Agente Gerenciador
manager = ManagerAgent()


@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint para verificar se a aplicação está funcionando."""
    return jsonify({"status": "ok"})


@app.route('/task', methods=['POST'])
def create_task():
    """Endpoint para criar uma nova tarefa."""
    data = request.json
    
    if not data:
        return jsonify({"error": "Dados não fornecidos"}), 400
    
    objectives = data.get('objectives', '')
    theory_text = data.get('theory_text', '')
    
    if not objectives or not theory_text:
        return jsonify({"error": "Objetivos e fundamentação teórica são obrigatórios"}), 400
    
    # Inicializa a tarefa
    task_id = manager.initialize_task(objectives, theory_text)
    
    return jsonify({
        "task_id": task_id,
        "message": "Tarefa criada com sucesso"
    })


@app.route('/task/<task_id>', methods=['GET'])
def get_task_status(task_id):
    """Endpoint para obter o status de uma tarefa."""
    # Carrega a tarefa
    if not manager.load_task(task_id):
        return jsonify({"error": f"Tarefa {task_id} não encontrada"}), 404
    
    # Obtém o status da tarefa
    status = manager.get_task_status()
    
    return jsonify(status)


@app.route('/task/<task_id>/content', methods=['POST'])
def run_content_agent(task_id):
    """Endpoint para executar o Agente Conteudista."""
    # Carrega a tarefa
    if not manager.load_task(task_id):
        return jsonify({"error": f"Tarefa {task_id} não encontrada"}), 404
    
    # Executa o Agente Conteudista
    success, message = manager.assign_to_content_agent()
    
    if not success:
        return jsonify({"error": message}), 500
    
    return jsonify({
        "task_id": task_id,
        "message": message
    })


@app.route('/task/<task_id>/rt', methods=['POST'])
def run_rt_agent(task_id):
    """Endpoint para executar o Agente Revisor Técnico."""
    # Carrega a tarefa
    if not manager.load_task(task_id):
        return jsonify({"error": f"Tarefa {task_id} não encontrada"}), 404
    
    # Executa o Agente RT
    success, message = manager.assign_to_rt_agent()
    
    if not success:
        return jsonify({"error": message}), 500
    
    return jsonify({
        "task_id": task_id,
        "message": message
    })


@app.route('/task/<task_id>/de', methods=['POST'])
def run_de_agent(task_id):
    """Endpoint para executar o Agente Design Educacional."""
    # Carrega a tarefa
    if not manager.load_task(task_id):
        return jsonify({"error": f"Tarefa {task_id} não encontrada"}), 404
    
    # Executa o Agente DE
    success, message = manager.assign_to_de_agent()
    
    if not success:
        return jsonify({"error": message}), 500
    
    return jsonify({
        "task_id": task_id,
        "message": message
    })


@app.route('/task/<task_id>/validator', methods=['POST'])
def run_validator_agent(task_id):
    """Endpoint para executar o Agente Validador."""
    # Carrega a tarefa
    if not manager.load_task(task_id):
        return jsonify({"error": f"Tarefa {task_id} não encontrada"}), 404
    
    # Executa o Agente Validador
    success, message = manager.assign_to_validator_agent()
    
    if not success:
        return jsonify({"error": message}), 500
    
    return jsonify({
        "task_id": task_id,
        "message": message
    })


@app.route('/task/<task_id>/results', methods=['GET'])
def get_task_results(task_id):
    """Endpoint para obter os resultados finais de uma tarefa."""
    # Carrega a tarefa
    if not manager.load_task(task_id):
        return jsonify({"error": f"Tarefa {task_id} não encontrada"}), 404
    
    # Obtém os resultados da tarefa
    results = manager.get_final_results()
    
    if results["status"] == "no_task":
        return jsonify({"error": "Nenhuma tarefa inicializada"}), 404
    
    if results["status"] == "in_progress":
        return jsonify({"error": "Tarefa ainda não concluída"}), 400
    
    # Lê os arquivos de resultados
    questions_path = results.get("questions_path")
    report_path = results.get("report_path")
    document_path = results.get("document_path")
    
    questions = {}
    report = ""
    document = ""
    
    if questions_path and os.path.exists(questions_path):
        with open(questions_path, 'r', encoding='utf-8') as f:
            questions = json.load(f)
    
    if report_path and os.path.exists(report_path):
        report = read_text(report_path)
    
    if document_path and os.path.exists(document_path):
        document = read_text(document_path)
    
    return jsonify({
        "task_id": task_id,
        "status": "completed",
        "questions": questions,
        "report": report,
        "document": document
    })


@app.route('/task/<task_id>/run_all', methods=['POST'])
def run_all_agents(task_id):
    """Endpoint para executar todos os agentes em sequência."""
    # Carrega a tarefa
    if not manager.load_task(task_id):
        return jsonify({"error": f"Tarefa {task_id} não encontrada"}), 404
    
    # Executa o Agente Conteudista
    success, message = manager.assign_to_content_agent()
    if not success:
        return jsonify({"error": f"Erro no Agente Conteudista: {message}"}), 500
    
    # Executa o Agente RT
    success, message = manager.assign_to_rt_agent()
    if not success:
        return jsonify({"error": f"Erro no Agente RT: {message}"}), 500
    
    # Executa o Agente DE
    success, message = manager.assign_to_de_agent()
    if not success:
        return jsonify({"error": f"Erro no Agente DE: {message}"}), 500
    
    # Executa o Agente Validador
    success, message = manager.assign_to_validator_agent()
    if not success:
        return jsonify({"error": f"Erro no Agente Validador: {message}"}), 500
    
    # Obtém os resultados da tarefa
    results = manager.get_final_results()
    
    return jsonify({
        "task_id": task_id,
        "status": "completed",
        "message": "Todos os agentes executados com sucesso",
        "results_path": {
            "questions": results.get("questions_path"),
            "report": results.get("report_path"),
            "document": results.get("document_path")
        }
    })


@app.route('/upload', methods=['POST'])
def upload_files():
    """Endpoint para fazer upload de arquivos."""
    if 'file' not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado"}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({"error": "Nome de arquivo vazio"}), 400
    
    # Salva o arquivo no diretório de entrada
    file_path = os.path.join(config.INPUT_DIR, file.filename)
    ensure_dir(config.INPUT_DIR)
    file.save(file_path)
    
    return jsonify({
        "message": f"Arquivo {file.filename} enviado com sucesso",
        "path": file_path
    })


if __name__ == '__main__':
    # Garante que os diretórios necessários existem
    ensure_dir(config.INPUT_DIR)
    ensure_dir(config.OUTPUT_DIR)
    ensure_dir(config.TEMPLATES_DIR)
    
    # Inicia a aplicação
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)

