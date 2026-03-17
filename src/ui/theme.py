# -*- coding: utf-8 -*-
"""
程序员计算器 - 主题配置
提供深色主题和样式配置
"""

import flet as ft
from typing import Final


# 颜色常量
PRIMARY_COLOR: Final[str] = "#0078D4"
BACKGROUND_COLOR: Final[str] = "#1E1E1E"
SURFACE_COLOR: Final[str] = "#2D2D2D"
BUTTON_BG_COLOR: Final[str] = "#3C3C3C"
TEXT_COLOR: Final[str] = "#FFFFFF"


def get_dark_theme() -> ft.Theme:
    """
    获取程序员计算器深色主题

    Returns:
        ft.Theme: Flet主题对象
    """
    return ft.Theme(
        # 主色调种子，用于生成配色方案
        color_scheme_seed=PRIMARY_COLOR,

        # 自定义配色方案
        color_scheme=ft.ColorScheme(
            primary=PRIMARY_COLOR,           # 主色
            on_primary=TEXT_COLOR,           # 主色上的文字
            primary_container="#1A5FB4",     # 主色容器
            on_primary_container=TEXT_COLOR, # 主色容器上的文字

            secondary=BUTTON_BG_COLOR,       # 次级色
            on_secondary=TEXT_COLOR,         # 次级色上的文字
            secondary_container="#4A4A4A",   # 次级色容器

            surface=SURFACE_COLOR,           # 表面色
            on_surface=TEXT_COLOR,           # 表面上的文字
            surface_variant="#3C3C3C",       # 表面变体

            background=BACKGROUND_COLOR,     # 背景色
            on_background=TEXT_COLOR,        # 背景上的文字

            error="#FF3B30",                 # 错误色
            on_error=TEXT_COLOR,             # 错误色上的文字

            outline="#505050",               # 轮廓色
            outline_variant="#3C3C3C",       # 轮廓变体
        ),

        # 按钮主题
        button_theme=ft.ButtonTheme(
            style=ft.ButtonStyle(
                padding=ft.padding.all(12),
                shape=ft.RoundedRectangleBorder(radius=8),
            ),
        ),

        # 文本主题
        text_theme=ft.TextTheme(
            # 大标题
            headline_large=ft.TextStyle(
                size=36,
                weight=ft.FontWeight.W_300,
                color=TEXT_COLOR,
            ),
            # 标题
            title_medium=ft.TextStyle(
                size=16,
                weight=ft.FontWeight.W_500,
                color=TEXT_COLOR,
            ),
            # 正文
            body_large=ft.TextStyle(
                size=14,
                color=TEXT_COLOR,
            ),
            # 标签
            label_large=ft.TextStyle(
                size=12,
                weight=ft.FontWeight.W_500,
                color="#9E9E9E",
            ),
        ),

        # 输入框主题
        input_decoration_theme=ft.InputDecorationTheme(
            filled=True,
            fill_color=SURFACE_COLOR,
            border=ft.InputBorder.NONE,
            content_padding=ft.padding.all(16),
        ),

        # 应用栏主题
        appbar_theme=ft.AppBarTheme(
            bgcolor=BACKGROUND_COLOR,
            color=TEXT_COLOR,
            elevation=0,
        ),
    )


def apply_dark_theme(page: ft.Page) -> None:
    """
    应用深色主题到页面

    Args:
        page: Flet页面对象
    """
    # 设置主题模式为深色
    page.theme_mode = ft.ThemeMode.DARK

    # 应用自定义深色主题
    page.theme = get_dark_theme()

    # 设置背景色
    page.bgcolor = BACKGROUND_COLOR

    # 启用自适应模式（根据平台自动调整样式）
    page.adaptive = True


def get_button_style(
    bgcolor: str = BUTTON_BG_COLOR,
    color: str = TEXT_COLOR,
    radius: int = 8,
) -> ft.ButtonStyle:
    """
    获取自定义按钮样式

    Args:
        bgcolor: 背景颜色
        color: 文字颜色
        radius: 圆角半径

    Returns:
        ft.ButtonStyle: 按钮样式对象
    """
    return ft.ButtonStyle(
        color={
            ft.ControlState.DEFAULT: color,
            ft.ControlState.DISABLED: "#666666",
        },
        bgcolor={
            ft.ControlState.DEFAULT: bgcolor,
            ft.ControlState.HOVERED: "#4A4A4A" if bgcolor == BUTTON_BG_COLOR else bgcolor,
            ft.ControlState.PRESSED: "#505050" if bgcolor == BUTTON_BG_COLOR else bgcolor,
            ft.ControlState.DISABLED: "#2D2D2D",
        },
        padding=ft.padding.all(12),
        shape=ft.RoundedRectangleBorder(radius=radius),
    )


def get_digit_button_style() -> ft.ButtonStyle:
    """获取数字按钮样式"""
    return get_button_style(
        bgcolor=BUTTON_BG_COLOR,
        color=TEXT_COLOR,
    )


def get_operator_button_style() -> ft.ButtonStyle:
    """获取运算符按钮样式（橙色）"""
    return get_button_style(
        bgcolor="#FF9500",
        color=TEXT_COLOR,
    )


def get_function_button_style() -> ft.ButtonStyle:
    """获取功能按钮样式"""
    return get_button_style(
        bgcolor=SURFACE_COLOR,
        color="#9E9E9E",
    )


def get_hex_button_style() -> ft.ButtonStyle:
    """获取十六进制按钮样式"""
    return get_button_style(
        bgcolor=BUTTON_BG_COLOR,
        color="#FF6B6B",  # 红色调
    )


def get_equals_button_style() -> ft.ButtonStyle:
    """获取等号按钮样式（蓝色）"""
    return get_button_style(
        bgcolor=PRIMARY_COLOR,
        color=TEXT_COLOR,
    )