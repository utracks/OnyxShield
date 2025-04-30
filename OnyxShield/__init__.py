"""
OnyxShield - Advanced Python Code Protection System

Provides:
- Source code obfuscation
- String encryption
- Anti-debugging techniques
- Executable packaging
"""

__version__ = "2.5.0"
__author__ = "Security Engineering Team"
__license__ = "GPL-3.0"

# Core API exports
from .core import ObfuscationEngine
from .encrypt import AESEncryptor
from .cli import main as cli_main

# Shortcut functions for common operations
def obfuscate_code(source: str, **options) -> str:
    """One-line obfuscation interface"""
    return ObfuscationEngine().transform(source, **options)

def protect_file(input_path: str, output_path: str = None, **options) -> str:
    """
    Protect a Python source file
    Args:
        input_path: Path to source file
        output_path: Optional output path
        **options: Obfuscation options
    
    Returns:
        Path to protected file
    """
    with open(input_path, 'r', encoding='utf-8') as f:
        code = f.read()
    
    protected = obfuscate_code(code, **options)
    output = output_path or f"{input_path.split('.')[0]}_protected.py"
    
    with open(output, 'w', encoding='utf-8') as f:
        f.write(protected)
    
    return output

# Package initialization checks
try:
    from Crypto.Cipher import AES  # noqa
except ImportError:
    raise ImportError(
        "Required cryptography packages not found. "
        "Install with: pip install pycryptodome"
    )

__all__ = [
    'ObfuscationEngine',
    'AESEncryptor',
    'obfuscate_code',
    'protect_file',
    'cli_main'
]