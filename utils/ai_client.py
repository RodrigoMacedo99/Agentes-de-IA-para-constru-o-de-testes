"""
Cliente para interagir com APIs de IA.
"""

import os
import json
import requests
from typing import Dict, Any, List, Optional

import config


class AIClient:
    """
    Cliente para interagir com APIs de IA.
    """
    
    def __init__(self):
        """
        Inicializa o cliente de API de IA.
        """
        self.provider = config.AI_PROVIDER
        
        if self.provider == "deepseek":
            self.api_key = config.DEEPSEEK_API_KEY
            self.api_url = config.DEEPSEEK_API_URL
        elif self.provider == "ollama":
            self.api_url = config.OLLAMA_API_URL
            self.model = config.OLLAMA_MODEL
        else:
            raise ValueError(f"Provedor de IA não suportado: {self.provider}")
    
    def generate_text(self, prompt: str, max_tokens: int = 2000) -> Dict[str, Any]:
        """
        Gera texto usando a API de IA.
        
        Args:
            prompt: Prompt para a API
            max_tokens: Número máximo de tokens a serem gerados
            
        Returns:
            Resposta da API
        """
        if self.provider == "deepseek":
            return self._generate_text_deepseek(prompt, max_tokens)
        elif self.provider == "ollama":
            return self._generate_text_ollama(prompt, max_tokens)
        else:
            raise ValueError(f"Provedor de IA não suportado: {self.provider}")
    
    def _generate_text_deepseek(self, prompt: str, max_tokens: int = 2000) -> Dict[str, Any]:
        """
        Gera texto usando a API DeepSeek.
        
        Args:
            prompt: Prompt para a API
            max_tokens: Número máximo de tokens a serem gerados
            
        Returns:
            Resposta da API
        """
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        data = {
            "model": "deepseek-chat",
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "max_tokens": max_tokens,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(
                self.api_url,
                headers=headers,
                json=data,
                timeout=config.REQUEST_TIMEOUT
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"Erro ao chamar a API DeepSeek: {e}")
            # Retorna uma resposta simulada para desenvolvimento
            return self._get_mock_response(prompt)
    
    def _generate_text_ollama(self, prompt: str, max_tokens: int = 2000) -> Dict[str, Any]:
        """
        Gera texto usando a API Ollama.
        
        Args:
            prompt: Prompt para a API
            max_tokens: Número máximo de tokens a serem gerados
            
        Returns:
            Resposta da API
        """
        data = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "num_predict": max_tokens,
                "temperature": 0.7
            }
        }
        
        try:
            response = requests.post(
                self.api_url,
                json=data,
                timeout=config.REQUEST_TIMEOUT
            )
            response.raise_for_status()
            
            # Converte a resposta do Ollama para o formato do DeepSeek
            ollama_response = response.json()
            return {
                "choices": [
                    {
                        "message": {
                            "role": "assistant",
                            "content": ollama_response.get("response", "")
                        }
                    }
                ]
            }
        except requests.exceptions.RequestException as e:
            print(f"Erro ao chamar a API Ollama: {e}")
            # Retorna uma resposta simulada para desenvolvimento
            return self._get_mock_response(prompt)
    
    def _get_mock_response(self, prompt: str) -> Dict[str, Any]:
        """
        Gera uma resposta simulada para desenvolvimento.
        
        Args:
            prompt: Prompt para a API
            
        Returns:
            Resposta simulada
        """
        # Verifica o tipo de agente no prompt
        if "Conteudista" in prompt:
            return self._get_mock_content_response()
        elif "Revisor Técnico" in prompt:
            return self._get_mock_rt_response()
        elif "Design Educacional" in prompt:
            return self._get_mock_de_response()
        elif "Validador" in prompt:
            return self._get_mock_validator_response()
        else:
            return {
                "choices": [
                    {
                        "message": {
                            "role": "assistant",
                            "content": "Esta é uma resposta simulada para desenvolvimento."
                        }
                    }
                ]
            }
    
    def _get_mock_content_response(self) -> Dict[str, Any]:
        """
        Gera uma resposta simulada para o Agente Conteudista.
        
        Returns:
            Resposta simulada
        """
        return {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": """
                        ```json
                        {
                          "objective_id": "Obj.1",
                          "type": "single_answer",
                          "context": "A qualidade dos dados é fundamental para o sucesso de projetos de ciência de dados e análise. Dados de alta qualidade são caracterizados por sua precisão, completude, consistência e relevância para o problema em questão.",
                          "statement": "Ao avaliar a qualidade de um conjunto de dados para um projeto de análise, qual dos seguintes critérios é mais importante para garantir resultados confiáveis?",
                          "alternatives": [
                            {"id": "a", "text": "A completude dos dados, garantindo que não existam valores ausentes que possam comprometer a análise", "correct": true},
                            {"id": "b", "text": "O tamanho do conjunto de dados, priorizando sempre a maior quantidade possível de registros", "correct": false},
                            {"id": "c", "text": "A fonte dos dados, dando preferência para dados coletados internamente pela organização", "correct": false},
                            {"id": "d", "text": "O formato de armazenamento dos dados, priorizando formatos proprietários mais seguros", "correct": false},
                            {"id": "e", "text": "A idade dos dados, utilizando principalmente dados históricos para análises preditivas", "correct": false}
                          ],
                          "feedback": {
                            "a": "Correta. A completude dos dados é um critério fundamental de qualidade, pois valores ausentes podem distorcer análises e levar a conclusões incorretas. Dados completos permitem análises mais precisas e confiáveis.",
                            "b": "Incorreta. Embora o tamanho do conjunto de dados seja relevante, a qualidade é mais importante que a quantidade. Um conjunto de dados grande, mas com problemas de qualidade, pode levar a resultados menos confiáveis que um conjunto menor e de alta qualidade.",
                            "c": "Incorreta. A fonte dos dados é importante, mas não é o critério mais relevante para a qualidade. Dados externos podem ser tão ou mais valiosos que dados internos, dependendo do contexto e da confiabilidade da fonte.",
                            "d": "Incorreta. O formato de armazenamento tem pouca relação com a qualidade intrínseca dos dados. Formatos abertos podem ser tão seguros e úteis quanto formatos proprietários, e a escolha depende mais das necessidades de processamento.",
                            "e": "Incorreta. A idade dos dados deve ser avaliada conforme o contexto da análise. Dados recentes podem ser mais relevantes para muitas análises, enquanto dados históricos são essenciais para análises de tendências ou sazonalidade."
                          }
                        }
                        ```
                        """
                    }
                }
            ]
        }
    
    def _get_mock_rt_response(self) -> Dict[str, Any]:
        """
        Gera uma resposta simulada para o Agente RT.
        
        Returns:
            Resposta simulada
        """
        return {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": """
                        ```json
                        {
                          "objective_id": "Obj.1",
                          "type": "single_answer",
                          "context": "A qualidade dos dados é fundamental para o sucesso de projetos de ciência de dados e análise. Dados de alta qualidade são caracterizados por sua precisão, completude, consistência e relevância para o problema em questão.",
                          "statement": "Ao avaliar a qualidade de um conjunto de dados para um projeto de análise, qual dos seguintes critérios é mais importante para garantir resultados confiáveis?",
                          "alternatives": [
                            {"id": "a", "text": "A completude dos dados, garantindo que não existam valores ausentes que possam comprometer a análise", "correct": true},
                            {"id": "b", "text": "O tamanho do conjunto de dados, priorizando sempre a maior quantidade possível de registros", "correct": false},
                            {"id": "c", "text": "A fonte dos dados, dando preferência para dados coletados internamente pela organização", "correct": false},
                            {"id": "d", "text": "O formato de armazenamento dos dados, priorizando formatos proprietários mais seguros", "correct": false},
                            {"id": "e", "text": "A idade dos dados, utilizando principalmente dados históricos para análises preditivas", "correct": false}
                          ],
                          "feedback": {
                            "a": "Correta. A completude dos dados é um critério fundamental de qualidade, pois valores ausentes podem distorcer análises e levar a conclusões incorretas. Dados completos permitem análises mais precisas e confiáveis.",
                            "b": "Incorreta. Embora o tamanho do conjunto de dados seja relevante, a qualidade é mais importante que a quantidade. Um conjunto de dados grande, mas com problemas de qualidade, pode levar a resultados menos confiáveis que um conjunto menor e de alta qualidade.",
                            "c": "Incorreta. A fonte dos dados é importante, mas não é o critério mais relevante para a qualidade. Dados externos podem ser tão ou mais valiosos que dados internos, dependendo do contexto e da confiabilidade da fonte.",
                            "d": "Incorreta. O formato de armazenamento tem pouca relação com a qualidade intrínseca dos dados. Formatos abertos podem ser tão seguros e úteis quanto formatos proprietários, e a escolha depende mais das necessidades de processamento.",
                            "e": "Incorreta. A idade dos dados deve ser avaliada conforme o contexto da análise. Dados recentes podem ser mais relevantes para muitas análises, enquanto dados históricos são essenciais para análises de tendências ou sazonalidade."
                          },
                          "validation": {
                            "rt": {
                              "status": "approved",
                              "comments": "O conteúdo está tecnicamente correto e alinhado com as práticas de ciência de dados.",
                              "checklist": {
                                "item1": {"result": "sim", "observation": "As questões abordam os conteúdos tratados nas UAs correspondentes"},
                                "item2": {"result": "sim", "observation": "Os objetivos de aprendizagem estão alinhados com o PAA"},
                                "item3": {"result": "sim", "observation": "A questão permite avaliar a aprendizagem a partir do objetivo associado"}
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
    
    def _get_mock_de_response(self) -> Dict[str, Any]:
        """
        Gera uma resposta simulada para o Agente DE.
        
        Returns:
            Resposta simulada
        """
        return {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": """
                        ```json
                        {
                          "objective_id": "Obj.1",
                          "type": "single_answer",
                          "context": "A qualidade dos dados é fundamental para o sucesso de projetos de ciência de dados e análise. Dados de alta qualidade são caracterizados por sua precisão, completude, consistência e relevância para o problema em questão.",
                          "statement": "Ao avaliar a qualidade de um conjunto de dados para um projeto de análise, qual dos seguintes critérios é mais importante para garantir resultados confiáveis?",
                          "alternatives": [
                            {"id": "a", "text": "A completude dos dados, garantindo que não existam valores ausentes que possam comprometer a análise", "correct": true},
                            {"id": "b", "text": "O tamanho do conjunto de dados, priorizando sempre a maior quantidade possível de registros", "correct": false},
                            {"id": "c", "text": "A fonte dos dados, dando preferência para dados coletados internamente pela organização", "correct": false},
                            {"id": "d", "text": "O formato de armazenamento dos dados, priorizando formatos proprietários mais seguros", "correct": false},
                            {"id": "e", "text": "A idade dos dados, utilizando principalmente dados históricos para análises preditivas", "correct": false}
                          ],
                          "feedback": {
                            "a": "Correta. A completude dos dados é um critério fundamental de qualidade, pois valores ausentes podem distorcer análises e levar a conclusões incorretas. Dados completos permitem análises mais precisas e confiáveis.",
                            "b": "Incorreta. Embora o tamanho do conjunto de dados seja relevante, a qualidade é mais importante que a quantidade. Um conjunto de dados grande, mas com problemas de qualidade, pode levar a resultados menos confiáveis que um conjunto menor e de alta qualidade.",
                            "c": "Incorreta. A fonte dos dados é importante, mas não é o critério mais relevante para a qualidade. Dados externos podem ser tão ou mais valiosos que dados internos, dependendo do contexto e da confiabilidade da fonte.",
                            "d": "Incorreta. O formato de armazenamento tem pouca relação com a qualidade intrínseca dos dados. Formatos abertos podem ser tão seguros e úteis quanto formatos proprietários, e a escolha depende mais das necessidades de processamento.",
                            "e": "Incorreta. A idade dos dados deve ser avaliada conforme o contexto da análise. Dados recentes podem ser mais relevantes para muitas análises, enquanto dados históricos são essenciais para análises de tendências ou sazonalidade."
                          },
                          "validation": {
                            "rt": {
                              "status": "approved",
                              "comments": "O conteúdo está tecnicamente correto e alinhado com as práticas de ciência de dados.",
                              "checklist": {
                                "item1": {"result": "sim", "observation": "As questões abordam os conteúdos tratados nas UAs correspondentes"},
                                "item2": {"result": "sim", "observation": "Os objetivos de aprendizagem estão alinhados com o PAA"},
                                "item3": {"result": "sim", "observation": "A questão permite avaliar a aprendizagem a partir do objetivo associado"}
                              }
                            },
                            "de": {
                              "status": "approved",
                              "comments": "A questão está bem estruturada e segue o template adequadamente.",
                              "checklist": {
                                "item1": {"result": "sim", "observation": "O texto-base está claro e sem ambiguidades"},
                                "item2": {"result": "sim", "observation": "O texto-base dá suporte para a resolução da questão"},
                                "item3": {"result": "sim", "observation": "Os feedbacks justificam o porquê do acerto ou erro de forma clara"}
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
    
    def _get_mock_validator_response(self) -> Dict[str, Any]:
        """
        Gera uma resposta simulada para o Agente Validador.
        
        Returns:
            Resposta simulada
        """
        return {
            "choices": [
                {
                    "message": {
                        "role": "assistant",
                        "content": """
                        ```json
                        {
                          "questions": [
                            {
                              "objective_id": "Obj.1",
                              "type": "single_answer",
                              "context": "A qualidade dos dados é fundamental para o sucesso de projetos de ciência de dados e análise. Dados de alta qualidade são caracterizados por sua precisão, completude, consistência e relevância para o problema em questão.",
                              "statement": "Ao avaliar a qualidade de um conjunto de dados para um projeto de análise, qual dos seguintes critérios é mais importante para garantir resultados confiáveis?",
                              "alternatives": [
                                {"id": "a", "text": "A completude dos dados, garantindo que não existam valores ausentes que possam comprometer a análise", "correct": true},
                                {"id": "b", "text": "O tamanho do conjunto de dados, priorizando sempre a maior quantidade possível de registros", "correct": false},
                                {"id": "c", "text": "A fonte dos dados, dando preferência para dados coletados internamente pela organização", "correct": false},
                                {"id": "d", "text": "O formato de armazenamento dos dados, priorizando formatos proprietários mais seguros", "correct": false},
                                {"id": "e", "text": "A idade dos dados, utilizando principalmente dados históricos para análises preditivas", "correct": false}
                              ],
                              "feedback": {
                                "a": "Correta. A completude dos dados é um critério fundamental de qualidade, pois valores ausentes podem distorcer análises e levar a conclusões incorretas. Dados completos permitem análises mais precisas e confiáveis.",
                                "b": "Incorreta. Embora o tamanho do conjunto de dados seja relevante, a qualidade é mais importante que a quantidade. Um conjunto de dados grande, mas com problemas de qualidade, pode levar a resultados menos confiáveis que um conjunto menor e de alta qualidade.",
                                "c": "Incorreta. A fonte dos dados é importante, mas não é o critério mais relevante para a qualidade. Dados externos podem ser tão ou mais valiosos que dados internos, dependendo do contexto e da confiabilidade da fonte.",
                                "d": "Incorreta. O formato de armazenamento tem pouca relação com a qualidade intrínseca dos dados. Formatos abertos podem ser tão seguros e úteis quanto formatos proprietários, e a escolha depende mais das necessidades de processamento.",
                                "e": "Incorreta. A idade dos dados deve ser avaliada conforme o contexto da análise. Dados recentes podem ser mais relevantes para muitas análises, enquanto dados históricos são essenciais para análises de tendências ou sazonalidade."
                              },
                              "validation": {
                                "rt": {
                                  "status": "approved",
                                  "comments": "O conteúdo está tecnicamente correto e alinhado com as práticas de ciência de dados.",
                                  "checklist": {
                                    "item1": {"result": "sim", "observation": "As questões abordam os conteúdos tratados nas UAs correspondentes"},
                                    "item2": {"result": "sim", "observation": "Os objetivos de aprendizagem estão alinhados com o PAA"},
                                    "item3": {"result": "sim", "observation": "A questão permite avaliar a aprendizagem a partir do objetivo associado"}
                                  }
                                },
                                "de": {
                                  "status": "approved",
                                  "comments": "A questão está bem estruturada e segue o template adequadamente.",
                                  "checklist": {
                                    "item1": {"result": "sim", "observation": "O texto-base está claro e sem ambiguidades"},
                                    "item2": {"result": "sim", "observation": "O texto-base dá suporte para a resolução da questão"},
                                    "item3": {"result": "sim", "observation": "Os feedbacks justificam o porquê do acerto ou erro de forma clara"}
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
                        
                        Este relatório descreve o processo de desenvolvimento e validação de questões educacionais utilizando um sistema multi-agente. O processo envolveu quatro agentes especializados: Conteudista, Revisor Técnico (RT), Design Educacional (DE) e Validador, cada um com responsabilidades específicas na criação e validação das questões.
                        
                        ## Etapas do Processo
                        
                        ### Agente Conteudista
                        
                        O Agente Conteudista foi responsável pela criação inicial das questões com base nos objetivos de aprendizagem e na fundamentação teórica fornecida. Ele elaborou questões de resposta única que avaliam a compreensão e aplicação dos conceitos, evitando a memorização.
                        
                        **Observações:** As questões criadas seguiram o template fornecido e abordaram adequadamente os objetivos de aprendizagem.
                        
                        ### Agente Revisor Técnico (RT)
                        
                        O Agente RT validou a precisão técnica do conteúdo das questões, verificando se estavam alinhadas com os objetivos de aprendizagem e se apresentavam informações tecnicamente corretas.
                        
                        **Observações:** Todas as questões foram aprovadas pelo RT, confirmando sua precisão técnica e alinhamento com os objetivos.
                        
                        ### Agente Design Educacional (DE)
                        
                        O Agente DE validou a estrutura e qualidade pedagógica das questões, verificando clareza, formato adequado e ausência de ambiguidades ou inconsistências.
                        
                        **Observações:** As questões foram aprovadas pelo DE, confirmando sua qualidade pedagógica e estrutural.
                        
                        ## Recomendações para Melhoria do Prompt
                        
                        1. Incluir exemplos específicos de questões bem elaboradas para cada tipo (resposta única, múltipla escolha, asserção-razão).
                        2. Fornecer diretrizes mais detalhadas sobre como elaborar feedbacks construtivos para cada alternativa.
                        3. Incluir orientações sobre como adaptar as questões para diferentes níveis de dificuldade.
                        ```
                        
                        ```markdown
                        # Questões Validadas
                        
                        ## Objetivo 1: Identificar critérios de qualidade e relevância dos dados, como completude, consistência e ausência de vieses.
                        
                        ### Questão 1 (Resposta Única)
                        
                        **Contextualização:**
                        A qualidade dos dados é fundamental para o sucesso de projetos de ciência de dados e análise. Dados de alta qualidade são caracterizados por sua precisão, completude, consistência e relevância para o problema em questão.
                        
                        **Enunciado:**
                        Ao avaliar a qualidade de um conjunto de dados para um projeto de análise, qual dos seguintes critérios é mais importante para garantir resultados confiáveis?
                        
                        **Alternativas:**
                        a) A completude dos dados, garantindo que não existam valores ausentes que possam comprometer a análise
                        b) O tamanho do conjunto de dados, priorizando sempre a maior quantidade possível de registros
                        c) A fonte dos dados, dando preferência para dados coletados internamente pela organização
                        d) O formato de armazenamento dos dados, priorizando formatos proprietários mais seguros
                        e) A idade dos dados, utilizando principalmente dados históricos para análises preditivas
                        
                        **Feedback:**
                        a) Correta. A completude dos dados é um critério fundamental de qualidade, pois valores ausentes podem distorcer análises e levar a conclusões incorretas. Dados completos permitem análises mais precisas e confiáveis.
                        b) Incorreta. Embora o tamanho do conjunto de dados seja relevante, a qualidade é mais importante que a quantidade. Um conjunto de dados grande, mas com problemas de qualidade, pode levar a resultados menos confiáveis que um conjunto menor e de alta qualidade.
                        c) Incorreta. A fonte dos dados é importante, mas não é o critério mais relevante para a qualidade. Dados externos podem ser tão ou mais valiosos que dados internos, dependendo do contexto e da confiabilidade da fonte.
                        d) Incorreta. O formato de armazenamento tem pouca relação com a qualidade intrínseca dos dados. Formatos abertos podem ser tão seguros e úteis quanto formatos proprietários, e a escolha depende mais das necessidades de processamento.
                        e) Incorreta. A idade dos dados deve ser avaliada conforme o contexto da análise. Dados recentes podem ser mais relevantes para muitas análises, enquanto dados históricos são essenciais para análises de tendências ou sazonalidade.
                        ```
                        """
                    }
                }
            ]
        }
    
    def create_agent_prompt(self, agent_type: str, task_data: Dict[str, Any]) -> str:
        """
        Cria um prompt para um agente específico.
        
        Args:
            agent_type: Tipo de agente (content, rt, de, validator)
            task_data: Dados da tarefa
            
        Returns:
            Prompt formatado
        """
        if agent_type == "content":
            return self._create_content_agent_prompt(task_data)
        elif agent_type == "rt":
            return self._create_rt_agent_prompt(task_data)
        elif agent_type == "de":
            return self._create_de_agent_prompt(task_data)
        elif agent_type == "validator":
            return self._create_validator_agent_prompt(task_data)
        else:
            raise ValueError(f"Tipo de agente não suportado: {agent_type}")
    
    def _create_content_agent_prompt(self, task_data: Dict[str, Any]) -> str:
        """
        Cria um prompt para o Agente Conteudista.
        
        Args:
            task_data: Dados da tarefa
            
        Returns:
            Prompt formatado
        """
        return f"""
        Você é um Professor-Conteudista especializado em elaborar questões educacionais de alta qualidade.
        
        OBJETIVOS DE APRENDIZAGEM:
        {task_data["objectives"]}
        
        FUNDAMENTAÇÃO TEÓRICA:
        {task_data["theory"]}
        
        TEMPLATES DE QUESTÕES:
        {task_data["template"]}
        
        PALAVRAS A EVITAR (não use estas palavras ou similares):
        {task_data["stopwords"]}
        
        INSTRUÇÕES:
        1. Elabore UMA questão para CADA objetivo de aprendizagem fornecido.
        2. Siga rigorosamente o formato dos templates fornecidos.
        3. Evite usar palavras restritivas listadas acima.
        4. Crie questões que avaliem compreensão e aplicação, não memorização.
        5. Forneça feedback detalhado para cada alternativa.
        6. Cada questão deve ter exatamente 5 alternativas (a, b, c, d, e), sendo apenas uma correta.
        7. Todas as alternativas devem ter extensão semelhante.
        
        Por favor, elabore as questões no formato JSON seguindo a estrutura dos templates fornecidos.
        """
    
    def _create_rt_agent_prompt(self, task_data: Dict[str, Any]) -> str:
        """
        Cria um prompt para o Agente RT.
        
        Args:
            task_data: Dados da tarefa
            
        Returns:
            Prompt formatado
        """
        return f"""
        Você é um Revisor Técnico especializado em validar a precisão técnica de questões educacionais.
        
        QUESTÕES A SEREM REVISADAS:
        {json.dumps(task_data["questions"], ensure_ascii=False, indent=2)}
        
        CHECKLIST DE VALIDAÇÃO RT:
        {task_data["rt_checklist"]}
        
        PALAVRAS A EVITAR (verifique e substitua estas palavras ou similares):
        {task_data["stopwords"]}
        
        INSTRUÇÕES:
        1. Analise cada questão quanto à precisão técnica do conteúdo.
        2. Verifique se as questões estão alinhadas com os objetivos de aprendizagem.
        3. Identifique e corrija quaisquer erros técnicos ou conceituais.
        4. Substitua palavras restritivas por alternativas mais adequadas.
        5. Preencha o checklist de validação para cada questão.
        
        Por favor, retorne as questões revisadas no mesmo formato JSON, adicionando um campo "validation.rt" com o resultado da sua análise para cada questão.
        
        Exemplo de formato para o campo validation.rt:
        ```json
        "validation": {{
          "rt": {{
            "status": "approved",
            "comments": "O conteúdo está tecnicamente correto e alinhado com as práticas de ciência de dados.",
            "checklist": {{
              "item1": {{"result": "sim", "observation": "As questões abordam os conteúdos tratados nas UAs correspondentes"}},
              "item2": {{"result": "sim", "observation": "Os objetivos de aprendizagem estão alinhados com o PAA"}},
              ...
            }}
          }}
        }}
        ```
        """
    
    def _create_de_agent_prompt(self, task_data: Dict[str, Any]) -> str:
        """
        Cria um prompt para o Agente DE.
        
        Args:
            task_data: Dados da tarefa
            
        Returns:
            Prompt formatado
        """
        return f"""
        Você é um Designer Educacional especializado em validar a estrutura e qualidade pedagógica de questões educacionais.
        
        QUESTÕES A SEREM REVISADAS:
        {json.dumps(task_data["questions"], ensure_ascii=False, indent=2)}
        
        CHECKLIST DE VALIDAÇÃO DE:
        {task_data["de_checklist"]}
        
        PALAVRAS A EVITAR (verifique e substitua estas palavras ou similares):
        {task_data["stopwords"]}
        
        INSTRUÇÕES:
        1. Analise cada questão quanto à clareza, estrutura e qualidade pedagógica.
        2. Verifique se as questões seguem o formato adequado.
        3. Identifique e corrija problemas de redação, ambiguidades ou inconsistências.
        4. Substitua palavras restritivas por alternativas mais adequadas.
        5. Preencha o checklist de validação para cada questão.
        
        Por favor, retorne as questões revisadas no mesmo formato JSON, adicionando um campo "validation.de" com o resultado da sua análise para cada questão.
        
        Exemplo de formato para o campo validation.de:
        ```json
        "validation": {{
          "de": {{
            "status": "approved",
            "comments": "A questão está bem estruturada e segue o template adequadamente.",
            "checklist": {{
              "item1": {{"result": "sim", "observation": "As questões abordam os conteúdos tratados nas UAs correspondentes"}},
              "item2": {{"result": "sim", "observation": "Os objetivos de aprendizagem estão alinhados com o PAA"}},
              ...
            }}
          }}
        }}
        ```
        """
    
    def _create_validator_agent_prompt(self, task_data: Dict[str, Any]) -> str:
        """
        Cria um prompt para o Agente Validador.
        
        Args:
            task_data: Dados da tarefa
            
        Returns:
            Prompt formatado
        """
        return f"""
        Você é um Validador Final especializado em garantir a qualidade geral de questões educacionais.
        
        QUESTÕES A SEREM VALIDADAS:
        {json.dumps(task_data["questions"], ensure_ascii=False, indent=2)}
        
        INSTRUÇÕES:
        1. Analise cada questão quanto à qualidade geral, considerando as validações RT e DE já realizadas.
        2. Verifique se todas as questões estão completas e prontas para uso.
        3. Adicione uma validação final para cada questão.
        4. Gere um relatório de desenvolvimento explicando a lógica adotada no processo.
        5. Gere um documento final com todas as questões validadas.
        
        Por favor, retorne:
        
        1. As questões validadas no mesmo formato JSON, adicionando um campo "validation.final" com o resultado da sua análise para cada questão.
        
        2. Um relatório de desenvolvimento em formato Markdown:
        ```markdown
        # Relatório de Desenvolvimento
        
        ## Resumo
        
        [Resumo do processo]
        
        ## Etapas do Processo
        
        ### Agente Conteudista
        
        [Descrição do trabalho do Agente Conteudista]
        
        **Observações:** [Observações sobre o processo]
        
        ### Agente Revisor Técnico (RT)
        
        [Descrição do trabalho do Agente RT]
        
        **Observações:** [Observações sobre o processo]
        
        ### Agente Design Educacional (DE)
        
        [Descrição do trabalho do Agente DE]
        
        **Observações:** [Observações sobre o processo]
        
        ## Recomendações para Melhoria do Prompt
        
        1. [Recomendação 1]
        2. [Recomendação 2]
        3. [Recomendação 3]
        ...
        ```
        
        3. Um documento final com todas as questões validadas em formato Markdown:
        ```markdown
        # Questões Validadas
        
        ## Objetivo 1: [Texto do objetivo]
        
        ### Questão 1 ([Tipo da questão])
        
        **Contextualização:**
        [Texto de contextualização]
        
        **Enunciado:**
        [Enunciado da questão]
        
        **Alternativas:**
        a) [Texto da alternativa A]
        b) [Texto da alternativa B]
        c) [Texto da alternativa C]
        d) [Texto da alternativa D]
        e) [Texto da alternativa E]
        
        **Feedback:**
        a) [Feedback para alternativa A]
        b) [Feedback para alternativa B]
        c) [Feedback para alternativa C]
        d) [Feedback para alternativa D]
        e) [Feedback para alternativa E]
        
        ## Objetivo 2: [Texto do objetivo]
        
        ...
        ```
        """

