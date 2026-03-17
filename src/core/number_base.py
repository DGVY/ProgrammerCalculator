from enum import Enum
from typing import Union


class NumberBase(Enum):
    """
    数字进制枚举
    
    定义了常见的数字进制及其对应的基数
    """
    HEX = 16  # 十六进制
    DEC = 10  # 十进制
    OCT = 8   # 八进制
    BIN = 2   # 二进制


class NumberBaseConverter:
    """
    进制转换器类
    
    提供不同进制之间的转换功能，包括：
    - 基本转换方法（任意进制之间相互转换）
    - 专用于特定目标进制的辅助方法
    - 从字符串解析到数字的方法
    """
    
    def convert(self, value: int, from_base: NumberBase, to_base: NumberBase) -> str:
        """
        将数值从一个进制转换到另一个进制

        Args:
            value: 输入的整数值（作为指定from_base下的代表数值）
            from_base: 源进制
            to_base: 目标进制

        Returns:
            转换后的字符串表示
        """
        # 如果目标就是十进制，则直接转换为字符串返回
        if to_base == NumberBase.DEC:
            return str(value)
        
        # 获取对应进制的十进制值（实际上value已经是十进制了，所以这里应该是把value从指定base理解为十进制来处理）
        # 实际上，这里的接口设计可能有点误解，参数的value已经是十进制值，我们需要将其转换为目标进制
        # 正确做法是将十进制value转换为目标进制
        decimal_value = value  # 这里value实际上是十进制值
        return self._decimal_to_base(decimal_value, to_base.value)

    def _decimal_to_base(self, value: int, base: int) -> str:
        """
        将十进制数值转换为指定进制的字符串表示

        Args:
            value: 十进制数值
            base: 目标进制

        Returns:
            指定进制的字符串表示
        """
        # 处理负数情况
        if value < 0:
            sign = '-'
            value = abs(value)
        else:
            sign = ''
            
        # 特殊情况：如果值为0，返回'0'
        if value == 0:
            return '0'
        
        digits = "0123456789ABCDEF"
        result = ""
        
        while value > 0:
            remainder = value % base
            result = digits[remainder] + result
            value = value // base
            
        return sign + result

    def _is_valid_for_base(self, s: str, base: int) -> bool:
        """
        检查字符串是否为指定进制的有效表示
        
        Args:
            s: 要检查的字符串
            base: 进制基数
            
        Returns:
            字符串是否有效
        """
        if not s:
            return False
            
        # 移除可能的符号
        start_idx = 0
        if s[0] in ['-', '+']:
            if len(s) <= 1:
                return False
            start_idx = 1
            
        valid_chars = "0123456789ABCDEF"[:base]  # 有效字符集合
        
        for char in s[start_idx:]:
            if char.upper() not in valid_chars:
                return False
        
        return True

    def to_hex(self, value: int) -> str:
        """
        将十进制整数转换为十六进制字符串

        Args:
            value: 十进制数值

        Returns:
            十六进制大写字符串
        """
        return self._decimal_to_base(value, 16)

    def to_dec(self, value: int) -> str:
        """
        将十进制整数转换为十进制字符串(即其本身)

        Args:
            value: 十进制数值

        Returns:
            十进制字符串表示
        """
        return str(value)

    def to_oct(self, value: int) -> str:
        """
        将十进制整数转换为八进制字符串

        Args:
            value: 十进制数值

        Returns:
            八进制字符串表示
        """
        return self._decimal_to_base(value, 8)

    def to_bin(self, value: int) -> str:
        """
        将十进制整数转换为二进制字符串

        Args:
            value: 十进制数值

        Returns:
            二进制字符串表示，不带前缀
        """
        return self._decimal_to_base(value, 2)

    def to_base(self, value: int, base: NumberBase) -> str:
        """
        将十进制整数转换为指定进制的字符串

        Args:
            value: 十进制数值
            base: 目标进制

        Returns:
            指定进制的字符串表示
        """
        if base == NumberBase.HEX:
            return self.to_hex(value)
        elif base == NumberBase.DEC:
            return self.to_dec(value)
        elif base == NumberBase.OCT:
            return self.to_oct(value)
        elif base == NumberBase.BIN:
            return self.to_bin(value)
        return self._decimal_to_base(value, base.value)

    def from_string(self, value: str, base: NumberBase) -> int:
        """
        从指定进制的字符串中解析出十进制整数

        Args:
            value: 表示数字的字符串
            base: 字符串所用进制

        Returns:
            解析出的十进制整数

        Raises:
            ValueError: 当字符串格式无效时
        """
        if not self._is_valid_for_base(value, base.value):
            raise ValueError(f"Invalid number '{value}' for base {base.value}")
        
        return int(value, base.value)