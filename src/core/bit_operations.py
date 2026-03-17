"""
位运算模块
提供各种位运算操作，支持不同数据类型的位宽约束。
"""

from enum import Enum
from typing import Union


class BitMode(Enum):
    """位宽模式枚举"""
    QWORD = 64  # 64位模式
    DWORD = 32  # 32位模式
    WORD = 16   # 16位模式
    BYTE = 8    # 8位模式


class BitOperations:
    """位运算操作类"""
    
    def __init__(self):
        """初始化位运算类"""
        # 预定义掩码以提高性能
        self.mask_map = {
            BitMode.BYTE: (1 << 8) - 1,
            BitMode.WORD: (1 << 16) - 1,
            BitMode.DWORD: (1 << 32) - 1,
            BitMode.QWORD: (1 << 64) - 1,
        }

    def _apply_mask(self, value: int, mode: BitMode) -> int:
        """
        根据指定模式应用位掩码，确保结果不超过模式指定的位宽
        
        Args:
            value: 输入数值
            mode: 位宽模式
            
        Returns:
            应用掩码后的数值
        """
        return value & self.mask_map[mode]

    def _normalize_for_mode(self, value: int, mode: BitMode) -> int:
        """
        将输入值根据指定模式标准化（截断为对应位宽内的值）
        
        Args:
            value: 输入数值
            mode: 位宽模式
            
        Returns:
            标准化后的数值
        """
        mask = self.mask_map[mode]
        return value & mask

    def and_op(self, a: int, b: int, mode: BitMode) -> int:
        """
        按位与运算
        
        Args:
            a: 第一个操作数
            b: 第二个操作数
            mode: 位宽模式
            
        Returns:
            按位与运算结果
        """
        a = self._normalize_for_mode(a, mode)
        b = self._normalize_for_mode(b, mode)
        return self._apply_mask(a & b, mode)

    def or_op(self, a: int, b: int, mode: BitMode) -> int:
        """
        按位或运算
        
        Args:
            a: 第一个操作数
            b: 第二个操作数
            mode: 位宽模式
            
        Returns:
            按位或运算结果
        """
        a = self._normalize_for_mode(a, mode)
        b = self._normalize_for_mode(b, mode)
        return self._apply_mask(a | b, mode)

    def xor(self, a: int, b: int, mode: BitMode) -> int:
        """
        按位异或运算
        
        Args:
            a: 第一个操作数
            b: 第二个操作数
            mode: 位宽模式
            
        Returns:
            按位异或运算结果
        """
        a = self._normalize_for_mode(a, mode)
        b = self._normalize_for_mode(b, mode)
        return self._apply_mask(a ^ b, mode)

    def not_op(self, value: int, mode: BitMode) -> int:
        """
        按位取反运算
        
        Args:
            value: 操作数
            mode: 位宽模式
            
        Returns:
            按位取反运算结果
        """
        normalized_value = self._normalize_for_mode(value, mode)
        inverted_value = (~normalized_value) & self.mask_map[mode]
        return inverted_value

    def left_shift(self, value: int, bits: int, mode: BitMode) -> int:
        """
        逻辑左移运算（忽略符号位）
        
        Args:
            value: 操作数
            bits: 移位位数
            mode: 位宽模式
            
        Returns:
            左移运算结果
        """
        normalized_value = self._normalize_for_mode(value, mode)
        # 防止过度移位导致无效结果
        bit_width = mode.value
        effective_bits = bits % bit_width if bit_width > 0 else bits
        shifted_value = (normalized_value << effective_bits)
        return self._apply_mask(shifted_value, mode)

    def right_shift(self, value: int, bits: int, mode: BitMode) -> int:
        """
        逻辑右移运算（忽略符号位）
        
        Args:
            value: 操作数
            bits: 移位位数
            mode: 位宽模式
            
        Returns:
            右移运算结果
        """
        normalized_value = self._normalize_for_mode(value, mode)
        # 防止过度移位导致无效结果
        bit_width = mode.value
        effective_bits = bits % bit_width if bit_width > 0 else bits
        shifted_value = normalized_value >> effective_bits
        return self._apply_mask(shifted_value, mode)

    def rotate_left(self, value: int, bits: int, mode: BitMode) -> int:
        """
        循环左移运算
        
        Args:
            value: 操作数
            bits: 移位位数
            mode: 位宽模式
            
        Returns:
            循环左移运算结果
        """
        normalized_value = self._normalize_for_mode(value, mode)
        bit_width = mode.value
        # 处理负数的移位量
        effective_bits = bits % bit_width if bit_width > 0 else 0
        
        if effective_bits == 0:
            return normalized_value

        # 循环左移：(value << bits) | (value >> (width - bits))
        left_part = (normalized_value << effective_bits) & self.mask_map[mode]
        right_part = normalized_value >> (bit_width - effective_bits)
        result = left_part | right_part
        return self._apply_mask(result, mode)

    def rotate_right(self, value: int, bits: int, mode: BitMode) -> int:
        """
        循环右移运算
        
        Args:
            value: 操作数
            bits: 移位位数
            mode: 位宽模式
            
        Returns:
            循环右移运算结果
        """
        normalized_value = self._normalize_for_mode(value, mode)
        bit_width = mode.value
        # 处理负数的移位量
        effective_bits = bits % bit_width if bit_width > 0 else 0
        
        if effective_bits == 0:
            return normalized_value

        # 循环右移：(value >> bits) | (value << (width - bits))
        right_part = normalized_value >> effective_bits
        left_part = (normalized_value << (bit_width - effective_bits)) & self.mask_map[mode]
        result = left_part | right_part
        return self._apply_mask(result, mode)

    def get_bit(self, value: int, position: int) -> int:
        """
        获取指定位置的位值
        
        Args:
            value: 操作数
            position: 位位置（从0开始）
            
        Returns:
            指定位置的位值（0或1）
        """
        if position < 0:
            raise ValueError("位位置不能为负数")
        return (value >> position) & 1

    def set_bit(self, value: int, position: int) -> int:
        """
        将指定位置的位设置为1
        
        Args:
            value: 操作数
            position: 位位置（从0开始）
            
        Returns:
            设置后的数值
        """
        if position < 0:
            raise ValueError("位位置不能为负数")
        return value | (1 << position)

    def clear_bit(self, value: int, position: int) -> int:
        """
        将指定位置的位清除为0
        
        Args:
            value: 操作数
            position: 位位置（从0开始）
            
        Returns:
            清除后的数值
        """
        if position < 0:
            raise ValueError("位位置不能为负数")
        return value & ~(1 << position)

    def toggle_bit(self, value: int, position: int) -> int:
        """
        翻转指定位置的位
        
        Args:
            value: 操作数
            position: 位位置（从0开始）
            
        Returns:
            翻转后的数值
        """
        if position < 0:
            raise ValueError("位位置不能为负数")
        return value ^ (1 << position)