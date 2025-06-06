"""
Utilitários para processamento de texto.
"""

import re
import json
from typing import Dict, Any, List, Optional, Set, Tuple


def extract_json_from_text(text: str) -> Dict[str, Any]:
    """
    Extrai um objeto JSON de um texto.
    
    Args:
        text: Texto contendo JSON
        
    Returns:
        Dicionário com o conteúdo JSON extraído
    """
    # Procura por blocos de código JSON
    json_pattern = r"```(?:json)?\s*([\s\S]*?)```"
    matches = re.findall(json_pattern, text)
    
    if matches:
        # Usa o maior bloco encontrado (provavelmente o mais completo)
        json_str = max(matches, key=len).strip()
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar JSON: {e}")
    
    # Se não encontrou blocos de código, tenta extrair diretamente
    try:
        # Procura por chaves de abertura e fechamento
        start = text.find('{')
        end = text.rfind('}')
        if start != -1 and end != -1 and start < end:
            json_str = text[start:end+1]
            return json.loads(json_str)
    except json.JSONDecodeError:
        pass
    
    # Se tudo falhar, retorna um dicionário vazio
    return {}


def extract_markdown_sections(text: str) -> Dict[str, str]:
    """
    Extrai seções de um texto em formato Markdown.
    
    Args:
        text: Texto em formato Markdown
        
    Returns:
        Dicionário com as seções extraídas
    """
    sections = {}
    current_section = "default"
    current_content = []
    
    # Padrão para cabeçalhos Markdown
    header_pattern = r"^(#{1,6})\s+(.+)$"
    
    for line in text.split('\n'):
        match = re.match(header_pattern, line)
        if match:
            # Se encontrou um cabeçalho, salva a seção atual e inicia uma nova
            if current_content:
                sections[current_section] = '\n'.join(current_content).strip()
                current_content = []
            
            level = len(match.group(1))  # Número de # no cabeçalho
            title = match.group(2).strip()
            current_section = f"h{level}:{title}"
            current_content.append(line)
        else:
            current_content.append(line)
    
    # Salva a última seção
    if current_content:
        sections[current_section] = '\n'.join(current_content).strip()
    
    return sections


def check_restricted_words(text: str, stopwords: List[str]) -> List[Tuple[str, int]]:
    """
    Verifica se o texto contém palavras restritivas.
    
    Args:
        text: Texto a ser verificado
        stopwords: Lista de palavras restritivas
        
    Returns:
        Lista de tuplas (palavra_encontrada, posição)
    """
    found = []
    text_lower = text.lower()
    
    for word in stopwords:
        word_lower = word.lower()
        start = 0
        while True:
            pos = text_lower.find(word_lower, start)
            if pos == -1:
                break
            found.append((word, pos))
            start = pos + len(word)
    
    return sorted(found, key=lambda x: x[1])


def replace_restricted_words(text: str, stopwords: List[str], 
                            replacements: Optional[Dict[str, str]] = None) -> str:
    """
    Substitui palavras restritivas no texto.
    
    Args:
        text: Texto a ser processado
        stopwords: Lista de palavras restritivas
        replacements: Dicionário de substituições (palavra_original -> substituto)
        
    Returns:
        Texto com as palavras substituídas
    """
    if replacements is None:
        replacements = {
            "limita-se": "abrange",
            "estritamente": "adequadamente",
            "apenas": "principalmente",
            "exclusivamente": "especialmente",
            "somente": "preferencialmente",
            "unicamente": "particularmente",
            "restritivamente": "apropriadamente",
            "rigorosamente": "cuidadosamente",
            "especificamente": "notadamente",
            "exatamente": "precisamente",
            "precisamente": "detalhadamente",
            "unilateralmente": "diretamente",
            "singularmente": "distintamente",
            "determinadamente": "consistentemente",
            "explicitamente": "claramente",
            "meramente": "basicamente",
            "unicidade": "característica",
            "nada além de": "principalmente",
            "só isso": "isso",
            "e somente isso": "entre outros aspectos",
            "de forma exclusiva": "de forma destacada",
            "de modo restrito": "de modo específico",
            "de maneira limitada": "de maneira particular",
            "sem exceções": "em geral"
        }
    
    result = text
    found = check_restricted_words(text, stopwords)
    
    # Substitui de trás para frente para não afetar as posições
    for word, pos in reversed(found):
        word_lower = word.lower()
        replacement = replacements.get(word_lower, "")
        if not replacement:
            # Se não houver substituição específica, usa uma genérica
            if word.istitle():
                replacement = "Principalmente"
            elif word.isupper():
                replacement = "PRINCIPALMENTE"
            else:
                replacement = "principalmente"
        
        result = result[:pos] + replacement + result[pos + len(word):]
    
    return result


