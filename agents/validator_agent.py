"""
Agente Validador - Responsável pela validação final das questões.
"""

import json
import re
from typing import Dict, Any, List, Optional, Tuple

from models.question import Question
from models.report import Report
from utils.ai_client import AIClient
from utils.text_processor import extract_questions_from_text


class ValidatorAgent:
    """
    Agente Validador - Realiza a validação final das questões.
    """
    
    def __init__(self):
        """
        Inicializa o Agente Validador.
        """
        self.ai_client = AIClient()
    
    def validate_questions(self, questions: List[Question]) -> Tuple[List[Question], str, str]:
        """
        Realiza a validação final das questões.
        
        Args:
            questions: Lista de questões a serem validadas
            
        Returns:
            Tupla (questões validadas, relatório de desenvolvimento, documento final)
        """
        # Prepara os dados para o prompt
        task_data = {
            "questions": [q.to_dict() for q in questions]
        }
        
        # Cria o prompt para o Agente Validador
        prompt = self.ai_client.create_agent_prompt("validator", task_data)
        
        # Gera a validação usando a API de IA
        response = self.ai_client.generate_text(prompt, max_tokens=6000)
        
        # Extrai os resultados da resposta
        content = response.get("choices", [{}])[0].get("message", {}).get("content", "")
        
        # Extrai o JSON da resposta
        result_data = extract_questions_from_text(content)
        
        # Extrai as seções de Markdown
        sections = self._extract_markdown_sections(content)
        
        development_report = sections.get("development_report", "")
        final_document = sections.get("final_document", "")
        
        # Processa as questões validadas
        validated_questions = []
        if isinstance(result_data, dict) and "questions" in result_data:
            questions_data = result_data["questions"]
        else:
            questions_data = result_data
        
        for q_data in questions_data:
            question = Question.from_dict(q_data)
            validated_questions.append(question)
        
        return validated_questions, development_report, final_document
    
    def _extract_markdown_sections(self, text: str) -> Dict[str, str]:
        """
        Extrai seções de um texto em formato Markdown.
        
        Args:
            text: Texto em formato Markdown
            
        Returns:
            Dicionário com as seções extraídas
        """
        sections = {}
        
        # Procura por blocos de código Markdown
        development_report_pattern = r"```(?:markdown)?\s*(# Relatório de Desenvolvimento[\s\S]*?)```"
        final_document_pattern = r"```(?:markdown)?\s*(# Questões Validadas[\s\S]*?)```"
        
        # Extrai o relatório de desenvolvimento
        development_match = re.search(development_report_pattern, text, re.IGNORECASE)
        if development_match:
            sections["development_report"] = development_match.group(1).strip()
        
        # Extrai o documento final
        final_match = re.search(final_document_pattern, text, re.IGNORECASE)
        if final_match:
            sections["final_document"] = final_match.group(1).strip()
        
        # Se não encontrou nos blocos de código, tenta extrair diretamente
        if "development_report" not in sections:
            dev_start = text.find("# Relatório de Desenvolvimento")
            if dev_start != -1:
                dev_end = text.find("#", dev_start + 1)
                if dev_end == -1:
                    dev_end = len(text)
                sections["development_report"] = text[dev_start:dev_end].strip()
        
        if "final_document" not in sections:
            doc_start = text.find("# Questões Validadas")
            if doc_start != -1:
                sections["final_document"] = text[doc_start:].strip()
        
        return sections
    
    def perform_final_validation(self, question: Question) -> Dict[str, Any]:
        """
        Realiza a validação final de uma única questão.
        
        Args:
            question: Questão a ser validada
            
        Returns:
            Resultado da validação
        """
        # Verifica se a questão já passou pelas validações RT e DE
        if not question.validation or "rt" not in question.validation or "de" not in question.validation:
            return {
                "status": "rejected",
                "comments": "A questão não passou por todas as etapas de validação necessárias."
            }
        
        # Verifica se as validações RT e DE foram aprovadas
        rt_status = question.validation["rt"].get("status", "")
        de_status = question.validation["de"].get("status", "")
        
        if rt_status != "approved" or de_status != "approved":
            return {
                "status": "rejected",
                "comments": "A questão não foi aprovada em todas as etapas de validação."
            }
        
        # Realiza verificações adicionais
        issues = []
        
        # Verifica se tem contexto
        if not question.context:
            issues.append("Falta contexto na questão")
        
        # Verifica se tem enunciado
        if not question.statement:
            issues.append("Falta enunciado na questão")
        
        # Verifica se tem 5 alternativas
        if len(question.alternatives) != 5:
            issues.append(f"A questão deve ter 5 alternativas, mas tem {len(question.alternatives)}")
        
        # Verifica se tem feedback para todas as alternativas
        for alt in question.alternatives:
            if alt["id"] not in question.feedback:
                issues.append(f"Falta feedback para a alternativa {alt['id']}")
        
        # Verifica se tem pelo menos uma alternativa correta
        if not any(alt["correct"] for alt in question.alternatives):
            issues.append("A questão não tem nenhuma alternativa correta")
        
        if issues:
            return {
                "status": "rejected",
                "comments": "A questão apresenta os seguintes problemas: " + "; ".join(issues)
            }
        
        return {
            "status": "approved",
            "comments": "A questão passou por todas as etapas de validação com sucesso."
        }
    
    def generate_development_report(self, questions: List[Question]) -> str:
        """
        Gera um relatório de desenvolvimento do processo.
        
        Args:
            questions: Lista de questões validadas
            
        Returns:
            Relatório de desenvolvimento em formato Markdown
        """
        # Prepara os dados para o prompt
        task_data = {
            "questions": [q.to_dict() for q in questions],
            "report_type": "development"
        }
        
        # Cria o prompt específico para geração do relatório
        prompt = self._create_report_generation_prompt(task_data)
        
        # Gera o relatório usando a API de IA
        response = self.ai_client.generate_text(prompt, max_tokens=3000)
        
        # Extrai o relatório da resposta
        content = response.get("choices", [{}])[0].get("message", {}).get("content", "")
        
        # Procura por blocos de código Markdown
        report_pattern = r"```(?:markdown)?\s*(# Relatório de Desenvolvimento[\s\S]*?)```"
        report_match = re.search(report_pattern, content, re.IGNORECASE)
        
        if report_match:
            return report_match.group(1).strip()
        
        # Se não encontrou no bloco de código, retorna o conteúdo completo
        return content
    
    def generate_final_document(self, questions: List[Question]) -> str:
        """
        Gera o documento final com as questões validadas.
        
        Args:
            questions: Lista de questões validadas
            
        Returns:
            Documento final em formato Markdown
        """
        # Prepara os dados para o prompt
        task_data = {
            "questions": [q.to_dict() for q in questions],
            "document_type": "final"
        }
        
        # Cria o prompt específico para geração do documento
        prompt = self._create_document_generation_prompt(task_data)
        
        # Gera o documento usando a API de IA
        response = self.ai_client.generate_text(prompt, max_tokens=3000)
        
        # Extrai o documento da resposta
        content = response.get("choices", [{}])[0].get("message", {}).get("content", "")
        
        # Procura por blocos de código Markdown
        document_pattern = r"```(?:markdown)?\s*(# Questões Validadas[\s\S]*?)```"
        document_match = re.search(document_pattern, content, re.IGNORECASE)
        
        if document_match:
            return document_match.group(1).strip()
        
        # Se não encontrou no bloco de código, retorna o conteúdo completo
        return content
    
    def _create_report_generation_prompt(self, task_data: Dict[str, Any]) -> str:
        """
        Cria um prompt específico para geração do relatório de desenvolvimento.
        
        Args:
            task_data: Dados da tarefa
            
        Returns:
            Prompt formatado
        """
        return f"""
        Você é um Validador Final especializado em garantir a qualidade geral de questões educacionais.
        
        QUESTÕES VALIDADAS:
        {json.dumps(task_data["questions"], ensure_ascii=False, indent=2)}
        
        INSTRUÇÕES:
        1. Gere um relatório de desenvolvimento explicando a lógica adotada no processo.
        2. O relatório deve incluir:
           - Um resumo do processo
           - Descrição das etapas realizadas por cada agente
           - Observações sobre o processo
           - Recomendações para melhoria do prompt
        
        Por favor, retorne o relatório em formato Markdown.
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
        """
    
    def _create_document_generation_prompt(self, task_data: Dict[str, Any]) -> str:
        """
        Cria um prompt específico para geração do documento final.
        
        Args:
            task_data: Dados da tarefa
            
        Returns:
            Prompt formatado
        """
        return f"""
        Você é um Validador Final especializado em garantir a qualidade geral de questões educacionais.
        
        QUESTÕES VALIDADAS:
        {json.dumps(task_data["questions"], ensure_ascii=False, indent=2)}
        
        INSTRUÇÕES:
        1. Gere um documento final com todas as questões validadas.
        2. O documento deve ser organizado por objetivos de aprendizagem.
        3. Cada questão deve incluir:
           - Contextualização
           - Enunciado
           - Alternativas
           - Feedback
        
        Por favor, retorne o documento em formato Markdown.
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

