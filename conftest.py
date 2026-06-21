"""
Configuración compartida para pytest.
Agrega la raíz del proyecto al path para que los tests
puedan importar desde src/ sin problemas.
"""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))