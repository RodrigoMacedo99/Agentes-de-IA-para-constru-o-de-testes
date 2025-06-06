"""
Modelo para representar relatórios.
"""

import uuid
import json
from datetime import datetime
from typing import Dict, Any, List, Optional


class Report:
    """
    Representa um relatório gerado durante o processo.
    """
    
    def __init__(self, report_type: str, agent: str, content: Dict[str, Any]):
        """
        Inicializa um novo relatório.
        
        Args:
            report_type: Tipo do relatório (development_report, validation_report)
            agent: Nome do agente que gerou o relatório
            content: Conteúdo do relatório
        """
        self.id = str(uuid.uuid4())[:8]  # ID único para o relatório
        self.type = report_type
        self.creation_date = datetime.now().isoformat()
        self.agent = agent
        self.content = content
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Converte o relatório para um dicionário.
        
        Returns:
            Dicionário representando o relatório
        """
        return {
            "id": self.id,
            "type": self.type,
            "creation_date": self.creation_date,
            "agent": self.agent,
            "content": self.content
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Report':
        """
        Cria um relatório a partir de um dicionário.
        
        Args:
            data: Dicionário com os dados do relatório
            
        Returns:
            Objeto Report
        """
        report = cls(
            report_type=data["type"],
            agent=data["agent"],
            content=data["content"]
        )
        report.id = data.get("id", report.id)
        report.creation_date = data.get("creation_date", report.creation_date)
        return report
    
    def to_markdown(self) -> str:
        """
        Converte o relatório para formato Markdown.
        
        Returns:
            String em formato Markdown
        """
        if self.type == "development_report":
            return self._development_report_to_markdown()
        elif self.type == "validation_report":
            return self._validation_report_to_markdown()
        else:
            return f"# Relatório {self.id}\n\n{json.dumps(self.content, indent=2)}"
    
    def _development_report_to_markdown(self) -> str:
        """
        Converte um relatório de desenvolvimento para Markdown.
        
        Returns:
            String em formato Markdown
        """
        md = f"# Relatório de Desenvolvimento\n\n"
        md += f"**ID:** {self.id}\n"
        md += f"**Data:** {self.creation_date}\n"
        md += f"**Agente:** {self.agent}\n\n"
        
        md += f"## Resumo\n\n{self.content.get('summary', '')}\n\n"
        
        md += "## Etapas do Processo\n\n"
        for step in self.content.get("steps", []):
            md += f"### {step['agent']}\n\n"
            md += f"{step['description']}\n\n"
            md += f"**Observações:** {step['observations']}\n\n"
        
        md += "## Recomendações para Melhoria do Prompt\n\n"
        for i, rec in enumerate(self.content.get("recommendations", []), 1):
            md += f"{i}. {rec}\n"
        
        return md
    
    def _validation_report_to_markdown(self) -> str:
        """
        Converte um relatório de validação para Markdown.
        
        Returns:
            String em formato Markdown
        """
        md = f"# Relatório de Validação\n\n"
        md += f"**ID:** {self.id}\n"
        md += f"**Data:** {self.creation_date}\n"
        md += f"**Agente:** {self.agent}\n\n"
        
        md += f"## Resumo\n\n{self.content.get('summary', '')}\n\n"
        
        md += "## Resultados da Validação\n\n"
        for result in self.content.get("results", []):
            md += f"### Questão {result['question_id']}\n\n"
            md += f"**Status:** {result['status']}\n\n"
            md += f"**Comentários:** {result['comments']}\n\n"
            
            if "checklist" in result:
                md += "#### Checklist\n\n"
                for item, value in result["checklist"].items():
                    md += f"- {item}: {value}\n"
            
            md += "\n"
        
        return md


class Checklist:
    """
    Representa um checklist de validação.
    """
    
    def __init__(self, checklist_type: str, items: Dict[str, Any]):
        """
        Inicializa um novo checklist.
        
        Args:
            checklist_type: Tipo do checklist (rt, de)
            items: Dicionário com os itens do checklist
        """
        self.type = checklist_type
        self.items = items
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Converte o checklist para um dicionário.
        
        Returns:
            Dicionário representando o checklist
        """
        return {
            "type": self.type,
            "items": self.items
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Checklist':
        """
        Cria um checklist a partir de um dicionário.
        
        Args:
            data: Dicionário com os dados do checklist
            
        Returns:
            Objeto Checklist
        """
        return cls(
            checklist_type=data["type"],
            items=data["items"]
        )
    
    def to_markdown_table(self) -> str:
        """
        Converte o checklist para uma tabela Markdown.
        
        Returns:
            String em formato Markdown
        """
        md = "| Nº | Item | Sim | Não | NA | Observação |\n"
        md += "|---|---|---|---|---|---|\n"
        
        for i, (key, value) in enumerate(self.items.items(), 1):
            item_text = key
            yes = "✓" if value.get("result") == "sim" else ""
            no = "✓" if value.get("result") == "nao" else ""
            na = "✓" if value.get("result") == "na" else ""
            obs = value.get("observation", "")
            
            md += f"| {i} | {item_text} | {yes} | {no} | {na} | {obs} |\n"
        
        return md

