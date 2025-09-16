# This makes the whole `src` a package
# Usually left empty, but you can define version info if needed
from .config import settings
from .http_client import get_http_client
__version__ = "0.1.0"
__all__ = ["settings","get_http_client"]
