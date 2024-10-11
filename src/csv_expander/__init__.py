from .cli import cli
from .utils import version

__version__ = version()
__all__ = ["__version__", "cli"]
