import re

content = """# 1 ПРАКТИЧЕСКАЯ РАБОТА №5

1.1 Задание на практическую работу

1.  Построить структурные диаграммы своего проекта.

## 1.2 Выполнение работы

2 ПРАКТИЧЕСКАЯ РАБОТА №6

2.1 Задание на практическую работу
"""

# Match existing headings: # 1.2.3 Text -> # Text
# Match missing headings: 1.2.3 Text -> #... Text

def replacer(m):
    hashes = m.group(1).strip()
    number = m.group(2)
    text = m.group(3)
    
    # If no hashes, we determine level by number of dots
    if not hashes:
        level = number.count('.') + 1
        hashes = '#' * level
        
    return f"{hashes} {text}"

# Regex for heading lines
# Matches optional hashes and spaces
# Then digit(s)(.digit(s))* 
# Then a space 
# Then an Uppercase letter or uppercase Cyrillic
# Oh wait, "Задание" is Uppercase 'З'. "ПРАКТИЧЕСКАЯ" is Uppercase.
# List items like "1.  " have a trailing dot and two spaces. Handled automatically since they won't match (\d+(?:\.\d+)*) followed immediately by space without trailing dot if it's "1.". Wait! "2 ПРАКТИЧЕСКАЯ" has no trailing dot. "1.1 Задание" has no trailing dot.
# So number format: `\d+(?:\.\d+)*` with NO trailing dot!
pattern = re.compile(r'^([#\s]*?)(\d+(?:\.\d+)*)\s+([A-ZА-ЯЁ].*)$', re.MULTILINE)
print(pattern.sub(replacer, content))
