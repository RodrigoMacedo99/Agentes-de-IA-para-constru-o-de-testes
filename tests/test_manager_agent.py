"""
Testes para o Agente Gerenciador.
"""

import sys
import os
import json
import unittest
from unittest.mock import patch, MagicMock

# Adiciona o diretório raiz ao path para importar os módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.manager_agent import ManagerAgent
from models.task import Task
from models.question import Question


class TestManagerAgent(unittest.TestCase):
    """
    Testes para o Agente Gerenciador.
    """
    
    def setUp(self):
        """
        Configura o ambiente de teste.
        """
        self.agent = ManagerAgent()
        
        # Mock para a API de IA
        self.ai_client_mock = MagicMock()
        self.agent.ai_client = self.ai_client_mock
        
        # Dados de teste
        self.objectives = "Obj.1: Identificar critérios de qualidade e relevância dos dados."
        self.theory_text = "A qualidade dos dados é fundamental para o sucesso de projetos de ciência de dados."
    
    @patch('agents.manager_agent.save_task_data')
    def test_initialize_task(self, mock_save_task_data):
        """
        Testa a inicialização de uma tarefa.
        """
        # Configura o mock para retornar um valor simulado
        mock_save_task_data.return_value = "/path/to/task.json"
        
        # Executa o método a ser testado
        task_id = self.agent.initialize_task(self.objectives, self.theory_text)
        
        # Verifica os resultados
        self.assertIsNotNone(task_id)
        self.assertEqual(self.agent.current_task.theory_text, self.theory_text)
        self.assertEqual(len(self.agent.current_task.objectives), 1)
        self.assertEqual(self.agent.current_task.status, "created")
        
        # Verifica se o método save_task_data foi chamado
        mock_save_task_data.assert_called_once()
    
    @patch('agents.manager_agent.load_task_data')
    def test_load_task(self, mock_load_task_data):
        """
        Testa o carregamento de uma tarefa.
        """
        # Configura o mock para retornar dados simulados
        mock_task_data = {
            "id": "12345678",
            "creation_date": "2023-01-01T00:00:00",
            "objectives": ["Obj.1: Identificar critérios de qualidade e relevância dos dados."],
            "theory_text": "A qualidade dos dados é fundamental para o sucesso de projetos de ciência de dados.",
            "templates": {},
            "stopwords": [],
            "questions": [],
            "reports": [],
            "status": "created",
            "current_agent": None
        }
        mock_load_task_data.return_value = mock_task_data
        
        # Executa o método a ser testado
        result = self.agent.load_task("12345678")
        
        # Verifica os resultados
        self.assertTrue(result)
        self.assertEqual(self.agent.current_task.id, "12345678")
        self.assertEqual(self.agent.current_task.status, "created")
        
        # Verifica se o método load_task_data foi chamado
        mock_load_task_data.assert_called_once_with("12345678")
    
    @patch('agents.manager_agent.save_task_data')
    def test_assign_to_content_agent(self, mock_save_task_data):
        """
        Testa a atribuição da tarefa ao Agente Conteudista.
        """
        # Configura o mock para retornar um valor simulado
        mock_save_task_data.return_value = "/path/to/task.json"
        
        # Configura o mock para a API de IA
        mock_response = {
            "choices": [
                {
                    "message": {
                        "content": """
                        ```json
                        {
                          "objective_id": "Obj.1",
                          "type": "single_answer",
                          "context": "A qualidade dos dados é fundamental para o sucesso de projetos de ciência de dados.",
                          "statement": "Qual critério é mais importante para garantir resultados confiáveis?",
                          "alternatives": [
                            {"id": "a", "text": "A completude dos dados", "correct": true},
                            {"id": "b", "text": "O tamanho do conjunto de dados", "correct": false}
                          ],
                          "feedback": {
                            "a": "Correta. A completude dos dados é fundamental.",
                            "b": "Incorreta. A qualidade é mais importante que a quantidade."
                          }
                        }
                        ```
                        """
                    }
                }
            ]
        }
        self.ai_client_mock.generate_text.return_value = mock_response
        
        # Inicializa uma tarefa para o teste
        self.agent.initialize_task(self.objectives, self.theory_text)
        
        # Executa o método a ser testado
        success, message = self.agent.assign_to_content_agent()
        
        # Verifica os resultados
        self.assertTrue(success)
        self.assertEqual(self.agent.current_task.status, "in_progress")
        self.assertEqual(self.agent.current_task.current_agent, "content_agent")
        self.assertEqual(len(self.agent.current_task.questions), 1)
        
        # Verifica se o método save_task_data foi chamado
        mock_save_task_data.assert_called()
    
    def test_get_task_status(self):
        """
        Testa a obtenção do status da tarefa.
        """
        # Inicializa uma tarefa para o teste
        self.agent.initialize_task(self.objectives, self.theory_text)
        
        # Executa o método a ser testado
        status = self.agent.get_task_status()
        
        # Verifica os resultados
        self.assertEqual(status["status"], "created")
        self.assertIsNone(status["current_agent"])
        self.assertEqual(status["questions_count"], 0)
        self.assertEqual(status["reports_count"], 0)


if __name__ == '__main__':
    unittest.main()

