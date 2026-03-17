import pytest
from src.core.bit_operations import BitMode, BitOperations


class TestBitOperations:
    """位运算模块的单元测试"""
    
    def setup_method(self):
        """每个测试方法运行前的初始化"""
        self.bit_ops = BitOperations()

    def test_bitmode_enum_values(self):
        """测试BitMode枚举值"""
        assert BitMode.BYTE.value == 8
        assert BitMode.WORD.value == 16
        assert BitMode.DWORD.value == 32
        assert BitMode.QWORD.value == 64

    def test_and_operation(self):
        """测试按位与操作"""
        # BYTE模式
        result = self.bit_ops.and_op(0xFF, 0xF0, BitMode.BYTE)
        assert result == 0xF0
        
        # DWORD模式
        result = self.bit_ops.and_op(0xFFFFFFFF, 0xFFFF0000, BitMode.DWORD)
        assert result == 0xFFFF0000
        
        # QWORD模式
        result = self.bit_ops.and_op(0xFFFFFFFFFFFFFFFF, 0xFFFFFFFF00000000, BitMode.QWORD)
        assert result == 0xFFFFFFFF00000000

    def test_or_operation(self):
        """测试按位或操作"""
        # BYTE模式
        result = self.bit_ops.or_op(0x0F, 0xF0, BitMode.BYTE)
        assert result == 0xFF
        
        # DWORD模式
        result = self.bit_ops.or_op(0xFFFF0000, 0x0000FFFF, BitMode.DWORD)
        assert result == 0xFFFFFFFF
        
        # QWORD模式
        result = self.bit_ops.or_op(0xFFFFFFFF00000000, 0x00000000FFFFFFFF, BitMode.QWORD)
        assert result == 0xFFFFFFFFFFFFFFFF

    def test_xor_operation(self):
        """测试按位异或操作"""
        # BYTE模式
        result = self.bit_ops.xor(0xFF, 0xF0, BitMode.BYTE)
        assert result == 0x0F
        
        # DWORD模式
        result = self.bit_ops.xor(0xFFFFFFFF, 0xFFFF0000, BitMode.DWORD)
        assert result == 0x0000FFFF
        
        # QWORD模式
        result = self.bit_ops.xor(0xFFFFFFFFFFFFFFFF, 0xFFFFFFFF00000000, BitMode.QWORD)
        assert result == 0x00000000FFFFFFFF

    def test_not_operation(self):
        """测试按位取反操作"""
        # BYTE模式
        result = self.bit_ops.not_op(0xF0, BitMode.BYTE)
        assert result == 0x0F
        
        # DWORD模式
        result = self.bit_ops.not_op(0xFFFF0000, BitMode.DWORD)
        assert result == 0x0000FFFF
        
        # QWORD模式
        result = self.bit_ops.not_op(0xFFFFFFFF00000000, BitMode.QWORD)
        assert result == 0x00000000FFFFFFFF

    def test_left_shift_operation(self):
        """测试左移操作"""
        # BYTE模式
        result = self.bit_ops.left_shift(0x01, 4, BitMode.BYTE)
        assert result == 0x10
        
        # DWORD模式
        result = self.bit_ops.left_shift(0x00000001, 16, BitMode.DWORD)
        assert result == 0x00010000
        
        # QWORD模式
        result = self.bit_ops.left_shift(0x0000000000000001, 32, BitMode.QWORD)
        assert result == 0x0000000100000000

    def test_right_shift_operation(self):
        """测试右移操作"""
        # BYTE模式
        result = self.bit_ops.right_shift(0x10, 4, BitMode.BYTE)
        assert result == 0x01
        
        # DWORD模式
        result = self.bit_ops.right_shift(0x00010000, 16, BitMode.DWORD)
        assert result == 0x00000001
        
        # QWORD模式
        result = self.bit_ops.right_shift(0x0000000100000000, 32, BitMode.QWORD)
        assert result == 0x0000000000000001

    def test_rotate_left_operation(self):
        """测试循环左移操作"""
        # BYTE模式下的简单旋转
        result = self.bit_ops.rotate_left(0b10000001, 1, BitMode.BYTE)
        assert result == 0b00000011  # 10000001 -> 00000011 (第一位转到末尾，但会被遮罩)
        
        # 真正的循环左移需要正确实现
        result = self.bit_ops.rotate_left(0b10000001, 1, BitMode.BYTE)
        expected = ((0b10000001 << 1) | (0b10000001 >> (8-1))) & 0xFF
        assert result == expected

    def test_rotate_right_operation(self):
        """测试循环右移操作"""
        # BYTE模式下的简单旋转
        result = self.bit_ops.rotate_right(0b10000001, 1, BitMode.BYTE)
        expected = ((0b10000001 >> 1) | (0b10000001 << (8-1)) & 0xFF)
        # 正确计算循环右移: 右移1位(01000000) | (首位放末尾)
        assert result == expected

    def test_get_bit_operation(self):
        """测试获取特定位操作"""
        value = 0b10101010  # 170

        assert self.bit_ops.get_bit(value, 0) == 0  # 最低位为0
        assert self.bit_ops.get_bit(value, 1) == 1  # 第1位为1
        assert self.bit_ops.get_bit(value, 2) == 0  # 第2位为0
        assert self.bit_ops.get_bit(value, 3) == 1  # 第3位为1
        assert self.bit_ops.get_bit(value, 7) == 1  # 最高位为1

    def test_set_bit_operation(self):
        """测试设置特定位为1操作"""
        value = 0b00000000
        
        # 设置第0位为1
        result = self.bit_ops.set_bit(value, 0)
        assert result == 0b00000001
        
        # 设置第7位为1
        result = self.bit_ops.set_bit(value, 7)
        assert result == 0b10000000
        
        # 对于已设置的位应该保持不变
        result = self.bit_ops.set_bit(0b10000001, 0)
        assert result == 0b10000001

    def test_clear_bit_operation(self):
        """测试清除特定位为0操作"""
        value = 0b11111111
        
        # 清除第0位
        result = self.bit_ops.clear_bit(value, 0)
        assert result == 0b11111110
        
        # 清除第7位
        result = self.bit_ops.clear_bit(value, 7)
        assert result == 0b01111111
        
        # 对于已清除的位应该保持不变
        result = self.bit_ops.clear_bit(0b11111110, 0)
        assert result == 0b11111110

    def test_toggle_bit_operation(self):
        """测试翻转特定位操作"""
        value = 0b00000000
        
        # 翻转第0位
        result = self.bit_ops.toggle_bit(value, 0)
        assert result == 0b00000001
        
        # 再次翻转第0位回到原状
        result = self.bit_ops.toggle_bit(result, 0)
        assert result == 0b00000000
        
        # 初始值1的情况
        value = 0b00000001
        result = self.bit_ops.toggle_bit(value, 0)
        assert result == 0b00000000

    def test_overflow_handling_byte(self):
        """测试BYTE模式下的溢出处理"""
        result = self.bit_ops.and_op(0xFF, 0xFF, BitMode.BYTE)
        assert result == 0xFF
        
        # 一个超出BYTE范围的数在BYTE模式下的处理
        result = self.bit_ops.not_op(0xFFFF, BitMode.BYTE)
        assert result == 0x00  # 0xFF ^ 0xFF = 0x00，实际应该是对0xFFFF按BYTE遮罩处理后取反
        
        # 更合适的测试：
        # 在字节模式下，我们应只考虑最低8位
        value = 0x123  # 0x123的低8位是0x23
        result = self.bit_ops.not_op(value, BitMode.BYTE)
        expected = (~value) & 0xFF  # 先取反再遮罩
        assert result == expected

    def test_overflow_handling_dword(self):
        """测试DWORD模式下的溢出处理"""
        result = self.bit_ops.not_op(0x12345678, BitMode.DWORD)
        expected = (~0x12345678) & 0xFFFFFFFF
        assert result == expected

    def test_overflow_handling_qword(self):
        """测试QWORD模式下的溢出处理"""
        result = self.bit_ops.not_op(0x1234567812345678, BitMode.QWORD)
        expected = (~0x1234567812345678) & 0xFFFFFFFFFFFFFFFF
        assert result == expected

    def test_edge_cases_zero_values(self):
        """测试零值边缘情况"""
        # 任何数与0进行AND操作应为0
        result = self.bit_ops.and_op(0xABCDE, 0, BitMode.DWORD)
        assert result == 0 
        
        # 任何数与全1进行AND操作应为自己
        result = self.bit_ops.and_op(0xABCD, 0xFFFF, BitMode.WORD)
        assert result == 0xABCD