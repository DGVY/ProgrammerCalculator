"""存储模块 - 实现内存存储功能，支持存储、读取、累加等操作"""


from typing import Optional


class Memory:
    """内存存储器类，模拟计算器的记忆功能
    
    提供类似Windows计算器的功能：
    - MS (Memory Store): 存储当前值
    - MR (Memory Recall): 读取存储值
    - MC (Memory Clear): 清除存储
    - M+ (Memory Plus): 累加到存储
    - M- (Memory Minus): 从存储减去
    """
    
    def __init__(self):
        """初始化存储器，初始值为None表示没有任何存储值"""
        self._value: Optional[int] = None
    
    def store(self, value: int) -> None:
        """存储指定值到内存中 (MS - Memory Store)
        
        Args:
            value: 要存储的整数值
        """
        self._value = value
    
    def recall(self) -> int:
        """从内存中读取存储值 (MR - Memory Recall)
        
        Returns:
            存储的整数值
            
        Raises:
            ValueError: 当内存中没有任何值时抛出异常
        """
        if self._value is None:
            raise ValueError("内存中没有存储任何值，请先存储一个值")
        return self._value
    
    def clear(self) -> None:
        """清除内存中的值 (MC - Memory Clear)"""
        self._value = None
    
    def add(self, value: int) -> None:
        """将指定值加到存储值上 (M+ - Memory Plus)
        
        Args:
            value: 要累加到存储中的整数值
            
        Raises:
            ValueError: 当内存中没有任何值时抛出异常
        """
        if self._value is None:
            raise ValueError("内存中没有存储任何值，请先存储一个值才能执行加法操作")
        self._value += value
    
    def subtract(self, value: int) -> None:
        """从存储值中减去指定值 (M- - Memory Minus)
        
        Args:
            value: 要从存储中减去的整数值
            
        Raises:
            ValueError: 当内存中没有任何值时抛出异常
        """
        if self._value is None:
            raise ValueError("内存中没有存储任何值，请先存储一个值才能执行减法操作")
        self._value -= value
    
    def has_value(self) -> bool:
        """检查内存中是否存储了值
        
        Returns:
            如果内存中有值则返回True，否则返回False
        """
        return self._value is not None
    
    def get_value(self) -> Optional[int]:
        """获取内存中的值（可能为None）
        
        Returns:
            内存中的值，如果没有值则返回None
        """
        return self._value