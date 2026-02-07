import logging
from rich.logging import RichHandler
from rich.console import Console

console = Console()

def setup_logging(verbose: bool = False):
    """
    Configure logging with Rich handler.
    
    Args:
        verbose: If True, set level to DEBUG. Otherwise, INFO.
    """
    level = logging.DEBUG if verbose else logging.INFO
    
    logging.basicConfig(
        level=level,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(console=console, rich_tracebacks=True, show_path=False)]
    )
    
    log = logging.getLogger("ask")
    log.setLevel(level)
    
    if verbose:
        log.debug("Verbose logging enabled")
        
    return log
