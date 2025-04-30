import ast
import random
import string
import zlib
import base64
from typing import Dict, Set, Optional
from .encrypt import AESEncryptor

class ObfuscationEngine:
    def __init__(self):
        self.name_map: Dict[str, str] = {}
        self.used_names: Set[str] = set()
        self.encryptor = AESEncryptor()

    def transform(self, code: str, **options) -> str:
        """Main obfuscation pipeline"""
        if options.get('anti_debug'):
            code = self._inject_anti_debug(code)
        if options.get('rename'):
            code = self._rename_identifiers(code)
        if options.get('encrypt_strings'):
            code = self._encrypt_strings(code)
        if options.get('compress'):
            code = self._compress(code)
        if options.get('junk_code'):
            code = self._add_junk_code(code)
        return code

    def _generate_secure_name(self) -> str:
        """Generate non-repeating random identifiers"""
        while True:
            name = ''.join(random.choices(string.ascii_letters + '_', k=16))
            if name not in self.used_names:
                self.used_names.add(name)
                return name

    def _rename_identifiers(self, code: str) -> str:
        """Obfuscate all variable/function/class names"""
        tree = ast.parse(code)
        
        class NameTransformer(ast.NodeTransformer):
            def __init__(self, outer):
                self.outer = outer
            
            def visit_Name(self, node):
                if isinstance(node.ctx, ast.Store):
                    node.id = self.outer._get_mapped_name(node.id)
                return node
            
            def visit_FunctionDef(self, node):
                node.name = self.outer._get_mapped_name(node.name)
                return self.generic_visit(node)
            
            def visit_ClassDef(self, node):
                node.name = self.outer._get_mapped_name(node.name)
                return self.generic_visit(node)
        
        NameTransformer(self).visit(tree)
        return ast.unparse(tree)

    def _get_mapped_name(self, original: str) -> str:
        """Get or create obfuscated name mapping"""
        if original not in self.name_map:
            self.name_map[original] = self._generate_secure_name()
        return self.name_map[original]

    def _encrypt_strings(self, code: str) -> str:
        """Encrypt all string literals"""
        tree = ast.parse(code)
        
        class StringEncryptor(ast.NodeTransformer):
            def visit_Constant(self, node):
                if isinstance(node.value, str):
                    encrypted = self.outer.encryptor.encrypt(node.value)
                    return ast.Call(
                        func=ast.Attribute(
                            value=ast.Call(
                                func=ast.Name(id='base64.b64decode', ctx=ast.Load()),
                                args=[ast.Constant(value=encrypted)],
                                keywords=[]),
                            attr='decode',
                            ctx=ast.Load()),
                        args=[],
                        keywords=[])
                return node
        
        StringEncryptor().visit(tree)
        return ast.unparse(tree)

    def _compress(self, code: str) -> str:
        """Compress and encode entire script"""
        compressed = zlib.compress(code.encode())
        return f"import zlib,base64;exec(zlib.decompress(base64.b64decode('{base64.b64encode(compressed).decode()}').decode())"

    def _inject_anti_debug(self, code: str) -> str:
        """Add anti-debugging measures"""
        return """
import sys, ctypes
if hasattr(sys, 'gettrace') and sys.gettrace():
    sys.exit(0)
if ctypes.windll.kernel32.IsDebuggerPresent():
    ctypes.windll.kernel32.TerminateProcess(-1, 0)
""" + code

    def _add_junk_code(self, code: str) -> str:
        """Insert meaningless but functional statements"""
        junk = [
            f"{self._generate_secure_name()} = lambda: None",
            "for _ in range(random.randint(1,5)): pass",
            "if True: None"
        ]
        lines = code.split('\n')
        for i in range(len(lines)-1, 0, -1):
            if random.random() > 0.7:  # 30% chance per line
                lines.insert(i, random.choice(junk))
        return '\n'.join(lines)