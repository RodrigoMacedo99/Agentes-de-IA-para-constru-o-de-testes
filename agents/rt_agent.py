"""
Agente Revisor Técnico (RT) - Responsável pela revisão técnica das questões.
"""

import json
from typing import Dict, Any, List, Optional, Tuple

from models.question import Question
from models.report import Checklist
from utils.ai_client import AIClient
from utils.text_processor import check_restricted_words, replace_restricted_words, extract_questions_from_text


class RTAgent:
    """
    Agente Revisor Técnico - Valida a precisão técnica do conteúdo das questões.
    """
    
    def __init__(self):
        """
        Inicializa o Agente Revisor Técnico.
        """
        self.ai_client = AIClient()
    
    def validate_questions(self, questions: List[Question], rt_checklist: str, 
                         stopwords: List[str]) -> List[Question]:
        """
        Valida tecnicamente as questões.
        
        Args:
            questions: Lista de questões a serem validadas
            rt_checklist: Checklist de validação RT
            stopwords: Lista de palavras a serem evitadas
            
        Returns:
            Lista de questões validadas
        """
        # Prepara os dados para o prompt
        task_data = {
            "questions": [q.to_dict() for q in questions],
            "rt_checklist": rt_checklist,
            "stopwords": ", ".join(stopwords)
        }
        
        # Cria o prompt para o Agente RT
        prompt = self.ai_client.create_agent_prompt("rt", task_data)
        
        # Gera a revisão usando a API de IA
        response = self.ai_client.generate_text(prompt, max_tokens=4000)
        
        # Extrai as questões revisadas da resposta
        content = response.get("choices", [{}])[0].get("message", {}).get("content", "")
        questions_data = extract_questions_from_text(content)
        
        if not questions_data:
            return questions  # Retorna as questões originais se não conseguir extrair as revisadas
        
        # Converte os dados para objetos Question
        validated_questions = []
        for q_data in questions_data:
            # Verifica se há palavras restritivas no texto da questão
            self._check_and_replace_restricted_words(q_data, stopwords)
            
            # Cria o objeto Question
            question = Question.from_dict(q_data)
            validated_questions.append(question)
        
        return validated_questions
    
    def _check_and_replace_restricted_words(self, question_data: Dict[str, Any], 
                                          stopwords: List[str]) -> None:
        """
        Verifica e substitui palavras restritivas em uma questão.
        
        Args:
            question_data: Dados da questão
            stopwords: Lista de palavras restritivas
        """
        # Verifica e substitui no contexto
        if "context" in question_data:
            question_data["context"] = replace_restricted_words(question_data["context"], stopwords)
        
        # Verifica e substitui no enunciado
        if "statement" in question_data:
            question_data["statement"] = replace_restricted_words(question_data["statement"], stopwords)
        
        # Verifica e substitui nas alternativas
        if "alternatives" in question_data:
            for alt in question_data["alternatives"]:
                if "text" in alt:
                    alt["text"] = replace_restricted_words(alt["text"], stopwords)
        
        # Verifica e substitui nos feedbacks
        if "feedback" in question_data:
            for key, value in question_data["feedback"].items():
                question_data["feedback"][key] = replace_restricted_words(value, stopwords)
    
    def validate_single_question(self, question: Question, rt_checklist: str, 
                               stopwords: List[str]) -> Question:
        """
        Valida tecnicamente uma única questão.
        
        Args:
            question: Questão a ser validada
            rt_checklist: Checklist de validação RT
            stopwords: Lista de palavras a serem evitadas
            
        Returns:
            Questão validada
        """
        # Prepara os dados para o prompt
        task_data = {
            "questions": [question.to_dict()],
            "rt_checklist": rt_checklist,
            "stopwords": ", ".join(stopwords)
        }
        
        # Cria o prompt específico para validação de uma única questão
        prompt = self._create_single_question_validation_prompt(task_data)
        
        # Gera a revisão usando a API de IA
        response = self.ai_client.generate_text(prompt, max_tokens=2000)
        
        # Extrai a questão revisada da resposta
        content = response.get("choices", [{}])[0].get("message", {}).get("content", "")
        questions_data = extract_questions_from_text(content)
        
        if not questions_data:
            return question  # Retorna a questão original se não conseguir extrair a revisada
        
        # Verifica se há palavras restritivas no texto da questão
        self._check_and_replace_restricted_words(questions_data[0], stopwords)
        
        # Cria o objeto Question
        return Question.from_dict(questions_data[0])
    
    def _create_single_question_validation_prompt(self, task_data: Dict[str, Any]) -> str:
        """
        Cria um prompt específico para validação de uma única questão.
        
        Args:
            task_data: Dados da tarefa
            
        Returns:
            Prompt formatado
        """
        return f"""
        Você é um Revisor Técnico especializado em validar a precisão técnica de questões educacionais.
        
        QUESTÃO A SER REVISADA:
        {json.dumps(task_data["questions"][0], ensure_ascii=False, indent=2)}
        
        CHECKLIST DE VALIDAÇÃO RT:
        {task_data["rt_checklist"]}
        
        PALAVRAS A EVITAR (verifique e substitua estas palavras ou similares):
        {task_data["stopwords"]}
        
        INSTRUÇÕES:
        1. Analise a questão quanto à precisão técnica do conteúdo.
        2. Verifique se a questão está alinhada com o objetivo de aprendizagem.
        3. Identifique e corrija quaisquer erros técnicos ou conceituais.
        4. Substitua palavras restritivas por alternativas mais adequadas.
        5. Preencha o checklist de validação para a questão.
        
        Por favor, retorne a questão revisada no mesmo formato JSON, adicionando um campo "validation.rt" com o resultado da sua análise.
        
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
    
    def search_external_information(self, topic: str) -> str:
        """
        Simula uma pesquisa de informações externas sobre um tópico.
        
        Args:
            topic: Tópico a ser pesquisado
            
        Returns:
            Informações encontradas
        """
        # Em uma implementação real, este método faria uma pesquisa na web
        # Para esta simulação, retornamos um texto genérico
        return f"""
        Resultados da pesquisa sobre "{topic}":
        
        1. Definição: {topic} refere-se a um conceito importante na área de estudo.
        2. Características principais: Precisão, confiabilidade, relevância.
        3. Aplicações: Amplamente utilizado em diversos contextos.
        4. Melhores práticas: Seguir metodologias estabelecidas e padrões da indústria.
        """
    
    def generate_validation_report(self, questions: List[Question]) -> Dict[str, Any]:
        """
        Gera um relatório de validação técnica.
        
        Args:
            questions: Lista de questões validadas
            
        Returns:
            Relatório de validação
        """
        report = {
            "summary": "Relatório de Validação Técnica",
            "results": []
        }
        
        for question in questions:
            if question.validation and "rt" in question.validation:
                validation = question.validation["rt"]
                report["results"].append({
                    "question_id": question.id,
                    "objective_id": question.objective_id,
                    "status": validation.get("status", "unknown"),
                    "comments": validation.get("comments", ""),
                    "checklist": validation.get("checklist", {})
                })
        
        return report

