# onyxshield/utils.py
import os
import sys
from typing import Union
from pathlib import Path

class Colors:
    PURPLE = '\033[95m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    RESET = '\033[0m'

def display_banner():
    banner = rf"""
{Colors.PURPLE}

{Colors.RESET}
 ██████╗ ███╗   ██╗██╗   ██╗██╗  ██╗
██╔═══██╗████╗  ██║╚██╗ ██╔╝╚██╗██╔╝
██║   ██║██╔██╗ ██║ ╚████╔╝  ╚███╔╝ 
██║   ██║██║╚██╗██║  ╚██╔╝   ██╔██╗ 
╚██████╔╝██║ ╚████║   ██║   ██╔╝ ██╗
 ╚═════╝ ╚═╝  ╚═══╝   ╚═╝   ╚═╝  ╚═╝
                                    

    """
    print(banner)

def validate_file(path: Union[str, Path]) -> bool:
    """Check if file exists"""
    if not os.path.exists(path):
        print(f"{Colors.RED}[!] File does not exist{Colors.RESET}")
        return False
    return True