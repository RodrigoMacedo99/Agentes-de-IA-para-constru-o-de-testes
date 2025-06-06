"""
Agente Conteudista - Responsável pela criação inicial das questões.
"""

import json
from typing import Dict, Any, List, Optional, Tuple

from models.question import Question, Alternative
from utils.ai_client import AIClient
from utils.text_processor import check_restricted_words, replace_restricted_words, extract_questions_from_text


class ContentAgent:
    """
    Agente Conteudista - Cria questões com base nos objetivos e fundamentação teórica.
    """
    
    def __init__(self):
        """
        Inicializa o Agente Conteudista.
        """
        self.ai_client = AIClient()
    
    def create_questions(self, objectives: List[str], theory_text: str, 
                        templates: Dict[str, str], stopwords: List[str]) -> List[Question]:
        """
        Cria questões com base nos objetivos e fundamentação teórica.
        
        Args:
            objectives: Lista de objetivos de aprendizagem
            theory_text: Texto de fundamentação teórica
            templates: Dicionário com templates para os diferentes tipos de questão
            stopwords: Lista de palavras a serem evitadas
            
        Returns:
            Lista de questões criadas
        """
        # Prepara os dados para o prompt
        task_data = {
            "objectives": "\n".join(objectives),
            "theory": theory_text,
            "template": json.dumps(templates, ensure_ascii=False, indent=2),
            "stopwords": ", ".join(stopwords)
        }
        
        # Cria o prompt para o Agente Conteudista
        prompt = self.ai_client.create_agent_prompt("content", task_data)
        
        # Gera as questões usando a API de IA
        response = self.ai_client.generate_text(prompt, max_tokens=4000)
        
        # Extrai as questões da resposta
        content = response.get("choices", [{}])[0].get("message", {}).get("content", "")
        questions_data = extract_questions_from_text(content)
        
        if not questions_data:
            return []
        
        # Converte os dados para objetos Question
        questions = []
        for q_data in questions_data:
            # Verifica se há palavras restritivas no texto da questão
            self._check_and_replace_restricted_words(q_data, stopwords)
            
            # Cria o objeto Question
            question = Question.from_dict(q_data)
            questions.append(question)
        
        return questions
    
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
    
    def create_single_answer_question(self, objective: str, theory_text: str, 
                                     template: str, stopwords: List[str]) -> Optional[Question]:
        """
        Cria uma questão de resposta única.
        
        Args:
            objective: Objetivo de aprendizagem
            theory_text: Texto de fundamentação teórica
            template: Template para a questão
            stopwords: Lista de palavras a serem evitadas
            
        Returns:
            Questão criada ou None se falhar
        """
        # Prepara os dados para o prompt
        task_data = {
            "objectives": objective,
            "theory": theory_text,
            "template": template,
            "stopwords": ", ".join(stopwords),
            "question_type": "single_answer"
        }
        
        # Cria o prompt específico para questão de resposta única
        prompt = self._create_single_answer_prompt(task_data)
        
        # Gera a questão usando a API de IA
        response = self.ai_client.generate_text(prompt, max_tokens=2000)
        
        # Extrai a questão da resposta
        content = response.get("choices", [{}])[0].get("message", {}).get("content", "")
        questions_data = extract_questions_from_text(content)
        
        if not questions_data:
            return None
        
        # Verifica se há palavras restritivas no texto da questão
        self._check_and_replace_restricted_words(questions_data[0], stopwords)
        
        # Cria o objeto Question
        return Question.from_dict(questions_data[0])
    
    def create_multiple_answer_question(self, objective: str, theory_text: str, 
                                      template: str, stopwords: List[str]) -> Optional[Question]:
        """
        Cria uma questão de resposta múltipla.
        
        Args:
            objective: Objetivo de aprendizagem
            theory_text: Texto de fundamentação teórica
            template: Template para a questão
            stopwords: Lista de palavras a serem evitadas
            
        Returns:
            Questão criada ou None se falhar
        """
        # Prepara os dados para o prompt
        task_data = {
            "objectives": objective,
            "theory": theory_text,
            "template": template,
            "stopwords": ", ".join(stopwords),
            "question_type": "multiple_answer"
        }
        
        # Cria o prompt específico para questão de resposta múltipla
        prompt = self._create_multiple_answer_prompt(task_data)
        
        # Gera a questão usando a API de IA
        response = self.ai_client.generate_text(prompt, max_tokens=2000)
        
        # Extrai a questão da resposta
        content = response.get("choices", [{}])[0].get("message", {}).get("content", "")
        questions_data = extract_questions_from_text(content)
        
        if not questions_data:
            return None
        
        # Verifica se há palavras restritivas no texto da questão
        self._check_and_replace_restricted_words(questions_data[0], stopwords)
        
        # Cria o objeto Question
        return Question.from_dict(questions_data[0])
    
    def create_assertion_reason_question(self, objective: str, theory_text: str, 
                                       template: str, stopwords: List[str]) -> Optional[Question]:
        """
        Cria uma questão de asserção-razão.
        
        Args:
            objective: Objetivo de aprendizagem
            theory_text: Texto de fundamentação teórica
            template: Template para a questão
            stopwords: Lista de palavras a serem evitadas
            
        Returns:
            Questão criada ou None se falhar
        """
        # Prepara os dados para o prompt
        task_data = {
            "objectives": objective,
            "theory": theory_text,
            "template": template,
            "stopwords": ", ".join(stopwords),
            "question_type": "assertion_reason"
        }
        
        # Cria o prompt específico para questão de asserção-razão
        prompt = self._create_assertion_reason_prompt(task_data)
        
        # Gera a questão usando a API de IA
        response = self.ai_client.generate_text(prompt, max_tokens=2000)
        
        # Extrai a questão da resposta
        content = response.get("choices", [{}])[0].get("message", {}).get("content", "")
        questions_data = extract_questions_from_text(content)
        
        if not questions_data:
            return None
        
        # Verifica se há palavras restritivas no texto da questão
        self._check_and_replace_restricted_words(questions_data[0], stopwords)
        
        # Cria o objeto Question
        return Question.from_dict(questions_data[0])
    
    def _create_single_answer_prompt(self, task_data: Dict[str, Any]) -> str:
        """
        Cria um prompt específico para questão de resposta única.
        
        Args:
            task_data: Dados da tarefa
            
        Returns:
            Prompt formatado
        """
        return f"""
        Você é um Professor-Conteudista especializado em elaborar questões educacionais de alta qualidade.
        
        OBJETIVO DE APRENDIZAGEM:
        {task_data["objectives"]}
        
        FUNDAMENTAÇÃO TEÓRICA:
        {task_data["theory"]}
        
        TEMPLATE DE QUESTÃO DE RESPOSTA ÚNICA:
        {task_data["template"]}
        
        PALAVRAS A EVITAR (não use estas palavras ou similares):
        {task_data["stopwords"]}
        
        INSTRUÇÕES:
        1. Elabore UMA questão de RESPOSTA ÚNICA para o objetivo de aprendizagem fornecido.
        2. Siga rigorosamente o formato do template fornecido.
        3. Evite usar palavras restritivas listadas acima.
        4. Crie uma questão que avalie compreensão e aplicação, não memorização.
        5. Forneça feedback detalhado para cada alternativa.
        6. A questão deve ter exatamente 5 alternativas (a, b, c, d, e), sendo apenas uma correta.
        7. Todas as alternativas devem ter extensão semelhante.
        
        Por favor, elabore a questão no formato JSON seguindo a estrutura abaixo:
        ```json
        {{
          "objective_id": "objetivo",
          "type": "single_answer",
          "context": "Texto de contextualização...",
          "statement": "Enunciado da questão...",
          "alternatives": [
            {{"id": "a", "text": "Alternativa A", "correct": true}},
            {{"id": "b", "text": "Alternativa B", "correct": false}},
            {{"id": "c", "text": "Alternativa C", "correct": false}},
            {{"id": "d", "text": "Alternativa D", "correct": false}},
            {{"id": "e", "text": "Alternativa E", "correct": false}}
          ],
          "feedback": {{
            "a": "Correta. Justificativa para A...",
            "b": "Incorreta. Justificativa para B...",
            "c": "Incorreta. Justificativa para C...",
            "d": "Incorreta. Justificativa para D...",
            "e": "Incorreta. Justificativa para E..."
          }}
        }}
        ```
        """
    
    def _create_multiple_answer_prompt(self, task_data: Dict[str, Any]) -> str:
        """
        Cria um prompt específico para questão de resposta múltipla.
        
        Args:
            task_data: Dados da tarefa
            
        Returns:
            Prompt formatado
        """
        return f"""
        Você é um Professor-Conteudista especializado em elaborar questões educacionais de alta qualidade.
        
        OBJETIVO DE APRENDIZAGEM:
        {task_data["objectives"]}
        
        FUNDAMENTAÇÃO TEÓRICA:
        {task_data["theory"]}
        
        TEMPLATE DE QUESTÃO DE RESPOSTA MÚLTIPLA:
        {task_data["template"]}
        
        PALAVRAS A EVITAR (não use estas palavras ou similares):
        {task_data["stopwords"]}
        
        INSTRUÇÕES:
        1. Elabore UMA questão de RESPOSTA MÚLTIPLA para o objetivo de aprendizagem fornecido.
        2. Siga rigorosamente o formato do template fornecido.
        3. Evite usar palavras restritivas listadas acima.
        4. Crie uma questão que avalie compreensão e aplicação, não memorização.
        5. Forneça feedback detalhado para cada alternativa.
        6. A questão deve ter 4 afirmativas (I, II, III, IV) e 5 alternativas (a, b, c, d, e).
        7. Todas as alternativas devem ter extensão semelhante.
        
        Por favor, elabore a questão no formato JSON seguindo a estrutura abaixo:
        ```json
        {{
          "objective_id": "objetivo",
          "type": "multiple_answer",
          "context": "Texto de contextualização...",
          "statement": "Enunciado da questão...",
          "assertions": [
            {{"id": "I", "text": "Afirmativa I", "correct": true}},
            {{"id": "II", "text": "Afirmativa II", "correct": false}},
            {{"id": "III", "text": "Afirmativa III", "correct": true}},
            {{"id": "IV", "text": "Afirmativa IV", "correct": false}}
          ],
          "alternatives": [
            {{"id": "a", "text": "Se apenas as afirmativas I e III estiverem corretas", "correct": true}},
            {{"id": "b", "text": "Se apenas as afirmativas II e IV estiverem corretas", "correct": false}},
            {{"id": "c", "text": "Se apenas as afirmativas I, II e III estiverem corretas", "correct": false}},
            {{"id": "d", "text": "Se apenas as afirmativas II, III e IV estiverem corretas", "correct": false}},
            {{"id": "e", "text": "Se todas as afirmativas estiverem corretas", "correct": false}}
          ],
          "feedback": {{
            "a": "Correta. Justificativa para A...",
            "b": "Incorreta. Justificativa para B...",
            "c": "Incorreta. Justificativa para C...",
            "d": "Incorreta. Justificativa para D...",
            "e": "Incorreta. Justificativa para E..."
          }}
        }}
        ```
        """
    
    def _create_assertion_reason_prompt(self, task_data: Dict[str, Any]) -> str:
        """
        Cria um prompt específico para questão de asserção-razão.
        
        Args:
            task_data: Dados da tarefa
            
        Returns:
            Prompt formatado
        """
        return f"""
        Você é um Professor-Conteudista especializado em elaborar questões educacionais de alta qualidade.
        
        OBJETIVO DE APRENDIZAGEM:
        {task_data["objectives"]}
        
        FUNDAMENTAÇÃO TEÓRICA:
        {task_data["theory"]}
        
        TEMPLATE DE QUESTÃO DE ASSERÇÃO-RAZÃO:
        {task_data["template"]}
        
        PALAVRAS A EVITAR (não use estas palavras ou similares):
        {task_data["stopwords"]}
        
        INSTRUÇÕES:
        1. Elabore UMA questão de ASSERÇÃO-RAZÃO para o objetivo de aprendizagem fornecido.
        2. Siga rigorosamente o formato do template fornecido.
        3. Evite usar palavras restritivas listadas acima.
        4. Crie uma questão que avalie compreensão e aplicação, não memorização.
        5. Forneça feedback detalhado para cada alternativa.
        6. A questão deve ter duas asserções (I e II) e 5 alternativas (a, b, c, d, e).
        7. Priorize criar questões onde "as duas asserções são verdadeiras, mas a II não justifica a I" ou "as duas asserções são falsas".
        
        Por favor, elabore a questão no formato JSON seguindo a estrutura abaixo:
        ```json
        {{
          "objective_id": "objetivo",
          "type": "assertion_reason",
          "context": "Texto de contextualização...",
          "statement": "Avalie as asserções a seguir e a relação proposta entre elas.",
          "assertions": [
            {{"id": "I", "text": "Asserção I", "correct": true}},
            {{"id": "II", "text": "Asserção II (PORQUE)", "correct": true}}
          ],
          "alternatives": [
            {{"id": "a", "text": "As asserções I e II são proposições verdadeiras, e a II é uma justificativa correta da I.", "correct": false}},
            {{"id": "b", "text": "As asserções I e II são proposições verdadeiras, mas a II não é uma justificativa correta da I.", "correct": true}},
            {{"id": "c", "text": "A asserção I é uma proposição verdadeira, e a II é uma proposição falsa.", "correct": false}},
            {{"id": "d", "text": "A asserção I é uma proposição falsa, e a II é uma proposição verdadeira.", "correct": false}},
            {{"id": "e", "text": "As asserções I e II são proposições falsas.", "correct": false}}
          ],
          "feedback": {{
            "a": "Incorreta. Justificativa para A...",
            "b": "Correta. Justificativa para B...",
            "c": "Incorreta. Justificativa para C...",
            "d": "Incorreta. Justificativa para D...",
            "e": "Incorreta. Justificativa para E..."
          }}
        }}
        ```
        """

