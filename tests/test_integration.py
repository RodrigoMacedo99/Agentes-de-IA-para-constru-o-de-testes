"""
Testes de integração para o sistema multi-agente.
"""

import sys
import os
import json
import unittest
from unittest.mock import patch, MagicMock

# Adiciona o diretório raiz ao path para importar os módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.manager_agent import ManagerAgent
from agents.content_agent import ContentAgent
from agents.rt_agent import RTAgent
from agents.de_agent import DEAgent
from agents.validator_agent import ValidatorAgent
from utils.file_handler import read_text


class TestIntegration(unittest.TestCase):
    """
    Testes de integração para o sistema multi-agente.
    """
    
    def setUp(self):
        """
        Configura o ambiente de teste.
        """
        self.manager = ManagerAgent()
        
        # Carrega os dados de teste
        test_data_dir = os.path.join(os.path.dirname(__file__), 'test_data')
        self.objectives = read_text(os.path.join(test_data_dir, 'objectives.txt'))
        self.theory_text = read_text(os.path.join(test_data_dir, 'theory.txt'))
    
    @patch('agents.manager_agent.save_task_data')
    @patch('agents.manager_agent.save_questions')
    @patch('agents.manager_agent.save_report')
    @patch('agents.manager_agent.save_final_document')
    def test_full_workflow(self, mock_save_final_document, mock_save_report, 
                         mock_save_questions, mock_save_task_data):
        """
        Testa o fluxo completo do sistema.
        """
        # Configura os mocks para retornar valores simulados
        mock_save_task_data.return_value = "/path/to/task.json"
        mock_save_questions.return_value = "/path/to/questions.json"
        mock_save_report.return_value = "/path/to/report.md"
        mock_save_final_document.return_value = "/path/to/document.md"
        
        # Mock para a API de IA
        ai_client_mock = MagicMock()
        self.manager.ai_client = ai_client_mock
        
        # Configura o mock para retornar respostas simuladas para cada agente
        content_response = {
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
                            {"id": "b", "text": "O tamanho do conjunto de dados", "correct": false},
                            {"id": "c", "text": "A fonte dos dados", "correct": false},
                            {"id": "d", "text": "O formato de armazenamento", "correct": false},
                            {"id": "e", "text": "A idade dos dados", "correct": false}
                          ],
                          "feedback": {
                            "a": "Correta. A completude dos dados é fundamental.",
                            "b": "Incorreta. A qualidade é mais importante que a quantidade.",
                            "c": "Incorreta. A fonte não é o critério mais relevante.",
                            "d": "Incorreta. O formato tem pouca relação com a qualidade.",
                            "e": "Incorreta. A idade depende do contexto da análise."
                          }
                        }
                        ```
                        """
                    }
                }
            ]
        }
        
        rt_response = {
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
                            {"id": "b", "text": "O tamanho do conjunto de dados", "correct": false},
                            {"id": "c", "text": "A fonte dos dados", "correct": false},
                            {"id": "d", "text": "O formato de armazenamento", "correct": false},
                            {"id": "e", "text": "A idade dos dados", "correct": false}
                          ],
                          "feedback": {
                            "a": "Correta. A completude dos dados é fundamental.",
                            "b": "Incorreta. A qualidade é mais importante que a quantidade.",
                            "c": "Incorreta. A fonte não é o critério mais relevante.",
                            "d": "Incorreta. O formato tem pouca relação com a qualidade.",
                            "e": "Incorreta. A idade depende do contexto da análise."
                          },
                          "validation": {
                            "rt": {
                              "status": "approved",
                              "comments": "O conteúdo está tecnicamente correto.",
                              "checklist": {
                                "item1": {"result": "sim", "observation": "As questões abordam os conteúdos tratados"}
                              }
                            }
                          }
                        }
                        ```
                        """
                    }
                }
            ]
        }
        
        de_response = {
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
                            {"id": "b", "text": "O tamanho do conjunto de dados", "correct": false},
                            {"id": "c", "text": "A fonte dos dados", "correct": false},
                            {"id": "d", "text": "O formato de armazenamento", "correct": false},
                            {"id": "e", "text": "A idade dos dados", "correct": false}
                          ],
                          "feedback": {
                            "a": "Correta. A completude dos dados é fundamental.",
                            "b": "Incorreta. A qualidade é mais importante que a quantidade.",
                            "c": "Incorreta. A fonte não é o critério mais relevante.",
                            "d": "Incorreta. O formato tem pouca relação com a qualidade.",
                            "e": "Incorreta. A idade depende do contexto da análise."
                          },
                          "validation": {
                            "rt": {
                              "status": "approved",
                              "comments": "O conteúdo está tecnicamente correto.",
                              "checklist": {
                                "item1": {"result": "sim", "observation": "As questões abordam os conteúdos tratados"}
                              }
                            },
                            "de": {
                              "status": "approved",
                              "comments": "A questão está bem estruturada.",
                              "checklist": {
                                "item1": {"result": "sim", "observation": "O texto-base está claro"}
                              }
                            }
                          }
                        }
                        ```
                        """
                    }
                }
            ]
        }
        
        validator_response = {
            "choices": [
                {
                    "message": {
                        "content": """
                        ```json
                        {
                          "questions": [
                            {
                              "objective_id": "Obj.1",
                              "type": "single_answer",
                              "context": "A qualidade dos dados é fundamental para o sucesso de projetos de ciência de dados.",
                              "statement": "Qual critério é mais importante para garantir resultados confiáveis?",
                              "alternatives": [
                                {"id": "a", "text": "A completude dos dados", "correct": true},
                                {"id": "b", "text": "O tamanho do conjunto de dados", "correct": false},
                                {"id": "c", "text": "A fonte dos dados", "correct": false},
                                {"id": "d", "text": "O formato de armazenamento", "correct": false},
                                {"id": "e", "text": "A idade dos dados", "correct": false}
                              ],
                              "feedback": {
                                "a": "Correta. A completude dos dados é fundamental.",
                                "b": "Incorreta. A qualidade é mais importante que a quantidade.",
                                "c": "Incorreta. A fonte não é o critério mais relevante.",
                                "d": "Incorreta. O formato tem pouca relação com a qualidade.",
                                "e": "Incorreta. A idade depende do contexto da análise."
                              },
                              "validation": {
                                "rt": {
                                  "status": "approved",
                                  "comments": "O conteúdo está tecnicamente correto.",
                                  "checklist": {
                                    "item1": {"result": "sim", "observation": "As questões abordam os conteúdos tratados"}
                                  }
                                },
                                "de": {
                                  "status": "approved",
                                  "comments": "A questão está bem estruturada.",
                                  "checklist": {
                                    "item1": {"result": "sim", "observation": "O texto-base está claro"}
                                  }
                                },
                                "final": {
                                  "status": "approved",
                                  "comments": "A questão passou por todas as etapas de validação com sucesso."
                                }
                              }
                            }
                          ]
                        }
                        ```
                        
                        ```markdown
                        # Relatório de Desenvolvimento
                        
                        ## Resumo
                        
                        Este relatório descreve o processo de desenvolvimento e validação de questões educacionais.
                        ```
                        
                        ```markdown
                        # Questões Validadas
                        
                        ## Objetivo 1
                        
                        ### Questão 1 (Resposta Única)
                        
                        **Contextualização:**
                        A qualidade dos dados é fundamental para o sucesso de projetos de ciência de dados.
                        ```
                        """
                    }
                }
            ]
        }
        
        # Configura o mock para retornar diferentes respostas dependendo do prompt
        def mock_generate_text(prompt, max_tokens=2000):
            if "Conteudista" in prompt:
                return content_response
            elif "Revisor Técnico" in prompt:
                return rt_response
            elif "Designer Educacional" in prompt:
                return de_response
            elif "Validador" in prompt:
                return validator_response
            else:
                return {"choices": [{"message": {"content": "Resposta padrão"}}]}
        
        ai_client_mock.generate_text.side_effect = mock_generate_text
        
        # Executa o fluxo completo
        # 1. Inicializa a tarefa
        task_id = self.manager.initialize_task(self.objectives, self.theory_text)
        self.assertIsNotNone(task_id)
        
        # 2. Executa o Agente Conteudista
        success, message = self.manager.assign_to_content_agent()
        self.assertTrue(success)
        self.assertEqual(len(self.manager.current_task.questions), 1)
        
        # 3. Executa o Agente RT
        success, message = self.manager.assign_to_rt_agent()
        self.assertTrue(success)
        self.assertIn("rt", self.manager.current_task.questions[0].validation)
        
        # 4. Executa o Agente DE
        success, message = self.manager.assign_to_de_agent()
        self.assertTrue(success)
        self.assertIn("de", self.manager.current_task.questions[0].validation)
        
        # 5. Executa o Agente Validador
        success, message = self.manager.assign_to_validator_agent()
        self.assertTrue(success)
        self.assertEqual(self.manager.current_task.status, "completed")
        
        # Verifica se os métodos de salvamento foram chamados
        mock_save_task_data.assert_called()
        mock_save_questions.assert_called_once()
        mock_save_report.assert_called_once()
        mock_save_final_document.assert_called_once()


if __name__ == '__main__':
    unittest.main()

