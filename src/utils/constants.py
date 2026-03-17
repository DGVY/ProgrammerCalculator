# -*- coding: utf-8 -*-
"""
程序员计算器 - 常量定义
定义颜色、尺寸、按钮样式等常量
"""

from enum import Enum
from typing import Dict, Final


# ==================== 颜色常量 ====================
class COLORS:
    """颜色常量定义"""

    # 主题色
    PRIMARY: Final[str] = "#0078D4"  # 蓝色主色
    BACKGROUND: Final[str] = "#1E1E1E"  # 深灰背景
    SURFACE: Final[str] = "#2D2D2D"  # 表面色
    BUTTON_BG: Final[str] = "#3C3C3C"  # 按钮背景
    BUTTON_BG_HOVER: Final[str] = "#4A4A4A"  # 按钮悬停背景
    BUTTON_BG_ACTIVE: Final[str] = "#505050"  # 按钮激活背景

    # 文字颜色
    TEXT_PRIMARY: Final[str] = "#FFFFFF"  # 主文字白色
    TEXT_SECONDARY: Final[str] = "#9E9E9E"  # 次级文字灰色
    TEXT_DISABLED: Final[str] = "#666666"  # 禁用文字

    # 功能色
    ACCENT_ORANGE: Final[str] = "#FF9500"  # 运算符橙色
    ACCENT_GREEN: Final[str] = "#34C759"  # 确认绿色
    ACCENT_RED: Final[str] = "#FF3B30"  # 错误红色

    # 进制指示色
    HEX_COLOR: Final[str] = "#FF6B6B"  # 十六进制红
    DEC_COLOR: Final[str] = "#4ECDC4"  # 十进制青
    OCT_COLOR: Final[str] = "#FFE66D"  # 八进制黄
    BIN_COLOR: Final[str] = "#95E1D3"  # 二进制绿


# ==================== 尺寸常量 ====================
class SIZES:
    """尺寸常量定义"""

    # 窗口尺寸
    WINDOW_WIDTH: Final[int] = 400
    WINDOW_HEIGHT: Final[int] = 700
    MIN_WINDOW_WIDTH: Final[int] = 350
    MIN_WINDOW_HEIGHT: Final[int] = 600

    # 按钮尺寸
    BUTTON_WIDTH: Final[int] = 60
    BUTTON_HEIGHT: Final[int] = 50
    BUTTON_SPACING: Final[int] = 5
    BUTTON_RADIUS: Final[int] = 8

    # 字体尺寸
    FONT_SIZE_DISPLAY: Final[int] = 36
    FONT_SIZE_BUTTON: Final[int] = 20
    FONT_SIZE_LABEL: Final[int] = 14
    FONT_SIZE_BINARY: Final[int] = 12

    # 内边距
    PADDING_SMALL: Final[int] = 8
    PADDING_MEDIUM: Final[int] = 16
    PADDING_LARGE: Final[int] = 24


# ==================== 运算符常量 ====================
class OPERATORS:
    """运算符常量定义"""

    # 基础运算符
    ADD: Final[str] = "+"
    SUBTRACT: Final[str] = "-"
    MULTIPLY: Final[str] = "×"
    DIVIDE: Final[str] = "÷"
    EQUALS: Final[str] = "="
    PERCENT: Final[str] = "%"

    # 位运算符
    AND: Final[str] = "AND"
    OR: Final[str] = "OR"
    XOR: Final[str] = "XOR"
    NOT: Final[str] = "NOT"
    LSHIFT: Final[str] = "<<"
    RSHIFT: Final[str] = ">>"
    ROL: Final[str] = "RoL"
    ROR: Final[str] = "RoR"

    # 括号
    LEFT_PAREN: Final[str] = "("
    RIGHT_PAREN: Final[str] = ")"

    # 控制按钮
    CLEAR: Final[str] = "C"
    CLEAR_ENTRY: Final[str] = "CE"
    BACKSPACE: Final[str] = "⌫"
    SIGN_TOGGLE: Final[str] = "±"


# ==================== 位模式常量 ====================
class BIT_MODES:
    """位模式常量定义"""

    QWORD: Final[int] = 64  # 四字 (64位)
    DWORD: Final[int] = 32  # 双字 (32位)
    WORD: Final[int] = 16   # 字 (16位)
    BYTE: Final[int] = 8    # 字节 (8位)

    # 位模式名称映射
    NAMES: Final[Dict[int, str]] = {
        64: "QWORD",
        32: "DWORD",
        16: "WORD",
        8: "BYTE",
    }

    # 位模式最大值 (有符号)
    MAX_VALUES: Final[Dict[int, int]] = {
        64: (1 << 63) - 1,
        32: (1 << 31) - 1,
        16: (1 << 15) - 1,
        8: (1 << 7) - 1,
    }

    # 位模式最小值 (有符号)
    MIN_VALUES: Final[Dict[int, int]] = {
        64: -(1 << 63),
        32: -(1 << 31),
        16: -(1 << 15),
        8: -(1 << 7),
    }


# ==================== 按钮样式常量 ====================
class BUTTON_STYLE:
    """按钮样式常量定义"""

    # 数字按钮样式
    DIGIT: Final[Dict] = {
        "bgcolor": COLORS.BUTTON_BG,
        "color": COLORS.TEXT_PRIMARY,
    }

    # 运算符按钮样式
    OPERATOR: Final[Dict] = {
        "bgcolor": COLORS.ACCENT_ORANGE,
        "color": COLORS.TEXT_PRIMARY,
    }

    # 功能按钮样式
    FUNCTION: Final[Dict] = {
        "bgcolor": COLORS.SURFACE,
        "color": COLORS.TEXT_SECONDARY,
    }

    # 十六进制按钮样式
    HEX_DIGIT: Final[Dict] = {
        "bgcolor": COLORS.BUTTON_BG,
        "color": COLORS.HEX_COLOR,
    }

    # 等号按钮样式
    EQUALS: Final[Dict] = {
        "bgcolor": COLORS.PRIMARY,
        "color": COLORS.TEXT_PRIMARY,
    }


# ==================== 进制常量 ====================
class NumberBaseEnum(int, Enum):
    """进制枚举"""

    HEX = 16  # 十六进制
    DEC = 10  # 十进制
    OCT = 8   # 八进制
    BIN = 2   # 二进制


# ==================== 键盘映射 ====================
class KEYBOARD_MAP:
    """键盘快捷键映射"""

    # 数字键
    DIGIT_KEYS: Final[str] = "0123456789ABCDEF"

    # 运算符键映射
    OPERATOR_KEYS: Final[Dict[str, str]] = {
        "+": OPERATORS.ADD,
        "-": OPERATORS.SUBTRACT,
        "*": OPERATORS.MULTIPLY,
        "/": OPERATORS.DIVIDE,
        "Enter": OPERATORS.EQUALS,
        "=": OPERATORS.EQUALS,
        "%": OPERATORS.PERCENT,
        "(": OPERATORS.LEFT_PAREN,
        ")": OPERATORS.RIGHT_PAREN,
    }

    # 控制键映射
    CONTROL_KEYS: Final[Dict[str, str]] = {
        "Escape": OPERATORS.CLEAR,
        "Backspace": OPERATORS.BACKSPACE,
        "Delete": OPERATORS.CLEAR_ENTRY,
    }