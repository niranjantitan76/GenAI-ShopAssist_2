# This makes the whole `src` a package
# Usually left empty, but you can define version info if needed

__version__ = "0.1.0"
# Expose all route modules
from .chat_router import completion
from .dictionary_router import present
from .dialog_router import  run_dialogue
__all__ = ["completion","present","run_dialogue"]
