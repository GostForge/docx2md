# Expose necessary components in the core module
from .preprocessor import remove_toc_and_add_placeholder
from .postprocessor import apply_postprocessing
from .converter import DocxToMdConverter

__all__ = [
    'remove_toc_and_add_placeholder',
    'apply_postprocessing',
    'DocxToMdConverter'
]