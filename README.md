# 🔒 OnyxShield - Python Obfuscator

```bash
onyxshield input.py --rename --encrypt --compress --output protected.py
Features:
--rename : Obfuscate all names

--encrypt : AES-256 string encryption

--compress : Code compression

--anti-debug : Debugger protection

Programmatic Use:

from onyxshield import obfuscate_code
print(obfuscate_code("print('secret')", rename=True))
