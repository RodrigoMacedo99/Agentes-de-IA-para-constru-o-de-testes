#!/usr/bin/env python3
"""
Script para executar todos os testes do sistema.
"""

import unittest
import sys
import os

# Adiciona o diretório raiz ao path para importar os módulos
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))


def run_tests():
    """
    Executa todos os testes do sistema.
    """
    # Descobre e executa todos os testes
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover('tests', pattern='test_*.py')
    
    # Executa os testes
    test_runner = unittest.TextTestRunner(verbosity=2)
    result = test_runner.run(test_suite)
    
    # Retorna o código de saída
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_tests())

