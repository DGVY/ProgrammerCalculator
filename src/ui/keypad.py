# -*- coding: utf-8 -*-
"""
程序员计算器 - 数字键盘组件
提供数字、运算符、功能按钮的键盘布局
"""

import flet as ft
from typing import Callable, Optional, Dict, List
from enum import Enum

from src.utils.constants import COLORS, SIZES, OPERATORS
from src.ui.theme import (
    get_digit_button_style,
    get_operator_button_style,
    get_function_button_style,
    get_hex_button_style,
    get_equals_button_style,
)


class KeyType(str, Enum):
    """按键类型枚举"""

    DIGIT = "digit"           # 数字键 (0-9)
    HEX_DIGIT = "hex_digit"   # 十六进制数字键 (A-F)
    OPERATOR = "operator"     # 运算符键 (+, -, ×, ÷)
    FUNCTION = "function"     # 功能键 (C, ⌫, %)
    EQUALS = "equals"         # 等号键
    PAREN = "paren"           # 括号键
    SHIFT = "shift"           # 位移键 (<<, >>)


class CalculatorKey(ft.Button):
    """
    计算器按键控件

    统一的按键样式和行为
    """

    def __init__(
        self,
        content: str,
        key_type: KeyType = KeyType.DIGIT,
        on_click: Optional[Callable[[str], None]] = None,
        enabled: bool = True,
        **kwargs,
    ):
        """
        初始化按键

        Args:
            content: 按键显示内容
            key_type: 按键类型
            on_click: 点击回调函数
            enabled: 是否启用
        """
        # 根据类型选择样式
        style_map = {
            KeyType.DIGIT: get_digit_button_style(),
            KeyType.HEX_DIGIT: get_hex_button_style(),
            KeyType.OPERATOR: get_operator_button_style(),
            KeyType.FUNCTION: get_function_button_style(),
            KeyType.EQUALS: get_equals_button_style(),
            KeyType.PAREN: get_function_button_style(),
            KeyType.SHIFT: get_function_button_style(),
        }

        super().__init__(
            content=content,
            style=style_map.get(key_type, get_digit_button_style()),
            on_click=self._handle_click if on_click else None,
            disabled=not enabled,
            expand=1,
            **kwargs,
        )

        self._key_value = content
        self._on_click_callback = on_click
        self._key_type = key_type

    def _handle_click(self, e) -> None:
        """处理点击事件"""
        if self._on_click_callback:
            self._on_click_callback(self._key_value)

    def set_enabled(self, enabled: bool) -> None:
        """
        设置启用状态

        Args:
            enabled: 是否启用
        """
        self.disabled = not enabled
        self.update()


