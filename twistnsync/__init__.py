"""Top-level package for Twist-n-Sync."""

__author__ = """Marsel Faizullin"""
__email__ = 'marsel.faizullin@skoltech.ru'
__version__ = '0.1.0'

from . import twistnsync

for module in dir(twistnsync):
    n = len(module) - 1
    if not (module[:2] == '__' and module[n:n-2:-1] == '__') and module.count('.') == 0:
        globals()[module] = getattr(twistnsync, module)

del twistnsync
