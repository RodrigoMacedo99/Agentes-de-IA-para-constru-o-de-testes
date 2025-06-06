"""
Testes para a API REST.
"""

import sys
import os
import json
import unittest
from unittest.mock import patch, MagicMock

# Adiciona o diretório raiz ao path para importar os módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import app


class TestAPI(unittest.TestCase):
    """
    Testes para a API REST.
    """
    
    def setUp(self):
        """
        Configura o ambiente de teste.
        """
        app.app.testing = True
        self.client = app.app.test_client()
        
        # Mock para o Agente Gerenciador
        self.manager_mock = MagicMock()
        app.manager = self.manager_mock
    
    def test_health_check(self):
        """
        Testa o endpoint de verificação de saúde.
        """
        response = self.client.get('/health')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data["status"], "ok")
    
    def test_create_task(self):
        """
        Testa o endpoint de criação de tarefa.
        """
        # Configura o mock para retornar um valor simulado
        self.manager_mock.initialize_task.return_value = "12345678"
        
        # Dados de teste
        data = {
            "objectives": "Obj.1: Identificar critérios de qualidade e relevância dos dados.",
            "theory_text": "A qualidade dos dados é fundamental para o sucesso de projetos de ciência de dados."
        }
        
        # Executa a requisição
        response = self.client.post('/task', json=data)
        result = json.loads(response.data)
        
        # Verifica os resultados
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["task_id"], "12345678")
        self.assertEqual(result["message"], "Tarefa criada com sucesso")
        
        # Verifica se o método initialize_task foi chamado com os argumentos corretos
        self.manager_mock.initialize_task.assert_called_once_with(
            data["objectives"],
            data["theory_text"]
        )
    
    def test_create_task_missing_data(self):
        """
        Testa o endpoint de criação de tarefa com dados ausentes.
        """
        # Dados de teste incompletos
        data = {
            "objectives": "Obj.1: Identificar critérios de qualidade e relevância dos dados."
            # theory_text está ausente
        }
        
        # Executa a requisição
        response = self.client.post('/task', json=data)
        result = json.loads(response.data)
        
        # Verifica os resultados
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", result)
    
    def test_get_task_status(self):
        """
        Testa o endpoint de obtenção do status da tarefa.
        """
        # Configura o mock para retornar valores simulados
        self.manager_mock.load_task.return_value = True
        self.manager_mock.get_task_status.return_value = {
            "task_id": "12345678",
            "status": "in_progress",
            "current_agent": "content_agent",
            "questions_count": 1,
            "reports_count": 0
        }
        
        # Executa a requisição
        response = self.client.get('/task/12345678')
        result = json.loads(response.data)
        
        # Verifica os resultados
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["status"], "in_progress")
        self.assertEqual(result["current_agent"], "content_agent")
        self.assertEqual(result["questions_count"], 1)
        
        # Verifica se os métodos foram chamados com os argumentos corretos
        self.manager_mock.load_task.assert_called_once_with("12345678")
        self.manager_mock.get_task_status.assert_called_once()
    
    def test_get_task_status_not_found(self):
        """
        Testa o endpoint de obtenção do status da tarefa quando a tarefa não existe.
        """
        # Configura o mock para retornar False (tarefa não encontrada)
        self.manager_mock.load_task.return_value = False
        
        # Executa a requisição
        response = self.client.get('/task/12345678')
        result = json.loads(response.data)
        
        # Verifica os resultados
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", result)
    
    def test_run_content_agent(self):
        """
        Testa o endpoint de execução do Agente Conteudista.
        """
        # Configura o mock para retornar valores simulados
        self.manager_mock.load_task.return_value = True
        self.manager_mock.assign_to_content_agent.return_value = (True, "Criadas 1 questões")
        
        # Executa a requisição
        response = self.client.post('/task/12345678/content')
        result = json.loads(response.data)
        
        # Verifica os resultados
        self.assertEqual(response.status_code, 200)
        self.assertEqual(result["task_id"], "12345678")
        self.assertEqual(result["message"], "Criadas 1 questões")
        
        # Verifica se os métodos foram chamados com os argumentos corretos
        self.manager_mock.load_task.assert_called_once_with("12345678")
        self.manager_mock.assign_to_content_agent.assert_called_once()
    
    def test_run_content_agent_error(self):
        """
        Testa o endpoint de execução do Agente Conteudista quando ocorre um erro.
        """
        # Configura o mock para retornar valores simulados
        self.manager_mock.load_task.return_value = True
        self.manager_mock.assign_to_content_agent.return_value = (False, "Erro ao criar questões")
        
        # Executa a requisição
        response = self.client.post('/task/12345678/content')
        result = json.loads(response.data)
        
        # Verifica os resultados
        self.assertEqual(response.status_code, 500)
        self.assertEqual(result["error"], "Erro ao criar questões")


if __name__ == '__main__':
    unittest.main()

