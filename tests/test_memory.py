import pytest
from src.core.memory import Memory


class TestMemory:
    """存储模块单元测试"""
    
    def test_initial_state_is_empty(self):
        """测试初始状态为空"""
        memory = Memory()
        assert not memory.has_value()
        assert memory.get_value() is None
    
    def test_store_and_recall_value(self):
        """测试存储值和重新调用值"""
        memory = Memory()
        
        # 存储值
        memory.store(42)
        assert memory.has_value()
        assert memory.recall() == 42
        assert memory.get_value() == 42
    
    def test_clear_function(self):
        """测试清除功能"""
        memory = Memory()
        
        # 先存储一个值
        memory.store(100)
        assert memory.has_value()
        assert memory.recall() == 100
        
        # 清除存储
        memory.clear()
        assert not memory.has_value()
        assert memory.get_value() is None
        
    def test_add_function(self):
        """测试累加功能"""
        memory = Memory()
        
        # 初始存储一个值
        memory.store(10)
        assert memory.recall() == 10
        
        # 累加
        memory.add(5)
        assert memory.recall() == 15
        
        # 继续累加负数
        memory.add(-3)
        assert memory.recall() == 12
    
    def test_subtract_function(self):
        """测试减法功能"""
        memory = Memory()
        
        # 初始存储一个值
        memory.store(20)
        assert memory.recall() == 20
        
        # 减法操作
        memory.subtract(5)
        assert memory.recall() == 15
        
        # 减去负数（相当于加法）
        memory.subtract(-10)
        assert memory.recall() == 25
    
    def test_operations_on_empty_memory(self):
        """测试对空存储的操作"""
        memory = Memory()
        
        # 对空存储进行运算应抛出异常
        with pytest.raises(ValueError):
            memory.recall()
            
        with pytest.raises(ValueError):
            memory.add(10)
            
        with pytest.raises(ValueError):
            memory.subtract(5)
    
    def test_store_after_operation(self):
        """测试存储覆盖功能"""
        memory = Memory()
        
        memory.store(10)
        assert memory.recall() == 10
        
        # 覆盖之前存储的值
        memory.store(99)
        assert memory.recall() == 99
        
    def test_boundary_values(self):
        """测试64位边界值处理"""
        memory = Memory()
        
        # 测试最小值
        min_val = -(2**63)
        memory.store(min_val)
        assert memory.recall() == min_val
        
        # 测试最大值
        max_val = 2**63 - 1
        memory.store(max_val)
        assert memory.recall() == max_val
        
        # 测试0
        memory.store(0)
        assert memory.recall() == 0
    
    def test_multiple_operations(self):
        """测试多项连续操作"""
        memory = Memory()
        
        # 存储初始值
        memory.store(50)
        assert memory.recall() == 50
        
        # 多次操作
        memory.add(10)      # 50 + 10 = 60
        assert memory.recall() == 60
        
        memory.subtract(20) # 60 - 20 = 40
        assert memory.recall() == 40
        
        memory.add(6)       # 40 + 6 = 46
        assert memory.recall() == 46
        
        memory.clear()
        assert not memory.has_value()
        
        # 验证清空后的状态
        memory.store(2333)
        assert memory.recall() == 2333


if __name__ == "__main__":
    pytest.main([__file__, "-v"])