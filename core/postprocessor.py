import re
from typing import List, Callable

class CodeBlockMasker:
    """
    Masks markdown code blocks and inline code to prevent regexes from incorrectly
    modifying user-provided examples (e.g. if the user documents [TOC] or &nbsp;).
    """
    def __init__(self) -> None:
        self._blocks: List[str] = []
        # Match fenced code blocks (```...```) and inline code (`...`)
        self._block_pattern = re.compile(r'(```.*?```)', re.DOTALL)
        self._inline_pattern = re.compile(r'(`[^`]*?`)')

    def mask(self, text: str) -> str:
        self._blocks.clear()
        
        def repl(match: re.Match) -> str:
            placeholder = f"__CODE_MASK_{len(self._blocks)}__"
            self._blocks.append(match.group(1))
            return placeholder

        text = self._block_pattern.sub(repl, text)
        text = self._inline_pattern.sub(repl, text)
        return text

    def unmask(self, text: str) -> str:
        for i, block in enumerate(self._blocks):
            text = text.replace(f"__CODE_MASK_{i}__", block)
        return text

class PostprocessorPipeline:
    """
    Executes a sequence of text transformation rules on markdown content.
    Automatically protects code segments from corruption.
    """
    def __init__(self) -> None:
        self._masker = CodeBlockMasker()
        self._rules: List[Callable[[str], str]] = []

    def add_rule(self, rule: Callable[[str], str]) -> 'PostprocessorPipeline':
        self._rules.append(rule)
        return self

    def process(self, content: str) -> str:
        content = self._masker.mask(content)
        for rule in self._rules:
            content = rule(content)
        content = self._masker.unmask(content)
        return content

# ----- Individual Transformation Rules -----

def fix_toc_escaping(content: str) -> str:
    """
    Restores the [TOC] marker that Pandoc typically escapes.
    Uses strict anchoring (^...$) so it only matches lines consisting entirely of the escaped TOC marker.
    """
    return re.sub(r'^\\\[TOC\\\]\s*$', '[TOC]', content, flags=re.MULTILINE)

def remove_empty_paragraphs(content: str) -> str:
    """
    Pandoc converts empty paragraphs from Word into &nbsp; alone on a line.
    This safely removes those specific empty line artifacts without breaking
    places where the user legitimately wrote about the `&nbsp;` symbol inline outside of code blocks.
    """
    return re.sub(r'^&nbsp;\s*$', '', content, flags=re.MULTILINE)

def integrate_image_captions(content: str) -> str:
    """
    Integrates image captions (e.g. 'Рисунок 1 - ...') directly into markdown image tags' alt text.
    """
    pattern = re.compile(
        r'!\[([^\]]*?)\]\(([^)]*)\)\n*Рисунок\s*[\d.]*\s*[-–—]\s*(.*?)(?=\n\n|\Z)',
        re.DOTALL
    )
    return pattern.sub(
        lambda m: f"![{m.group(3).replace(chr(10), ' ').strip()}]({m.group(2)})",
        content
    )

def normalize_lists(content: str) -> str:
    """
    Fixes blockquotes that are actually lists (e.g., "> ● " or "> 1\\. ").
    Matches only lines explicitly starting with '> '.
    """
    lines = content.split('\n')
    new_lines = []
    for line in lines:
        if line.startswith("> "):
            line_content = line[2:]
            if line_content.startswith("● "):
                line_content = "- " + line_content[2:]
            elif line_content == "":
                pass  # Keep empty line as is without blockquote
            else:
                if not re.match(r'^\d+\\\.', line_content) and not line_content.startswith("- "):
                    line_content = "  " + line_content
            new_lines.append(line_content)
        elif line.startswith(">"):
            new_lines.append(line[1:])
        else:
            new_lines.append(line)
    return "\n".join(new_lines)

def normalize_escaped_ordered_lists(content: str) -> str:
    """
    Converts escaped ordered list markers produced by Pandoc (e.g. '1\\.')
    into proper Markdown ordered lists and removes extra blank lines between
    consecutive ordered list entries.
    """
    content = re.sub(r'^(\s*\d+)\\\.\s+', r'\1. ', content, flags=re.MULTILINE)
    content = re.sub(r'^(\s*\d+\.\s[^\n]+)\n{2,}(?=\s*\d+\.\s)', r'\1\n', content, flags=re.MULTILINE)
    return content

def normalize_headings(content: str) -> str:
    """
    Removes GOST numbering from existing markdown headings and converts
    manually numbered headings into proper markdown headings automatically.
    """
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
    
    # Ensure an empty line before all headings if there isn't one already
    content = re.sub(r'([^\n])\n(#+\s)', r'\1\n\n\2', content)
    return content

def apply_postprocessing(content: str) -> str:
    """
    Configures and runs the post-processing pipeline.
    """
    pipeline = PostprocessorPipeline()
    pipeline.add_rule(fix_toc_escaping)\
            .add_rule(remove_empty_paragraphs)\
            .add_rule(integrate_image_captions)\
            .add_rule(normalize_lists)\
            .add_rule(normalize_escaped_ordered_lists)\
            .add_rule(normalize_headings)
            
    return pipeline.process(content)
