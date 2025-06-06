"""
Testes para o Agente Conteudista.
"""

import sys
import os
import json
import unittest
from unittest.mock import patch, MagicMock

# Adiciona o diretório raiz ao path para importar os módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.content_agent import ContentAgent
from models.question import Question


class TestContentAgent(unittest.TestCase):
    """
    Testes para o Agente Conteudista.
    """
    
    def setUp(self):
        """
        Configura o ambiente de teste.
        """
        self.agent = ContentAgent()
        
        # Mock para a API de IA
        self.ai_client_mock = MagicMock()
        self.agent.ai_client = self.ai_client_mock
        
        # Dados de teste
        self.objectives = ["Obj.1: Identificar critérios de qualidade e relevância dos dados."]
        self.theory_text = "A qualidade dos dados é fundamental para o sucesso de projetos de ciência de dados."
        self.templates = {
            "single_answer": json.dumps({
                "type": "single_answer",
                "context": "Texto de contextualização...",
                "statement": "Enunciado da questão...",
                "alternatives": [
                    {"id": "a", "text": "Alternativa A", "correct": True},
                    {"id": "b", "text": "Alternativa B", "correct": False}
                ],
                "feedback": {
                    "a": "Correta. Justificativa...",
                    "b": "Incorreta. Justificativa..."
                }
            })
        }
        self.stopwords = ["limita-se", "apenas", "somente"]
    
    def test_create_questions(self):
        """
        Testa a criação de questões.
        """
        # Configura o mock para retornar uma resposta simulada
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
        
        # Executa o método a ser testado
        questions = self.agent.create_questions(
            self.objectives,
            self.theory_text,
            self.templates,
            self.stopwords
        )
        
        # Verifica os resultados
        self.assertEqual(len(questions), 1)
        self.assertEqual(questions[0].objective_id, "Obj.1")
        self.assertEqual(questions[0].type, "single_answer")
        self.assertEqual(len(questions[0].alternatives), 2)
        self.assertTrue(questions[0].alternatives[0]["correct"])
        self.assertFalse(questions[0].alternatives[1]["correct"])
    
    def test_check_and_replace_restricted_words(self):
        """
        Testa a verificação e substituição de palavras restritivas.
        """
        # Dados de teste
        question_data = {
            "context": "Este texto limita-se a explicar os conceitos básicos.",
            "statement": "O que é importante considerar? Apenas os dados completos.",
            "alternatives": [
                {"id": "a", "text": "Somente a qualidade dos dados.", "correct": True},
                {"id": "b", "text": "A quantidade de dados.", "correct": False}
            ],
            "feedback": {
                "a": "Correta. Limita-se à qualidade dos dados.",
                "b": "Incorreta. Não apenas a quantidade."
            }
        }
        
        # Executa o método a ser testado
        self.agent._check_and_replace_restricted_words(question_data, self.stopwords)
        
        # Verifica os resultados
        self.assertNotIn("limita-se", question_data["context"])
        self.assertNotIn("Apenas", question_data["statement"])
        self.assertNotIn("Somente", question_data["alternatives"][0]["text"])
        self.assertNotIn("Limita-se", question_data["feedback"]["a"])
        self.assertNotIn("apenas", question_data["feedback"]["b"])


if __name__ == '__main__':
    unittest.main()

