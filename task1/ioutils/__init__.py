"""
ioutils package

提供与用户交互相关的输入/输出工具。
目前包含:
- prompts.py: 用户输入处理（整数校验等）

未来如果你加入 views.py，或更多 I/O 相关模块，也会在这里统一管理。
"""

from .prompts import ask_positive_int

__all__ = ["ask_positive_int"]