def extract_objectives(text: str) -> List[str]:
    """
    Extrai objetivos de aprendizagem de um texto.
    
    Args:
        text: Texto contendo objetivos
        
    Returns:
        Lista de objetivos extraídos
    """
    # Padrão para objetivos numerados (Obj.1:, Objetivo 1:, etc.)
    objective_pattern = r"(?:Obj(?:etivo)?\.?\s*(\d+)[:\.\)]\s*)(.*?)(?=(?:\n\s*Obj(?:etivo)?\.?\s*\d+[:\.\)])|$)"
    matches = re.findall(objective_pattern, text, re.DOTALL)
    
    objectives = []
    for num, content in matches:
        objective = f"Obj.{num}: {content.strip()}"
        objectives.append(objective)
    
    # Se não encontrou objetivos numerados, tenta por linhas
    if not objectives:
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        objectives = [line for line in lines if re.search(r"identificar|descrever|analisar|avaliar|compreender", line.lower())]
    
    return objectives


def extract_questions_from_text(text: str) -> List[Dict[str, Any]]:
    """
    Extrai questões de um texto.
    
    Args:
        text: Texto contendo questões
        
    Returns:
        Lista de questões extraídas
    """
    # Primeiro tenta extrair como JSON
    json_data = extract_json_from_text(text)
    if json_data:
        if isinstance(json_data, list):
            return json_data
        elif "questions" in json_data and isinstance(json_data["questions"], list):
            return json_data["questions"]
    
    # Se não conseguiu extrair como JSON, tenta extrair do texto
    questions = []
    
    # Padrão para questões de resposta única
    single_answer_pattern = r"(?:Questão|Question)\s+(\d+).*?(?:Contextualização|Context):(.*?)(?:Enunciado|Statement):(.*?)(?:Alternativas|Alternatives):(.*?)(?:Feedback):(.*?)(?=(?:Questão|Question)\s+\d+|$)"
    
    matches = re.findall(single_answer_pattern, text, re.DOTALL | re.IGNORECASE)
    
    for num, context, statement, alternatives_text, feedback_text in matches:
        # Processa alternativas
        alt_pattern = r"([a-e])\)\s*(.*?)(?=(?:[a-e]\))|$)"
        alt_matches = re.findall(alt_pattern, alternatives_text, re.DOTALL)
        
        alternatives = []
        for alt_id, alt_text in alt_matches:
            alternatives.append({
                "id": alt_id,
                "text": alt_text.strip(),
                "correct": False  # Será atualizado abaixo
            })
        
        # Processa feedback para identificar a alternativa correta
        feedback = {}
        correct_alt = None
        
        fb_pattern = r"([a-e])\)\s*(Correta|Incorreta)\.?\s*(.*?)(?=(?:[a-e]\))|$)"
        fb_matches = re.findall(fb_pattern, feedback_text, re.DOTALL | re.IGNORECASE)
        
        for fb_id, status, justification in fb_matches:
            feedback[fb_id] = f"{status}. {justification.strip()}"
            if status.lower() == "correta":
                correct_alt = fb_id
        
        # Atualiza a alternativa correta
        if correct_alt:
            for alt in alternatives:
                if alt["id"] == correct_alt:
                    alt["correct"] = True
        
        questions.append({
            "objective_id": f"Obj.{num}",
            "type": "single_answer",
            "context": context.strip(),
            "statement": statement.strip(),
            "alternatives": alternatives,
            "feedback": feedback
        })
    
    return questions

