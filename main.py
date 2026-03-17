# -*- coding: utf-8 -*-
"""
程序员计算器入口文件
Flet构建时需要在项目根目录有main.py或使用--module-name参数
"""

from src.main import main
import flet as ft

if __name__ == "__main__":
    ft.app(target=main)