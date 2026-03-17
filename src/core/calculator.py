# -*- coding: utf-8 -*-
"""
程序员计算器 - 核心计算器模块
提供计算器状态管理和运算功能
"""

from typing import Optional, Callable
from enum import Enum

from .number_base import NumberBase, NumberBaseConverter
from .bit_operations import BitMode, BitOperations
from .memory import Memory


class CalculatorState(str, Enum):
    """计算器状态枚举"""

    IDLE = "idle"           # 空闲状态
    INPUTTING = "inputting"  # 输入中
    OPERATOR = "operator"    # 等待第二个操作数
    RESULT = "result"        # 显示结果
    ERROR = "error"          # 错误状态


class Calculator:
    """
    程序员计算器核心实现类

    管理计算器状态、进制转换、运算和存储功能
    """

    def __init__(self):
        """
        初始化计算器
        """
        # 核心组件
        self._converter = NumberBaseConverter()
        self._bit_ops = BitOperations()
        self._memory = Memory()

        # 状态
        self._state = CalculatorState.IDLE
        self._current_value = 0
        self._display_value = "0"
        self._current_base = NumberBase.DEC
        self._bit_mode = BitMode.QWORD

        # 运算状态
        self._pending_operator: Optional[str] = None
        self._previous_value: Optional[int] = None
        self._new_input = True

        # 回调
        self._on_display_change: Optional[Callable[[int], None]] = None

    # ==================== 属性访问 ====================

    @property
    def current_value(self) -> int:
        """获取当前值"""
        return self._current_value

    @property
    def display_value(self) -> str:
        """获取显示值"""
        return self._display_value

    @property
    def current_base(self) -> NumberBase:
        """获取当前进制"""
        return self._current_base

    @property
    def bit_mode(self) -> BitMode:
        """获取当前位模式"""
        return self._bit_mode

    @property
    def state(self) -> CalculatorState:
        """获取当前状态"""
        return self._state

    @property
    def memory(self) -> Memory:
        """获取存储对象"""
        return self._memory

    # ==================== 设置方法 ====================

    def set_base(self, base: NumberBase) -> None:
        """
        设置当前进制

        Args:
            base: 目标进制
        """
        if base != self._current_base:
            self._current_base = base
            self._update_display()

    def set_bit_mode(self, mode: BitMode) -> None:
        """
        设置位模式

        Args:
            mode: 目标位模式
        """
        self._bit_mode = mode

    def set_on_display_change(self, callback: Optional[Callable[[int], None]]) -> None:
        """
        设置显示变化回调

        Args:
            callback: 回调函数
        """
        self._on_display_change = callback

    # ==================== 输入处理 ====================

    def input_digit(self, digit: str) -> bool:
        """
        输入数字

        Args:
            digit: 数字字符

        Returns:
            输入是否有效
        """
        # 验证输入
        if not self._is_valid_digit(digit):
            return False

        # 处理新输入
        if self._new_input or self._state == CalculatorState.RESULT:
            self._display_value = digit
            self._new_input = False
            self._state = CalculatorState.INPUTTING
        else:
            # 追加数字
            if self._display_value == "0":
                self._display_value = digit
            else:
                self._display_value += digit

        # 更新当前值
        self._parse_and_update()
        return True

    def input_operator(self, operator: str) -> None:
        """
        输入运算符

        Args:
            operator: 运算符
        """
        # 如果有待处理的运算符，先计算
        if self._pending_operator and self._previous_value is not None:
            self._calculate()

        self._previous_value = self._current_value
        self._pending_operator = operator
        self._new_input = True
        self._state = CalculatorState.OPERATOR

    def input_equals(self) -> None:
        """输入等号，计算结果"""
        if self._pending_operator and self._previous_value is not None:
            self._calculate()
            self._pending_operator = None
            self._previous_value = None
            self._new_input = True
            self._state = CalculatorState.RESULT

    def clear(self) -> None:
        """清除所有状态"""
        self._current_value = 0
        self._display_value = "0"
        self._pending_operator = None
        self._previous_value = None
        self._new_input = True
        self._state = CalculatorState.IDLE
        self._notify_display_change()

    def clear_entry(self) -> None:
        """清除当前输入"""
        self._display_value = "0"
        self._current_value = 0
        self._new_input = True
        self._notify_display_change()

    def backspace(self) -> None:
        """删除最后一位"""
        if self._state == CalculatorState.RESULT:
            return

        if len(self._display_value) > 1:
            self._display_value = self._display_value[:-1]
        else:
            self._display_value = "0"

        self._parse_and_update()

    def toggle_sign(self) -> None:
        """切换正负号"""
        self._current_value = -self._current_value
        self._update_display()

    def calculate_percent(self) -> None:
        """计算百分比"""
        self._current_value = self._current_value // 100
        self._update_display()

    # ==================== 位运算 ====================

    def bit_and(self) -> None:
        """按位与运算"""
        self.input_operator("AND")

    def bit_or(self) -> None:
        """按位或运算"""
        self.input_operator("OR")

    def bit_xor(self) -> None:
        """按位异或运算"""
        self.input_operator("XOR")

    def bit_not(self) -> None:
        """按位取反"""
        self._current_value = self._bit_ops.not_op(self._current_value, self._bit_mode)
        self._update_display()
        self._state = CalculatorState.RESULT

    def left_shift(self, bits: int) -> None:
        """
        左移运算

        Args:
            bits: 移位位数
        """
        self._current_value = self._bit_ops.left_shift(
            self._current_value, bits, self._bit_mode
        )
        self._update_display()
        self._state = CalculatorState.RESULT

    def right_shift(self, bits: int) -> None:
        """
        右移运算

        Args:
            bits: 移位位数
        """
        self._current_value = self._bit_ops.right_shift(
            self._current_value, bits, self._bit_mode
        )
        self._update_display()
        self._state = CalculatorState.RESULT

    def rotate_left(self, bits: int) -> None:
        """
        循环左移

        Args:
            bits: 移位位数
        """
        self._current_value = self._bit_ops.rotate_left(
            self._current_value, bits, self._bit_mode
        )
        self._update_display()
        self._state = CalculatorState.RESULT

    def rotate_right(self, bits: int) -> None:
        """
        循环右移

        Args:
            bits: 移位位数
        """
        self._current_value = self._bit_ops.rotate_right(
            self._current_value, bits, self._bit_mode
        )
        self._update_display()
        self._state = CalculatorState.RESULT

    def toggle_bit(self, position: int) -> None:
        """
        切换特定位

        Args:
            position: 位位置
        """
        self._current_value = self._bit_ops.toggle_bit(self._current_value, position)
        self._update_display()

    # ==================== 内部方法 ====================

    def _is_valid_digit(self, digit: str) -> bool:
        """
        检查数字是否在当前进制下有效

        Args:
            digit: 数字字符

        Returns:
            是否有效
        """
        valid_chars = {
            NumberBase.HEX: "0123456789ABCDEF",
            NumberBase.DEC: "0123456789",
            NumberBase.OCT: "01234567",
            NumberBase.BIN: "01",
        }
        return digit.upper() in valid_chars.get(self._current_base, "")

    def _parse_and_update(self) -> None:
        """解析显示值并更新当前值"""
        try:
            self._current_value = self._converter.from_string(
                self._display_value, self._current_base
            )
            self._notify_display_change()
        except ValueError:
            self._state = CalculatorState.ERROR

    def _update_display(self) -> None:
        """更新显示值"""
        self._display_value = self._converter.to_base(
            self._current_value, self._current_base
        )
        self._notify_display_change()

    def _calculate(self) -> None:
        """执行计算"""
        if self._previous_value is None:
            return

        try:
            a = self._previous_value
            b = self._current_value

            if self._pending_operator == "+":
                result = a + b
            elif self._pending_operator == "-":
                result = a - b
            elif self._pending_operator == "×" or self._pending_operator == "*":
                result = a * b
            elif self._pending_operator == "÷" or self._pending_operator == "/":
                if b == 0:
                    self._state = CalculatorState.ERROR
                    self._display_value = "Error"
                    return
                result = a // b
            elif self._pending_operator == "AND":
                result = self._bit_ops.and_op(a, b, self._bit_mode)
            elif self._pending_operator == "OR":
                result = self._bit_ops.or_op(a, b, self._bit_mode)
            elif self._pending_operator == "XOR":
                result = self._bit_ops.xor(a, b, self._bit_mode)
            else:
                result = b

            self._current_value = result
            self._update_display()
            self._state = CalculatorState.RESULT

        except Exception:
            self._state = CalculatorState.ERROR
            self._display_value = "Error"

    def _notify_display_change(self) -> None:
        """通知显示变化"""
        if self._on_display_change:
            self._on_display_change(self._current_value)

    # ==================== 便捷方法 ====================

    def get_display_for_base(self, base: NumberBase) -> str:
        """
        获取指定进制的显示值

        Args:
            base: 目标进制

        Returns:
            格式化后的字符串
        """
        return self._converter.to_base(self._current_value, base)

    def get_binary_display(self) -> str:
        """获取二进制显示值"""
        return self._converter.to_bin(self._current_value)

    def is_hex_digit_enabled(self, digit: str) -> bool:
        """
        检查十六进制数字键是否应该启用

        Args:
            digit: 数字字符

        Returns:
            是否启用
        """
        # 只有在十六进制模式下才启用A-F
        if self._current_base == NumberBase.HEX:
            return True
        # 其他模式下，只有0-9可能启用
        return digit.upper() not in "ABCDEF"