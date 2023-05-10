import re
import pyperclip
'''
Applies RegEx substitutions to the string in your clipboard:
 - Remove commented out lines
 - Escape double quotes
 - Remove newlines
'''
### Vars
replacements = [
    (r"\#.*?\n", ""),
    (r'\\', r'\\\\'),
    (r"\"", r'\\"'),
    (r"\n\#.*?\n", ""),
    (r"\r\n", ""),
    (r"\ +", " "),
    (r'\$(.*?)\$', r'\\\(\1\\\)')
]

### Runtime
# Load str from clipboard
a = pyperclip.paste()

# Apply replaces to str
for pattern, repl in replacements:
    a = re.sub(pattern, repl, a)

# Load str back into clipboard
pyperclip.copy(a)
print(a)
