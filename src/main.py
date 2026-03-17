# -*- coding: utf-8 -*-
"""
程序员计算器
跨平台进制转换计算器应用

功能特性:
- 多进制显示与编辑 (HEX/DEC/OCT/BIN)
- 64位二进制位显示 (QWORD/DWORD/WORD/BYTE)
- 基础运算 (+、-、×、÷)
- 位运算操作 (AND, OR, XOR, NOT, 移位)
- 存储功能 (MS/MR/MC/M+)
"""

import flet as ft

from src.ui.app import ProgrammerCalculatorApp


def main(page: ft.Page) -> None:
    """
    应用程序入口函数

    Args:
        page: Flet页面对象
    """
    app = ProgrammerCalculatorApp(page)
    app.run()


if __name__ == "__main__":
    ft.app(target=main)