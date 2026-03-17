import unittest
from src.core.number_base import NumberBase, NumberBaseConverter


class TestNumberBase(unittest.TestCase):
    """进制转换模块测试"""
    
    def test_number_base_enum_values(self):
        """测试NumberBase枚举值正确性"""
        self.assertEqual(NumberBase.HEX.value, 16)
        self.assertEqual(NumberBase.DEC.value, 10)
        self.assertEqual(NumberBase.OCT.value, 8)
        self.assertEqual(NumberBase.BIN.value, 2)

    def test_converter_basic_conversion(self):
        """测试基本进制转换功能"""
        converter = NumberBaseConverter()
        
        # 十进制转十六进制
        self.assertEqual(converter.convert(255, NumberBase.DEC, NumberBase.HEX), 'FF')
        # 十六进制转十进制
        self.assertEqual(converter.convert(255, NumberBase.HEX, NumberBase.DEC), '255')
        # 十进制转八进制
        self.assertEqual(converter.convert(64, NumberBase.DEC, NumberBase.OCT), '100')
        # 十进制转二进制
        self.assertEqual(converter.convert(8, NumberBase.DEC, NumberBase.BIN), '1000')

    def test_converter_edge_cases(self):
        """测试边界条件"""
        converter = NumberBaseConverter()
        
        # 转换零值
        self.assertEqual(converter.convert(0, NumberBase.DEC, NumberBase.HEX), '0')
        self.assertEqual(converter.convert(0, NumberBase.DEC, NumberBase.OCT), '0')
        self.assertEqual(converter.convert(0, NumberBase.DEC, NumberBase.BIN), '0')
        self.assertEqual(converter.to_hex(0), '0')
        self.assertEqual(converter.to_dec(0), '0')
        self.assertEqual(converter.to_oct(0), '0')
        self.assertEqual(converter.to_bin(0), '0')

        # 测试最大64位整数值的一些场景
        big_number = 2**63 - 1
        result_hex = converter.to_hex(big_number)
        result_dec = converter.to_dec(big_number)
        result_bin = converter.to_bin(big_number)
        
        self.assertEqual(int(result_dec), big_number)
        self.assertEqual(int(converter.from_string(result_hex, NumberBase.HEX)), big_number)
        self.assertEqual(int(converter.from_string(result_bin, NumberBase.BIN)), big_number)

    def test_negative_numbers(self):
        """测试负数转换"""
        converter = NumberBaseConverter()
        
        # 使用十进制的负数进行测试
        negative_value = -255
        
        # 确保结果包含负号
        self.assertIn('-', converter.to_hex(negative_value))
        self.assertIn('-', converter.to_dec(negative_value))
        self.assertIn('-', converter.to_oct(negative_value))
        self.assertIn('-', converter.to_bin(negative_value))

    def test_to_hex_method(self):
        """测试十进制转十六进制方法"""
        converter = NumberBaseConverter()
        
        self.assertEqual(converter.to_hex(255), 'FF')
        self.assertEqual(converter.to_hex(10), 'A')
        self.assertEqual(converter.to_hex(16), '10')
        self.assertEqual(converter.to_hex(256), '100')
        self.assertEqual(converter.to_hex(1), '1')

    def test_to_dec_method(self):
        """测试十进制输出方法"""
        converter = NumberBaseConverter()
        
        self.assertEqual(converter.to_dec(42), '42')
        self.assertEqual(converter.to_dec(1000), '1000')
        self.assertEqual(converter.to_dec(0), '0')

    def test_to_oct_method(self):
        """测试十进制转八进制方法"""
        converter = NumberBaseConverter()
        
        self.assertEqual(converter.to_oct(8), '10')
        self.assertEqual(converter.to_oct(64), '100')
        self.assertEqual(converter.to_oct(100), '144')
        self.assertEqual(converter.to_oct(0), '0')

    def test_to_bin_method(self):
        """测试十进制转二进制方法"""
        converter = NumberBaseConverter()
        
        self.assertEqual(converter.to_bin(2), '10')
        self.assertEqual(converter.to_bin(8), '1000')
        self.assertEqual(converter.to_bin(15), '1111')
        self.assertEqual(converter.to_bin(16), '10000')

    def test_from_string_method(self):
        """测试从字符串解析的方法"""
        converter = NumberBaseConverter()
        
        self.assertEqual(converter.from_string('FF', NumberBase.HEX), 255)
        self.assertEqual(converter.from_string('100', NumberBase.DEC), 100)
        self.assertEqual(converter.from_string('100', NumberBase.OCT), 64)
        self.assertEqual(converter.from_string('100', NumberBase.BIN), 4)

    def test_from_string_invalid_input(self):
        """测试从字符串解析中的无效输入"""
        converter = NumberBaseConverter()
        
        # 测试非法数字字符在各种进制下
        with self.assertRaises(ValueError):
            converter.from_string('G', NumberBase.HEX)  # G不是有效十六进制字符
            
        with self.assertRaises(ValueError):
            converter.from_string('8', NumberBase.OCT)  # 在八进制中8是非法字符
            
        with self.assertRaises(ValueError):
            converter.from_string('2', NumberBase.BIN)  # 在二进制中2是非法字符

    def test_from_string_empty_and_whitespace(self):
        """测试空字符串和其他边界条件"""
        converter = NumberBaseConverter()
        
        with self.assertRaises(ValueError):
            converter.from_string('', NumberBase.DEC)

    def test_consistent_convert_and_helper_methods(self):
        """测试转换函数与助手方法的一致性"""
        converter = NumberBaseConverter()
        
        value = 255
        
        # 检查转换方法与专用方法是否返回相同结果
        self.assertEqual(converter.convert(value, NumberBase.DEC, NumberBase.HEX), 
                         converter.to_hex(value))
        self.assertEqual(converter.convert(value, NumberBase.DEC, NumberBase.OCT), 
                         converter.to_oct(value))
        self.assertEqual(converter.convert(value, NumberBase.DEC, NumberBase.BIN), 
                         converter.to_bin(value))
        self.assertEqual(converter.convert(value, NumberBase.DEC, NumberBase.DEC), 
                         converter.to_dec(value))


if __name__ == '__main__':
    unittest.main()