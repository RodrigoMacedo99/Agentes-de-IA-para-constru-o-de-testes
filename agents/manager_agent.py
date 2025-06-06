"""
Agente Gerenciador - Responsável por coordenar o fluxo de trabalho entre os agentes.
"""

import os
import json
from typing import Dict, Any, List, Optional, Tuple

from models.task import Task
from models.question import Question
from models.report import Report
from utils.ai_client import AIClient
from utils.file_handler import save_task_data, load_task_data, save_questions, save_report, save_final_document
from utils.text_processor import extract_objectives, extract_questions_from_text

import config


class ManagerAgent:
    """
    Agente Gerenciador - Coordena o fluxo de trabalho entre os agentes.
    """
    
    def __init__(self):
        """
        Inicializa o Agente Gerenciador.
        """
        self.ai_client = AIClient()
        self.current_task = None
    
    def initialize_task(self, objectives: str, theory_text: str) -> str:
        """
        Inicializa uma nova tarefa.
        
        Args:
            objectives: Objetivos de aprendizagem
            theory_text: Texto de fundamentação teórica
            
        Returns:
            ID da tarefa criada
        """
        # Carrega os templates de questões
        templates = self._load_templates()
        
        # Carrega as stopwords
        stopwords = self._load_stopwords()
        
        # Extrai os objetivos de aprendizagem
        objectives_list = extract_objectives(objectives)
        
        # Cria a tarefa
        self.current_task = Task(
            objectives=objectives_list,
            theory_text=theory_text,
            templates=templates,
            stopwords=stopwords
        )
        
        # Salva a tarefa
        save_task_data(self.current_task.id, self.current_task.to_dict())
        
        return self.current_task.id
    
    def _load_templates(self) -> Dict[str, str]:
        """
        Carrega os templates de questões.
        
        Returns:
            Dicionário com os templates
        """
        templates = {}
        template_files = {
            "single_answer": "single_answer.json",
            "multiple_answer": "multiple_answer.json",
            "assertion_reason": "assertion_reason.json"
        }
        
        for key, filename in template_files.items():
            path = os.path.join(config.TEMPLATES_DIR, filename)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    templates[key] = f.read()
            except FileNotFoundError:
                # Se o arquivo não existir, usa um template padrão
                templates[key] = self._get_default_template(key)
        
        return templates
    
    def _get_default_template(self, template_type: str) -> str:
        """
        Retorna um template padrão para um tipo de questão.
        
        Args:
            template_type: Tipo de template
            
        Returns:
            Template padrão
        """
        if template_type == "single_answer":
            return """
            {
              "type": "single_answer",
              "context": "Texto de contextualização da questão...",
              "statement": "Enunciado da questão...",
              "alternatives": [
                {"id": "a", "text": "Alternativa A", "correct": true},
                {"id": "b", "text": "Alternativa B", "correct": false},
                {"id": "c", "text": "Alternativa C", "correct": false},
                {"id": "d", "text": "Alternativa D", "correct": false},
                {"id": "e", "text": "Alternativa E", "correct": false}
              ],
              "feedback": {
                "a": "Correta. Justificativa para A...",
                "b": "Incorreta. Justificativa para B...",
                "c": "Incorreta. Justificativa para C...",
                "d": "Incorreta. Justificativa para D...",
                "e": "Incorreta. Justificativa para E..."
              }
            }
            """
        elif template_type == "multiple_answer":
            return """
            {
              "type": "multiple_answer",
              "context": "Texto de contextualização da questão...",
              "statement": "Enunciado da questão...",
              "assertions": [
                {"id": "1", "text": "Afirmativa 1", "correct": true},
                {"id": "2", "text": "Afirmativa 2", "correct": false},
                {"id": "3", "text": "Afirmativa 3", "correct": true},
                {"id": "4", "text": "Afirmativa 4", "correct": false}
              ],
              "alternatives": [
                {"id": "a", "text": "Se apenas as afirmativas 1 e 3 estiverem corretas", "correct": true},
                {"id": "b", "text": "Se apenas as afirmativas 2 e 4 estiverem corretas", "correct": false},
                {"id": "c", "text": "Se apenas as afirmativas 1, 2 e 3 estiverem corretas", "correct": false},
                {"id": "d", "text": "Se apenas as afirmativas 2, 3 e 4 estiverem corretas", "correct": false},
                {"id": "e", "text": "Se todas as afirmativas estiverem corretas", "correct": false}
              ],
              "feedback": {
                "a": "Correta. Justificativa para A...",
                "b": "Incorreta. Justificativa para B...",
                "c": "Incorreta. Justificativa para C...",
                "d": "Incorreta. Justificativa para D...",
                "e": "Incorreta. Justificativa para E..."
              }
            }
            """
        elif template_type == "assertion_reason":
            return """
            {
              "type": "assertion_reason",
              "context": "Texto de contextualização da questão...",
              "statement": "Avalie as asserções a seguir e a relação proposta entre elas.",
              "assertions": [
                {"id": "1", "text": "Asserção I", "correct": true},
                {"id": "2", "text": "Asserção II (PORQUE)", "correct": true}
              ],
              "alternatives": [
                {"id": "a", "text": "As asserções I e II são proposições verdadeiras, e a II é uma justificativa correta da I.", "correct": true},
                {"id": "b", "text": "As asserções I e II são proposições verdadeiras, mas a II não é uma justificativa correta da I.", "correct": false},
                {"id": "c", "text": "A asserção I é uma proposição verdadeira, e a II é uma proposição falsa.", "correct": false},
                {"id": "d", "text": "A asserção I é uma proposição falsa, e a II é uma proposição verdadeira.", "correct": false},
                {"id": "e", "text": "As asserções I e II são proposições falsas.", "correct": false}
              ],
              "feedback": {
                "a": "Correta. Justificativa para A...",
                "b": "Incorreta. Justificativa para B...",
                "c": "Incorreta. Justificativa para C...",
                "d": "Incorreta. Justificativa para D...",
                "e": "Incorreta. Justificativa para E..."
              }
            }
            """
        else:
            return "{}"
    
    def _load_stopwords(self) -> List[str]:
        """
        Carrega as stopwords.
        
        Returns:
            Lista de stopwords
        """
        stopwords = [
            "limita-se", "estritamente", "apenas", "exclusivamente", "somente",
            "unicamente", "restritivamente", "rigorosamente", "especificamente",
            "exatamente", "precisamente", "unilateralmente", "singularmente",
            "determinadamente", "explicitamente", "meramente", "unicidade",
            "nada além de", "só isso", "e somente isso", "de forma exclusiva",
            "de modo restrito", "de maneira limitada", "sem exceções"
        ]
        
        # Tenta carregar de um arquivo
        try:
            path = os.path.join(config.DATA_DIR, "stopwords.txt")
            with open(path, 'r', encoding='utf-8') as f:
                custom_stopwords = [line.strip() for line in f if line.strip()]
                if custom_stopwords:
                    stopwords = custom_stopwords
        except FileNotFoundError:
            pass
        
        return stopwords
    
    def load_task(self, task_id: str) -> bool:
        """
        Carrega uma tarefa existente.
        
        Args:
            task_id: ID da tarefa
            
        Returns:
            True se a tarefa foi carregada com sucesso, False caso contrário
        """
        task_data = load_task_data(task_id)
        if not task_data:
            return False
        
        self.current_task = Task.from_dict(task_data)
        return True
    
    def assign_to_content_agent(self) -> Tuple[bool, str]:
        """
        Atribui a tarefa ao Agente Conteudista.
        
        Returns:
            Tupla (sucesso, mensagem)
        """
        if not self.current_task:
            return False, "Nenhuma tarefa inicializada"
        
        # Atualiza o status da tarefa
        self.current_task.update_status("in_progress", "content_agent")
        
        # Prepara os dados para o Agente Conteudista
        task_data = {
            "objectives": "\n".join(self.current_task.objectives),
            "theory": self.current_task.theory_text,
            "template": json.dumps(self.current_task.templates, ensure_ascii=False, indent=2),
            "stopwords": ", ".join(self.current_task.stopwords)
        }
        
        # Cria o prompt para o Agente Conteudista
        prompt = self.ai_client.create_agent_prompt("content", task_data)
        
        # Gera as questões usando a API de IA
        response = self.ai_client.generate_text(prompt, max_tokens=4000)
        
        # Extrai as questões da resposta
        content = response.get("choices", [{}])[0].get("message", {}).get("content", "")
        questions_data = extract_questions_from_text(content)
        
        if not questions_data:
            return False, "Não foi possível extrair questões da resposta"
        
        # Converte os dados para objetos Question
        for q_data in questions_data:
            question = Question.from_dict(q_data)
            self.current_task.add_question(question)
        
        # Salva a tarefa atualizada
        save_task_data(self.current_task.id, self.current_task.to_dict())
        
        return True, f"Criadas {len(questions_data)} questões"
    
    def assign_to_rt_agent(self) -> Tuple[bool, str]:
        """
        Atribui a tarefa ao Agente Revisor Técnico.
        
        Returns:
            Tupla (sucesso, mensagem)
        """
        if not self.current_task:
            return False, "Nenhuma tarefa inicializada"
        
        if not self.current_task.questions:
            return False, "Não há questões para revisar"
        
        # Atualiza o status da tarefa
        self.current_task.update_status("in_progress", "rt_agent")
        
        # Carrega o checklist RT
        rt_checklist = self._load_rt_checklist()
        
        # Prepara os dados para o Agente RT
        task_data = {
            "questions": [q.to_dict() for q in self.current_task.questions],
            "rt_checklist": rt_checklist,
            "stopwords": self.current_task.stopwords
        }
        
        # Cria o prompt para o Agente RT
        prompt = self.ai_client.create_agent_prompt("rt", task_data)
        
        # Gera a revisão usando a API de IA
        response = self.ai_client.generate_text(prompt, max_tokens=4000)
        
        # Extrai as questões revisadas da resposta
        content = response.get("choices", [{}])[0].get("message", {}).get("content", "")
        questions_data = extract_questions_from_text(content)
        
        if not questions_data:
            return False, "Não foi possível extrair questões revisadas da resposta"
        
        # Atualiza as questões com as revisões
        for q_data in questions_data:
            for i, question in enumerate(self.current_task.questions):
                if question.objective_id == q_data["objective_id"]:
                    # Atualiza a questão com os dados revisados
                    self.current_task.questions[i] = Question.from_dict(q_data)
                    break
        
        # Salva a tarefa atualizada
        save_task_data(self.current_task.id, self.current_task.to_dict())
        
        return True, f"Revisadas {len(questions_data)} questões"
    
    def _load_rt_checklist(self) -> str:
        """
        Carrega o checklist de validação RT.
        
        Returns:
            Checklist RT em formato string
        """
        try:
            path = os.path.join(config.DATA_DIR, "validacao_rt.txt")
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            # Retorna um checklist padrão
            return """
            CHECKLIST – REVISOR TÉCNICO

            | Nº | Item                                                                                                                                 | Sim | Não | NA  | Observação |
            |----|--------------------------------------------------------------------------------------------------------------------------------------|-----|-----|-----|-------------|
            | 1  | As questões abordam os conteúdos tratados nas UAs/Etapas/Aulas correspondentes?                                                     |     |     |     |             |
            | 2  | Os objetivos de aprendizagem indicados nos grupos correspondem aos definidos no PAA?                                                |     |     |     |             |
            | 3  | Todas as questões de um grupo permitem avaliar a aprendizagem a partir do(s) objetivo(s) associado(s)? (máximo 2 objetivos).        |     |     |     |             |
            | 4  | Há correlação entre os conteúdos desenvolvidos nas UAs/Etapas/Aulas e as questões?                                                  |     |     |     |             |
            | 5  | O nível de complexidade das questões é coerente com os conteúdos propostos nas UAs/Etapas/Aulas correspondentes?                   |     |     |     |             |
            | 6  | Os feedbacks das questões justificam o porquê do acerto ou erro de forma clara e precisa?                                           |     |     |     |             |
            | 7  | O texto-base/enunciado está claro e sem ambiguidades?                                                                               |     |     |     |             |
            | 8  | As questões não avaliam conteúdos memorizados?                                                                                      |     |     |     |             |
            """
    
    def assign_to_de_agent(self) -> Tuple[bool, str]:
        """
        Atribui a tarefa ao Agente Design Educacional.
        
        Returns:
            Tupla (sucesso, mensagem)
        """
        if not self.current_task:
            return False, "Nenhuma tarefa inicializada"
        
        if not self.current_task.questions:
            return False, "Não há questões para revisar"
        
        # Atualiza o status da tarefa
        self.current_task.update_status("in_progress", "de_agent")
        
        # Carrega o checklist DE
        de_checklist = self._load_de_checklist()
        
        # Prepara os dados para o Agente DE
        task_data = {
            "questions": [q.to_dict() for q in self.current_task.questions],
            "de_checklist": de_checklist,
            "stopwords": self.current_task.stopwords
        }
        
        # Cria o prompt para o Agente DE
        prompt = self.ai_client.create_agent_prompt("de", task_data)
        
        # Gera a revisão usando a API de IA
        response = self.ai_client.generate_text(prompt, max_tokens=4000)
        
        # Extrai as questões revisadas da resposta
        content = response.get("choices", [{}])[0].get("message", {}).get("content", "")
        questions_data = extract_questions_from_text(content)
        
        if not questions_data:
            return False, "Não foi possível extrair questões revisadas da resposta"
        
        # Atualiza as questões com as revisões
        for q_data in questions_data:
            for i, question in enumerate(self.current_task.questions):
                if question.objective_id == q_data["objective_id"]:
                    # Atualiza a questão com os dados revisados
                    self.current_task.questions[i] = Question.from_dict(q_data)
                    break
        
        # Salva a tarefa atualizada
        save_task_data(self.current_task.id, self.current_task.to_dict())
        
        return True, f"Revisadas {len(questions_data)} questões"
    
    def _load_de_checklist(self) -> str:
        """
        Carrega o checklist de validação DE.
        
        Returns:
            Checklist DE em formato string
        """
        try:
            path = os.path.join(config.DATA_DIR, "validacao_de.txt")
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            # Retorna um checklist padrão
            return """
            CHECKLIST – DESIGN EDUCACIONAL

            | Nº | Item                                                                                                                                 | Sim | Não | NA  | Observação |
            |----|--------------------------------------------------------------------------------------------------------------------------------------|-----|-----|-----|-------------|
            | 1  | As questões abordam os conteúdos tratados nas UAs/Etapas/Aulas correspondentes?                                                     |     |     |     |             |
            | 2  | Os objetivos de aprendizagem indicados nos grupos correspondem aos definidos no PAA?                                                |     |     |     |             |
            | 3  | Todas as questões de um grupo permitem avaliar a aprendizagem a partir do(s) objetivo(s) associado(s)? (máximo 2 objetivos).        |     |     |     |             |
            | 4  | Há correlação entre os conteúdos desenvolvidos nas UAs/Etapas/Aulas e as questões?                                                  |     |     |     |             |
            | 5  | O texto-base/enunciado está claro e sem ambiguidades?                                                                               |     |     |     |             |
            | 6  | O texto-base/enunciado dá suporte para a resolução da questão?                                                                      |     |     |     |             |
            | 7  | Os feedbacks das questões justificam o porquê do acerto ou erro de forma clara e precisa?                                           |     |     |     |             |
            | 8  | Há indicação de referência nos textos de suporte, seja autoral ou de curadoria?                                                     |     |     |     |             |
            | 9  | Nenhum comando solicita assinalar a alternativa incorreta?                                                                          |     |     |     |             |
            | 10 | As questões não avaliam conteúdos memorizados?                                                                                      |     |     |     |             |
            | 11 | As questões não apresentam alternativas com "todas as afirmativas estão erradas/incorretas"?                                        |     |     |     |             |
            | 12 | As questões apresentam alternativas com extensão semelhante?                                                                        |     |     |     |             |
            | 13 | As questões não apresentam elementos que tornem a afirmação falsa, como: "apenas", "somente", "nunca", etc.?                        |     |     |     |             |
            | 14 | Todas as afirmativas iniciam com palavras da mesma classe gramatical?                                                               |     |     |     |             |
            | 15 | Cada item avaliativo contempla 5 alternativas de resposta?                                                                          |     |     |     |             |
            """
    
    def assign_to_validator_agent(self) -> Tuple[bool, str]:
        """
        Atribui a tarefa ao Agente Validador.
        
        Returns:
            Tupla (sucesso, mensagem)
        """
        if not self.current_task:
            return False, "Nenhuma tarefa inicializada"
        
        if not self.current_task.questions:
            return False, "Não há questões para validar"
        
        # Atualiza o status da tarefa
        self.current_task.update_status("in_progress", "validator_agent")
        
        # Prepara os dados para o Agente Validador
        task_data = {
            "questions": [q.to_dict() for q in self.current_task.questions]
        }
        
        # Cria o prompt para o Agente Validador
        prompt = self.ai_client.create_agent_prompt("validator", task_data)
        
        # Gera a validação usando a API de IA
        response = self.ai_client.generate_text(prompt, max_tokens=6000)
        
        # Extrai os resultados da resposta
        content = response.get("choices", [{}])[0].get("message", {}).get("content", "")
        
        # Extrai o JSON da resposta
        result_data = extract_questions_from_text(content)
        
        if not result_data:
            return False, "Não foi possível extrair os resultados da validação"
        
        # Extrai as seções de Markdown
        sections = self._extract_markdown_sections(content)
        
        # Salva os resultados
        development_report = sections.get("development_report", "")
        final_document = sections.get("final_document", "")
        
        # Atualiza as questões com as validações finais
        if isinstance(result_data, dict) and "questions" in result_data:
            questions_data = result_data["questions"]
        else:
            questions_data = result_data
        
        for q_data in questions_data:
            for i, question in enumerate(self.current_task.questions):
                if question.objective_id == q_data["objective_id"]:
                    # Atualiza a questão com os dados validados
                    self.current_task.questions[i] = Question.from_dict(q_data)
                    break
        
        # Cria e adiciona o relatório de desenvolvimento
        report = Report(
            report_type="development_report",
            agent="validator_agent",
            content={"text": development_report}
        )
        self.current_task.add_report(report)
        
        # Salva a tarefa atualizada
        save_task_data(self.current_task.id, self.current_task.to_dict())
        
        # Salva os arquivos de saída
        questions_path = save_questions(self.current_task.id, [q.to_dict() for q in self.current_task.questions])
        report_path = save_report(self.current_task.id, "development", development_report)
        document_path = save_final_document(self.current_task.id, final_document)
        
        # Atualiza o status da tarefa
        self.current_task.update_status("completed", "validator_agent")
        save_task_data(self.current_task.id, self.current_task.to_dict())
        
        return True, f"Validação concluída. Arquivos salvos: {questions_path}, {report_path}, {document_path}"
    
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
    
    def get_task_status(self) -> Dict[str, Any]:
        """
        Retorna o status atual da tarefa.
        
        Returns:
            Dicionário com o status da tarefa
        """
        if not self.current_task:
            return {"status": "no_task", "message": "Nenhuma tarefa inicializada"}
        
        return {
            "task_id": self.current_task.id,
            "status": self.current_task.status,
            "current_agent": self.current_task.current_agent,
            "questions_count": len(self.current_task.questions),
            "reports_count": len(self.current_task.reports)
        }
    
    def get_final_results(self) -> Dict[str, Any]:
        """
        Retorna os resultados finais da tarefa.
        
        Returns:
            Dicionário com os resultados finais
        """
        if not self.current_task:
            return {"status": "no_task", "message": "Nenhuma tarefa inicializada"}
        
        if self.current_task.status != "completed":
            return {"status": "in_progress", "message": "Tarefa ainda não concluída"}
        
        # Obtém os caminhos dos arquivos de saída
        questions_path = os.path.join(config.OUTPUT_DIR, f"questions_{self.current_task.id}.json")
        report_path = os.path.join(config.OUTPUT_DIR, f"development_{self.current_task.id}.md")
        document_path = os.path.join(config.OUTPUT_DIR, f"final_document_{self.current_task.id}.md")
        
        return {
            "task_id": self.current_task.id,
            "status": "completed",
            "questions_path": questions_path if os.path.exists(questions_path) else None,
            "report_path": report_path if os.path.exists(report_path) else None,
            "document_path": document_path if os.path.exists(document_path) else None
        }

