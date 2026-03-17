# -*- coding: utf-8 -*-
"""
程序员计算器 - 主应用组件
整合所有UI组件，提供完整的应用功能
"""

import flet as ft
from typing import Optional
from enum import Enum

from src.core.calculator import Calculator
from src.core.number_base import NumberBase, NumberBaseConverter
from src.core.bit_operations import BitMode, BitOperations
from src.core.memory import Memory
from src.ui.display import DisplayPanel, BaseMode
from src.ui.binary_panel import BinaryPanel
from src.ui.keypad import Keypad, KeyType
from src.ui.theme import apply_dark_theme
from src.utils.constants import COLORS, SIZES, BIT_MODES, OPERATORS


class ProgrammerCalculatorApp:
    """
    程序员计算器主应用

    整合所有组件，提供完整的计算器功能
    """

    def __init__(self, page: ft.Page):
        """
        初始化应用

        Args:
            page: Flet页面对象
        """
        self.page = page
        self._setup_page()

        # 初始化核心组件
        self._calculator = Calculator()
        self._memory = Memory()
        self._converter = NumberBaseConverter()
        self._bit_operations = BitOperations()

        # 当前状态
        self._current_base = NumberBase.DEC
        self._bit_mode = BitMode.QWORD
        self._current_display = "0"
        self._pending_operator: Optional[str] = None
        self._previous_value: Optional[int] = None
        self._new_input = True

        # UI组件
        self._display_panel: Optional[DisplayPanel] = None
        self._binary_panel: Optional[BinaryPanel] = None
        self._keypad: Optional[Keypad] = None
        self._bit_mode_dropdown: Optional[ft.Dropdown] = None
        self._memory_buttons: dict = {}

    def _setup_page(self) -> None:
        """设置页面基本属性"""
        self.page.title = "程序员计算器"
        self.page.window.width = SIZES.WINDOW_WIDTH
        self.page.window.height = SIZES.WINDOW_HEIGHT
        self.page.window.min_width = SIZES.MIN_WINDOW_WIDTH
        self.page.window.min_height = SIZES.MIN_WINDOW_HEIGHT
        self.page.padding = 0

        # 应用深色主题
        apply_dark_theme(self.page)

    def run(self) -> None:
        """运行应用"""
        self._build_ui()
        self._setup_keyboard_handlers()

    def _build_ui(self) -> None:
        """构建用户界面"""
        # 标题栏
        title_bar = self._build_title_bar()

        # 进制显示面板
        self._display_panel = DisplayPanel(
            on_base_change=self._handle_base_change
        )

        # 功能工具栏
        toolbar = self._build_toolbar()

        # 二进制位显示面板
        self._binary_panel = BinaryPanel(
            bit_mode=BIT_MODES.QWORD,
            on_bit_toggle=self._handle_bit_toggle,
        )

        # 数字键盘
        self._keypad = Keypad(
            on_key_press=self._handle_key_press,
            on_operator_press=self._handle_operator_press,
            on_function_press=self._handle_function_press,
            hex_enabled=True,
        )

        # 组装主界面
        self.page.add(
            ft.Column(
                controls=[
                    title_bar,
                    # 显示区域
                    ft.Container(
                        content=self._display_panel,
                        padding=ft.padding.symmetric(horizontal=SIZES.PADDING_SMALL),
                    ),
                    # 工具栏
                    ft.Container(
                        content=toolbar,
                        padding=ft.padding.symmetric(horizontal=SIZES.PADDING_SMALL),
                    ),
                    # 二进制面板
                    ft.Container(
                        content=self._binary_panel,
                        padding=ft.padding.symmetric(horizontal=SIZES.PADDING_SMALL),
                    ),
                    # 键盘
                    ft.Container(
                        content=self._keypad,
                        padding=ft.padding.all(0),
                        expand=True,
                    ),
                ],
                spacing=SIZES.PADDING_SMALL,
                expand=True,
            )
        )

    def _build_title_bar(self) -> ft.Container:
        """
        构建标题栏

        Returns:
            标题栏容器
        """
        return ft.Container(
            content=ft.Row(
                controls=[
                    # 菜单按钮
                    ft.IconButton(
                        icon=ft.Icons.MENU,
                        icon_color=COLORS.TEXT_SECONDARY,
                        on_click=self._handle_menu_click,
                    ),
                    # 标题
                    ft.Text(
                        value="Programmer",
                        size=16,
                        color=COLORS.TEXT_PRIMARY,
                    ),
                ],
                alignment=ft.MainAxisAlignment.START,
            ),
            padding=ft.padding.only(left=8, right=8, top=8, bottom=4),
        )

    def _build_toolbar(self) -> ft.Row:
        """
        构建功能工具栏

        Returns:
            工具栏行
        """
        # 位模式下拉框
        self._bit_mode_dropdown = ft.Dropdown(
            value="QWORD",
            options=[
                ft.dropdown.Option("QWORD"),
                ft.dropdown.Option("DWORD"),
                ft.dropdown.Option("WORD"),
                ft.dropdown.Option("BYTE"),
            ],
            width=100,
            text_size=12,
            on_change=self._handle_bit_mode_change,
        )

        # 存储按钮
        self._memory_buttons = {
            "MS": ft.TextButton(
                text="MS",
                style=ft.ButtonStyle(
                    color=COLORS.TEXT_SECONDARY,
                ),
                on_click=lambda e: self._handle_memory_action("MS"),
            ),
            "MR": ft.TextButton(
                text="MR",
                style=ft.ButtonStyle(
                    color=COLORS.TEXT_SECONDARY,
                ),
                on_click=lambda e: self._handle_memory_action("MR"),
            ),
            "MC": ft.TextButton(
                text="MC",
                style=ft.ButtonStyle(
                    color=COLORS.TEXT_SECONDARY,
                ),
                on_click=lambda e: self._handle_memory_action("MC"),
            ),
            "M+": ft.TextButton(
                text="M+",
                style=ft.ButtonStyle(
                    color=COLORS.TEXT_SECONDARY,
                ),
                on_click=lambda e: self._handle_memory_action("M+"),
            ),
        }

        return ft.Row(
            controls=[
                # 位模式选择
                self._bit_mode_dropdown,
                ft.VerticalDivider(width=1, color=COLORS.BUTTON_BG),
                # 存储功能
                self._memory_buttons["MS"],
                self._memory_buttons["MR"],
                self._memory_buttons["MC"],
                self._memory_buttons["M+"],
            ],
            alignment=ft.MainAxisAlignment.START,
            spacing=4,
        )

    def _setup_keyboard_handlers(self) -> None:
        """设置键盘事件处理"""
        self.page.on_keyboard_event = self._handle_keyboard_event

    def _handle_keyboard_event(self, e: ft.KeyboardEvent) -> None:
        """
        处理键盘事件

        Args:
            e: 键盘事件对象
        """
        key = e.key

        # 数字键
        if key in "0123456789ABCDEF":
            self._handle_key_press(key)

        # 运算符
        elif key == "+":
            self._handle_operator_press(OPERATORS.ADD)
        elif key == "-":
            self._handle_operator_press(OPERATORS.SUBTRACT)
        elif key == "*":
            self._handle_operator_press(OPERATORS.MULTIPLY)
        elif key == "/":
            self._handle_operator_press(OPERATORS.DIVIDE)

        # 功能键
        elif key == "Enter" or key == "=":
            self._handle_function_press(OPERATORS.EQUALS)
        elif key == "Escape":
            self._handle_function_press(OPERATORS.CLEAR)
        elif key == "Backspace":
            self._handle_function_press(OPERATORS.BACKSPACE)

    def _handle_key_press(self, key: str) -> None:
        """
        处理数字键按下

        Args:
            key: 按键值
        """
        # 检查当前进制是否允许该输入
        if not self._is_valid_input(key):
            return

        # 新输入时重置显示
        if self._new_input:
            self._current_display = key
            self._new_input = False
        else:
            # 追加输入
            if self._current_display == "0":
                self._current_display = key
            else:
                self._current_display += key

        # 更新显示
        self._update_display()

    def _handle_operator_press(self, operator: str) -> None:
        """
        处理运算符按下

        Args:
            operator: 运算符
        """
        current_value = self._parse_display_value()

        if self._pending_operator and self._previous_value is not None:
            # 执行待处理的运算
            result = self._calculate(self._previous_value, current_value, self._pending_operator)
            self._current_display = self._format_value(result)
            self._update_display()
            current_value = result

        self._previous_value = current_value
        self._pending_operator = operator
        self._new_input = True

    def _handle_function_press(self, function: str) -> None:
        """
        处理功能键按下

        Args:
            function: 功能键值
        """
        if function == OPERATORS.CLEAR:
            self._clear_all()
        elif function == OPERATORS.BACKSPACE:
            self._backspace()
        elif function == OPERATORS.EQUALS:
            self._calculate_result()
        elif function == OPERATORS.SIGN_TOGGLE:
            self._toggle_sign()
        elif function == OPERATORS.PERCENT:
            self._calculate_percent()

    def _handle_base_change(self, base: BaseMode) -> None:
        """
        处理进制切换

        Args:
            base: 新的进制模式
        """
        base_map = {
            BaseMode.HEX: NumberBase.HEX,
            BaseMode.DEC: NumberBase.DEC,
            BaseMode.OCT: NumberBase.OCT,
            BaseMode.BIN: NumberBase.BIN,
        }
        self._current_base = base_map[base]

        # 更新十六进制键启用状态
        hex_enabled = (self._current_base == NumberBase.HEX)
        if self._keypad:
            self._keypad.set_hex_enabled(hex_enabled)

    def _handle_bit_toggle(self, position: int) -> None:
        """
        处理二进制位切换

        Args:
            position: 位位置
        """
        current = self._parse_display_value()
        new_value = self._bit_operations.toggle_bit(current, position)
        self._current_display = self._format_value(new_value)
        self._update_display()

    def _handle_bit_mode_change(self, e) -> None:
        """处理位模式切换"""
        mode_map = {
            "QWORD": BitMode.QWORD,
            "DWORD": BitMode.DWORD,
            "WORD": BitMode.WORD,
            "BYTE": BitMode.BYTE,
        }
        mode_name = e.control.value
        self._bit_mode = mode_map.get(mode_name, BitMode.QWORD)

        if self._binary_panel:
            mode_value = {
                BitMode.QWORD: BIT_MODES.QWORD,
                BitMode.DWORD: BIT_MODES.DWORD,
                BitMode.WORD: BIT_MODES.WORD,
                BitMode.BYTE: BIT_MODES.BYTE,
            }.get(self._bit_mode, BIT_MODES.QWORD)
            self._binary_panel.set_bit_mode(mode_value)

    def _handle_memory_action(self, action: str) -> None:
        """
        处理存储操作

        Args:
            action: 操作类型 (MS/MR/MC/M+)
        """
        if action == "MS":
            self._memory.store(self._parse_display_value())
        elif action == "MR":
            if self._memory.has_value():
                self._current_display = self._format_value(self._memory.recall())
                self._update_display()
        elif action == "MC":
            self._memory.clear()
        elif action == "M+":
            if self._memory.has_value():
                self._memory.add(self._parse_display_value())

    def _handle_menu_click(self, e) -> None:
        """处理菜单点击"""
        # TODO: 实现菜单功能
        pass

    def _is_valid_input(self, key: str) -> bool:
        """
        检查输入是否在当前进制下有效

        Args:
            key: 输入的字符

        Returns:
            是否有效
        """
        if self._current_base == NumberBase.HEX:
            return key.upper() in "0123456789ABCDEF"
        elif self._current_base == NumberBase.DEC:
            return key in "0123456789"
        elif self._current_base == NumberBase.OCT:
            return key in "01234567"
        elif self._current_base == NumberBase.BIN:
            return key in "01"
        return False

    def _parse_display_value(self) -> int:
        """
        解析当前显示值为整数

        Returns:
            整数值
        """
        try:
            return self._converter.from_string(self._current_display, self._current_base)
        except ValueError:
            return 0

    def _format_value(self, value: int) -> str:
        """
        格式化整数值为当前进制字符串

        Args:
            value: 整数值

        Returns:
            格式化后的字符串
        """
        return self._converter.convert(value, NumberBase.DEC, self._current_base)

    def _calculate(self, a: int, b: int, operator: str) -> int:
        """
        执行计算

        Args:
            a: 第一个操作数
            b: 第二个操作数
            operator: 运算符

        Returns:
            计算结果
        """
        if operator == OPERATORS.ADD:
            return a + b
        elif operator == OPERATORS.SUBTRACT:
            return a - b
        elif operator == OPERATORS.MULTIPLY:
            return a * b
        elif operator == OPERATORS.DIVIDE:
            if b == 0:
                return 0  # 除零返回0
            return a // b
        return b

    def _update_display(self) -> None:
        """更新所有显示组件"""
        value = self._parse_display_value()

        # 更新进制显示面板
        if self._display_panel:
            self._display_panel.set_value(value)

        # 更新二进制面板
        if self._binary_panel:
            self._binary_panel.set_value(value)

    def _clear_all(self) -> None:
        """清除所有状态"""
        self._current_display = "0"
        self._pending_operator = None
        self._previous_value = None
        self._new_input = True
        self._update_display()

    def _backspace(self) -> None:
        """删除最后一位"""
        if len(self._current_display) > 1:
            self._current_display = self._current_display[:-1]
        else:
            self._current_display = "0"
        self._update_display()

    def _calculate_result(self) -> None:
        """计算最终结果"""
        if self._pending_operator and self._previous_value is not None:
            current_value = self._parse_display_value()
            result = self._calculate(self._previous_value, current_value, self._pending_operator)
            self._current_display = self._format_value(result)
            self._pending_operator = None
            self._previous_value = None
            self._new_input = True
            self._update_display()

    def _toggle_sign(self) -> None:
        """切换正负号"""
        value = self._parse_display_value()
        value = -value
        self._current_display = self._format_value(value)
        self._update_display()

    def _calculate_percent(self) -> None:
        """计算百分比"""
        value = self._parse_display_value()
        value = value // 100
        self._current_display = self._format_value(value)
        self._update_display()