"""
Agente Design Educacional (DE) - Responsável pela validação da escrita e estrutura das questões.
"""

import json
from typing import Dict, Any, List, Optional, Tuple

from models.question import Question
from models.report import Checklist
from utils.ai_client import AIClient
from utils.text_processor import check_restricted_words, replace_restricted_words, extract_questions_from_text


class DEAgent:
    """
    Agente Design Educacional - Valida a escrita e estrutura das questões.
    """
    
    def __init__(self):
        """
        Inicializa o Agente Design Educacional.
        """
        self.ai_client = AIClient()
    
    def validate_questions(self, questions: List[Question], de_checklist: str, 
                         stopwords: List[str]) -> List[Question]:
        """
        Valida a escrita e estrutura das questões.
        
        Args:
            questions: Lista de questões a serem validadas
            de_checklist: Checklist de validação DE
            stopwords: Lista de palavras a serem evitadas
            
        Returns:
            Lista de questões validadas
        """
        # Prepara os dados para o prompt
        task_data = {
            "questions": [q.to_dict() for q in questions],
            "de_checklist": de_checklist,
            "stopwords": ", ".join(stopwords)
        }
        
        # Cria o prompt para o Agente DE
        prompt = self.ai_client.create_agent_prompt("de", task_data)
        
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
    
    def validate_single_question(self, question: Question, de_checklist: str, 
                               stopwords: List[str]) -> Question:
        """
        Valida a escrita e estrutura de uma única questão.
        
        Args:
            question: Questão a ser validada
            de_checklist: Checklist de validação DE
            stopwords: Lista de palavras a serem evitadas
            
        Returns:
            Questão validada
        """
        # Prepara os dados para o prompt
        task_data = {
            "questions": [question.to_dict()],
            "de_checklist": de_checklist,
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
        Você é um Designer Educacional especializado em validar a estrutura e qualidade pedagógica de questões educacionais.
        
        QUESTÃO A SER REVISADA:
        {json.dumps(task_data["questions"][0], ensure_ascii=False, indent=2)}
        
        CHECKLIST DE VALIDAÇÃO DE:
        {task_data["de_checklist"]}
        
        PALAVRAS A EVITAR (verifique e substitua estas palavras ou similares):
        {task_data["stopwords"]}
        
        INSTRUÇÕES:
        1. Analise a questão quanto à clareza, estrutura e qualidade pedagógica.
        2. Verifique se a questão segue o formato adequado.
        3. Identifique e corrija problemas de redação, ambiguidades ou inconsistências.
        4. Substitua palavras restritivas por alternativas mais adequadas.
        5. Preencha o checklist de validação para a questão.
        
        Por favor, retorne a questão revisada no mesmo formato JSON, adicionando um campo "validation.de" com o resultado da sua análise.
        
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
    
    def check_format_compliance(self, question: Question) -> Dict[str, Any]:
        """
        Verifica se a questão está em conformidade com o formato esperado.
        
        Args:
            question: Questão a ser verificada
            
        Returns:
            Resultado da verificação
        """
        result = {
            "compliant": True,
            "issues": []
        }
        
        # Verifica se tem contexto
        if not question.context:
            result["compliant"] = False
            result["issues"].append("Falta contexto na questão")
        
        # Verifica se tem enunciado
        if not question.statement:
            result["compliant"] = False
            result["issues"].append("Falta enunciado na questão")
        
        # Verifica se tem 5 alternativas
        if len(question.alternatives) != 5:
            result["compliant"] = False
            result["issues"].append(f"A questão deve ter 5 alternativas, mas tem {len(question.alternatives)}")
        
        # Verifica se tem feedback para todas as alternativas
        for alt in question.alternatives:
            if alt["id"] not in question.feedback:
                result["compliant"] = False
                result["issues"].append(f"Falta feedback para a alternativa {alt['id']}")
        
        return result
    
    def generate_validation_report(self, questions: List[Question]) -> Dict[str, Any]:
        """
        Gera um relatório de validação de design educacional.
        
        Args:
            questions: Lista de questões validadas
            
        Returns:
            Relatório de validação
        """
        report = {
            "summary": "Relatório de Validação de Design Educacional",
            "results": []
        }
        
        for question in questions:
            if question.validation and "de" in question.validation:
                validation = question.validation["de"]
                report["results"].append({
                    "question_id": question.id,
                    "objective_id": question.objective_id,
                    "status": validation.get("status", "unknown"),
                    "comments": validation.get("comments", ""),
                    "checklist": validation.get("checklist", {})
                })
        
        return report

