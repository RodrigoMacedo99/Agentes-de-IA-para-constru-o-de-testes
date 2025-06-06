"""
Modelo para representar tarefas.
"""

import uuid
from datetime import datetime
from typing import Dict, Any, List, Optional

from models.question import Question
from models.report import Report


class Task:
    """
    Representa uma tarefa a ser processada pelo sistema.
    """
    
    def __init__(self, objectives: List[str], theory_text: str, templates: Dict[str, str], stopwords: List[str]):
        """
        Inicializa uma nova tarefa.
        
        Args:
            objectives: Lista de objetivos de aprendizagem
            theory_text: Texto de fundamentação teórica
            templates: Dicionário com templates para os diferentes tipos de questão
            stopwords: Lista de palavras a serem evitadas
        """
        self.id = str(uuid.uuid4())[:8]  # ID único para a tarefa
        self.creation_date = datetime.now().isoformat()
        self.objectives = objectives
        self.theory_text = theory_text
        self.templates = templates
        self.stopwords = stopwords
        self.questions = []
        self.reports = []
        self.status = "created"  # created, in_progress, completed
        self.current_agent = None
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Converte a tarefa para um dicionário.
        
        Returns:
            Dicionário representando a tarefa
        """
        return {
            "id": self.id,
            "creation_date": self.creation_date,
            "objectives": self.objectives,
            "theory_text": self.theory_text,
            "templates": self.templates,
            "stopwords": self.stopwords,
            "questions": [q.to_dict() for q in self.questions],
            "reports": [r.to_dict() for r in self.reports],
            "status": self.status,
            "current_agent": self.current_agent
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """
        Cria uma tarefa a partir de um dicionário.
        
        Args:
            data: Dicionário com os dados da tarefa
            
        Returns:
            Objeto Task
        """
        task = cls(
            objectives=data["objectives"],
            theory_text=data["theory_text"],
            templates=data["templates"],
            stopwords=data["stopwords"]
        )
        task.id = data.get("id", task.id)
        task.creation_date = data.get("creation_date", task.creation_date)
        task.questions = [Question.from_dict(q) for q in data.get("questions", [])]
        task.reports = [Report.from_dict(r) for r in data.get("reports", [])]
        task.status = data.get("status", task.status)
        task.current_agent = data.get("current_agent", task.current_agent)
        return task
    
    def add_question(self, question: Question) -> None:
        """
        Adiciona uma questão à tarefa.
        
        Args:
            question: Objeto Question a ser adicionado
        """
        self.questions.append(question)
    
    def add_report(self, report: Report) -> None:
        """
        Adiciona um relatório à tarefa.
        
        Args:
            report: Objeto Report a ser adicionado
        """
        self.reports.append(report)
    
    def update_status(self, status: str, agent: Optional[str] = None) -> None:
        """
        Atualiza o status da tarefa.
        
        Args:
            status: Novo status da tarefa
            agent: Nome do agente atual
        """
        self.status = status
        self.current_agent = agent
    
    def get_questions_for_objective(self, objective_id: str) -> List[Question]:
        """
        Retorna as questões associadas a um objetivo específico.
        
        Args:
            objective_id: ID do objetivo
            
        Returns:
            Lista de questões associadas ao objetivo
        """
        return [q for q in self.questions if q.objective_id == objective_id]
    
    def get_report_by_type(self, report_type: str) -> Optional[Report]:
        """
        Retorna o relatório de um tipo específico.
        
        Args:
            report_type: Tipo do relatório
            
        Returns:
            Relatório do tipo especificado, ou None se não existir
        """
        for report in self.reports:
            if report.type == report_type:
                return report
        return None

