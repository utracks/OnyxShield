import os
import sys
from pathlib import Path
from typing import Optional
from .core import ObfuscationEngine
from .utils import Colors, display_banner, validate_file

def main():
    display_banner()
    
    # File selection
    target = get_valid_input(
        prompt=f"{Colors.PURPLE}[>] Python file to protect: {Colors.RESET}",
        validator=validate_file,
        error_msg="File does not exist"
    )

    # Get options
    options = {
        'anti_debug': get_boolean_input("Enable anti-debugging?"),
        'rename': get_boolean_input("Obfuscate identifiers?"),
        'encrypt_strings': get_boolean_input("Encrypt strings?"),
        'compress': get_boolean_input("Compress output?"),
        'junk_code': get_boolean_input("Add junk code?")
    }

    # Process file
    try:
        with open(target, 'r', encoding='utf-8') as f:
            code = f.read()
        
        protected = ObfuscationEngine().transform(code, **options)
        output = save_output(target, protected)
        
        if not options['compress']:
            handle_compilation(output)
            
    except Exception as e:
        print(f"{Colors.RED}[!] Error: {str(e)}{Colors.RESET}")
        sys.exit(1)

def get_valid_input(prompt: str, validator, error_msg: str) -> str:
    """Get validated user input"""
    while True:
        value = input(prompt).strip()
        if validator(value):
            return value
        print(f"{Colors.RED}[!] {error_msg}{Colors.RESET}")

def get_boolean_input(prompt: str) -> bool:
    """Get yes/no input"""
    return input(
        f"{Colors.PURPLE}[>] {prompt} (Y/n): {Colors.RESET}"
    ).lower() != 'n'

def save_output(original_path: str, content: str) -> str:
    """Save obfuscated file"""
    output = f"{Path(original_path).stem}_protected.py"
    with open(output, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"{Colors.GREEN}[✓] Protected file saved to: {output}{Colors.RESET}")
    return output

def handle_compilation(file_path: str):
    """Handle EXE compilation if requested"""
    if get_boolean_input("Compile to executable?"):
        print(f"{Colors.YELLOW}[!] Compiling with Nuitka...{Colors.RESET}")
        os.system(f"nuitka --onefile --standalone {file_path}")
        print(f"{Colors.GREEN}[✓] Executable created{Colors.RESET}")

if __name__ == "__main__":
    main()