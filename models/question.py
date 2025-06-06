"""
Modelo para representar questões educacionais.
"""

import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional


class Alternative:
    """
    Representa uma alternativa de resposta para uma questão.
    """
    
    def __init__(self, id: str, text: str, correct: bool = False):
        """
        Inicializa uma nova alternativa.
        
        Args:
            id: Identificador da alternativa (a, b, c, d, e)
            text: Texto da alternativa
            correct: Indica se a alternativa está correta
        """
        self.id = id
        self.text = text
        self.correct = correct
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Converte a alternativa para um dicionário.
        
        Returns:
            Dicionário representando a alternativa
        """
        return {
            "id": self.id,
            "text": self.text,
            "correct": self.correct
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Alternative':
        """
        Cria uma alternativa a partir de um dicionário.
        
        Args:
            data: Dicionário com os dados da alternativa
            
        Returns:
            Objeto Alternative
        """
        return cls(
            id=data["id"],
            text=data["text"],
            correct=data.get("correct", False)
        )


class Question:
    """
    Representa uma questão educacional.
    """
    
    def __init__(self, objective_id: str, question_type: str, context: str, 
                statement: str, alternatives: List[Dict[str, Any]], feedback: Dict[str, str]):
        """
        Inicializa uma nova questão.
        
        Args:
            objective_id: ID do objetivo de aprendizagem relacionado
            question_type: Tipo da questão (single_answer, multiple_answer, assertion_reason)
            context: Texto de contextualização da questão
            statement: Enunciado da questão
            alternatives: Lista de alternativas
            feedback: Dicionário com feedback para cada alternativa
        """
        self.id = str(uuid.uuid4())[:8]  # ID único para a questão
        self.objective_id = objective_id
        self.type = question_type
        self.context = context
        self.statement = statement
        self.alternatives = alternatives
        self.feedback = feedback
        self.metadata = {
            "created_by": "content_agent",
            "last_modified_by": "content_agent",
            "creation_date": datetime.now().isoformat(),
            "last_modified": datetime.now().isoformat()
        }
        self.validation = {
            "rt": None,
            "de": None,
            "final": None
        }
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Converte a questão para um dicionário.
        
        Returns:
            Dicionário representando a questão
        """
        return {
            "id": self.id,
            "objective_id": self.objective_id,
            "type": self.type,
            "context": self.context,
            "statement": self.statement,
            "alternatives": self.alternatives,
            "feedback": self.feedback,
            "metadata": self.metadata,
            "validation": self.validation
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Question':
        """
        Cria uma questão a partir de um dicionário.
        
        Args:
            data: Dicionário com os dados da questão
            
        Returns:
            Objeto Question
        """
        question = cls(
            objective_id=data["objective_id"],
            question_type=data["type"],
            context=data["context"],
            statement=data["statement"],
            alternatives=data["alternatives"],
            feedback=data["feedback"]
        )
        question.id = data.get("id", question.id)
        question.metadata = data.get("metadata", question.metadata)
        question.validation = data.get("validation", question.validation)
        return question
    
    def update_metadata(self, modified_by: str) -> None:
        """
        Atualiza os metadados da questão.
        
        Args:
            modified_by: Nome do agente que modificou a questão
        """
        self.metadata["last_modified_by"] = modified_by
        self.metadata["last_modified"] = datetime.now().isoformat()
    
    def add_validation(self, validation_type: str, status: str, comments: str, 
                      checklist: Optional[Dict[str, Any]] = None) -> None:
        """
        Adiciona uma validação à questão.
        
        Args:
            validation_type: Tipo de validação (rt, de, final)
            status: Status da validação (approved, rejected)
            comments: Comentários sobre a validação
            checklist: Dicionário com os itens do checklist
        """
        self.validation[validation_type] = {
            "status": status,
            "comments": comments,
            "checklist": checklist or {},
            "timestamp": datetime.now().isoformat()
        }
        self.update_metadata(f"{validation_type}_agent")
    
    def to_markdown(self) -> str:
        """
        Converte a questão para formato Markdown.
        
        Returns:
            String em formato Markdown
        """
        md = f"## {self.objective_id}\n\n"
        
        if self.type == "single_answer":
            md += self._single_answer_to_markdown()
        elif self.type == "multiple_answer":
            md += self._multiple_answer_to_markdown()
        elif self.type == "assertion_reason":
            md += self._assertion_reason_to_markdown()
        else:
            md += f"**Tipo não suportado:** {self.type}\n\n"
        
        return md
    
    def _single_answer_to_markdown(self) -> str:
        """
        Converte uma questão de resposta única para Markdown.
        
        Returns:
            String em formato Markdown
        """
        md = "### Questão (Resposta Única)\n\n"
        md += f"**Contextualização:**\n{self.context}\n\n"
        md += f"**Enunciado:**\n{self.statement}\n\n"
        
        md += "**Alternativas:**\n"
        for alt in self.alternatives:
            md += f"{alt['id']}) {alt['text']}\n"
        
        md += "\n**Feedback:**\n"
        for alt_id, feedback in self.feedback.items():
            md += f"{alt_id}) {feedback}\n"
        
        return md
    
    def _multiple_answer_to_markdown(self) -> str:
        """
        Converte uma questão de resposta múltipla para Markdown.
        
        Returns:
            String em formato Markdown
        """
        md = "### Questão (Resposta Múltipla)\n\n"
        md += f"**Contextualização:**\n{self.context}\n\n"
        md += f"**Enunciado:**\n{self.statement}\n\n"
        
        md += "**Afirmativas:**\n"
        for i, alt in enumerate(self.alternatives, 1):
            if alt['id'].isdigit():
                md += f"{alt['id']}. {alt['text']}\n"
            else:
                md += f"{i}. {alt['text']}\n"
        
        md += "\n**É correto apenas o que se afirma em:**\n"
        # Aqui assumimos que as alternativas são as opções de resposta
        # e não as afirmativas em si
        for alt in self.alternatives:
            md += f"{alt['id']}) {alt['text']}\n"
        
        md += "\n**Feedback:**\n"
        for alt_id, feedback in self.feedback.items():
            md += f"{alt_id}) {feedback}\n"
        
        return md
    
    def _assertion_reason_to_markdown(self) -> str:
        """
        Converte uma questão de asserção-razão para Markdown.
        
        Returns:
            String em formato Markdown
        """
        md = "### Questão (Asserção-Razão)\n\n"
        md += f"**Contextualização:**\n{self.context}\n\n"
        md += f"**Enunciado:**\n{self.statement}\n\n"
        
        # Assumimos que as duas primeiras alternativas são as asserções
        if len(self.alternatives) >= 2:
            md += "**Asserção I:**\n"
            md += f"{self.alternatives[0]['text']}\n\n"
            md += "**PORQUE**\n\n"
            md += "**Asserção II:**\n"
            md += f"{self.alternatives[1]['text']}\n\n"
        
        md += "**A respeito dessas asserções, assinale a opção correta:**\n"
        for alt in self.alternatives:
            md += f"{alt['id']}) {alt['text']}\n"
        
        md += "\n**Feedback:**\n"
        for alt_id, feedback in self.feedback.items():
            md += f"{alt_id}) {feedback}\n"
        
        return md