class Keypad(ft.Container):
    """
    数字键盘组件

    提供完整的计算器键盘布局
    """

    def __init__(
        self,
        on_key_press: Optional[Callable[[str], None]] = None,
        on_operator_press: Optional[Callable[[str], None]] = None,
        on_function_press: Optional[Callable[[str], None]] = None,
        hex_enabled: bool = True,
        **kwargs,
    ):
        """
        初始化键盘

        Args:
            on_key_press: 数字键按下回调
            on_operator_press: 运算符按下回调
            on_function_press: 功能键按下回调
            hex_enabled: 是否启用十六进制键
        """
        super().__init__(**kwargs)

        self._on_key_press = on_key_press
        self._on_operator_press = on_operator_press
        self._on_function_press = on_function_press
        self._hex_enabled = hex_enabled

        # 存储按键引用
        self._keys: Dict[str, CalculatorKey] = {}

        # 设置容器样式
        self.padding = ft.padding.all(SIZES.PADDING_SMALL)
        self.bgcolor = COLORS.BACKGROUND

        # 构建键盘
        self._build_keypad()

    def _build_keypad(self) -> None:
        """构建键盘布局"""
        # 键盘布局定义（从上到下，每行从左到右）
        # 格式: (显示内容, 键值, 按键类型)
        layout: List[List[tuple]] = [
            # 第一行: A-F十六进制键和位移操作
            [
                ("A", "A", KeyType.HEX_DIGIT),
                ("«", OPERATORS.LSHIFT, KeyType.SHIFT),
                ("»", OPERATORS.RSHIFT, KeyType.SHIFT),
                ("C", OPERATORS.CLEAR, KeyType.FUNCTION),
                ("⌫", OPERATORS.BACKSPACE, KeyType.FUNCTION),
            ],
            # 第二行
            [
                ("B", "B", KeyType.HEX_DIGIT),
                ("(", OPERATORS.LEFT_PAREN, KeyType.PAREN),
                (")", OPERATORS.RIGHT_PAREN, KeyType.PAREN),
                ("%", OPERATORS.PERCENT, KeyType.FUNCTION),
                ("÷", OPERATORS.DIVIDE, KeyType.OPERATOR),
            ],
            # 第三行
            [
                ("C", "C", KeyType.HEX_DIGIT),
                ("7", "7", KeyType.DIGIT),
                ("8", "8", KeyType.DIGIT),
                ("9", "9", KeyType.DIGIT),
                ("×", OPERATORS.MULTIPLY, KeyType.OPERATOR),
            ],
            # 第四行
            [
                ("D", "D", KeyType.HEX_DIGIT),
                ("4", "4", KeyType.DIGIT),
                ("5", "5", KeyType.DIGIT),
                ("6", "6", KeyType.DIGIT),
                ("−", OPERATORS.SUBTRACT, KeyType.OPERATOR),
            ],
            # 第五行
            [
                ("E", "E", KeyType.HEX_DIGIT),
                ("1", "1", KeyType.DIGIT),
                ("2", "2", KeyType.DIGIT),
                ("3", "3", KeyType.DIGIT),
                ("+", OPERATORS.ADD, KeyType.OPERATOR),
            ],
            # 第六行
            [
                ("F", "F", KeyType.HEX_DIGIT),
                ("±", OPERATORS.SIGN_TOGGLE, KeyType.FUNCTION),
                ("0", "0", KeyType.DIGIT),
                (".", ".", KeyType.FUNCTION),
                ("=", OPERATORS.EQUALS, KeyType.EQUALS),
            ],
        ]

        # 创建行
        rows = []
        for row_layout in layout:
            row_keys = []
            for display, key_value, key_type in row_layout:
                # 确定回调
                callback = self._get_callback(key_type)

                # 创建按键
                key = CalculatorKey(
                    content=display,
                    key_type=key_type,
                    on_click=callback,
                    enabled=self._is_key_enabled(key_value, key_type),
                )

                # 存储引用（用于后续更新状态）
                self._keys[key_value] = key
                row_keys.append(key)

            # 创建行容器
            row = ft.Row(
                controls=row_keys,
                spacing=SIZES.BUTTON_SPACING,
            )
            rows.append(row)

        # 设置内容
        self.content = ft.Column(
            controls=rows,
            spacing=SIZES.BUTTON_SPACING,
        )

    def _get_callback(self, key_type: KeyType) -> Optional[Callable[[str], None]]:
        """根据按键类型获取回调函数"""
        if key_type == KeyType.DIGIT or key_type == KeyType.HEX_DIGIT:
            return self._on_key_press
        elif key_type == KeyType.OPERATOR:
            return self._on_operator_press
        elif key_type in (KeyType.FUNCTION, KeyType.PAREN, KeyType.SHIFT, KeyType.EQUALS):
            return self._on_function_press
        return None

    def _is_key_enabled(self, key_value: str, key_type: KeyType) -> bool:
        """判断按键是否应该启用"""
        # 十六进制键根据模式决定是否启用
        if key_type == KeyType.HEX_DIGIT:
            return self._hex_enabled
        return True

    def set_hex_enabled(self, enabled: bool) -> None:
        """
        设置十六进制键是否启用

        Args:
            enabled: 是否启用
        """
        self._hex_enabled = enabled

        # 更新A-F键状态
        hex_keys = ["A", "B", "C", "D", "E", "F"]
        for key in hex_keys:
            if key in self._keys:
                self._keys[key].set_enabled(enabled)

    def set_key_enabled(self, key_value: str, enabled: bool) -> None:
        """
        设置特定按键的启用状态

        Args:
            key_value: 按键值
            enabled: 是否启用
        """
        if key_value in self._keys:
            self._keys[key_value].set_enabled(enabled)

    def press_key(self, key_value: str) -> None:
        """
        模拟按键按下

        Args:
            key_value: 按键值
        """
        callback = self._get_callback(self._keys[key_value]._key_type)
        if callback:
            callback(key_value)