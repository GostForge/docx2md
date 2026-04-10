import re

def normalize_headings(content: str) -> str:
    def heading_replacer(m: re.Match) -> str:
        hashes = m.group(1).strip()
        number = m.group(2)
        text = m.group(3)
        
        if not hashes:
            if re.match(r'^\d+\.$', number):
                return m.group(0)
            
            level = number.strip('.').count('.') + 1
            hashes = '#' * min(level, 6)
            
        return f"{hashes} {text}"
        
    heading_pattern = re.compile(r'^([#\s]*?)(\d+(?:\.\d+)*\.?)\s+([A-ZА-ЯЁ].*)$', re.MULTILINE)
    content = heading_pattern.sub(heading_replacer, content)
    content = re.sub(r'([^\n])\n(#+\s)', r'\1\n\n\2', content)
    return content

print(repr(normalize_headings("1. Ускорение реагирования\n1.1 Задание\n# 1 ПРАКТИЧЕСКАЯ\n3 ПРАКТИЧЕСКАЯ\n# 1. Заголовок")))
