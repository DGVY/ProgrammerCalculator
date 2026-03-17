# -*- coding: utf-8 -*-
"""
程序员计算器 - 二进制位显示面板
显示64位二进制数值，支持点击切换特定位
"""

import flet as ft
from typing import Callable, Optional, List

from src.utils.constants import COLORS, SIZES, BIT_MODES


class BinaryBit(ft.Container):
    """
    单个二进制位控件

    显示0或1，支持点击切换
    """

    def __init__(
        self,
        position: int,
        value: int = 0,
        on_toggle: Optional[Callable[[int], None]] = None,
        **kwargs,
    ):
        """
        初始化二进制位

        Args:
            position: 位位置（从右到左，0-63）
            value: 当前值（0或1）
            on_toggle: 切换回调函数
        """
        super().__init__(**kwargs)

        self.position = position
        self._value = value
        self._on_toggle = on_toggle

        # 设置样式
        self.width = 20
        self.height = 24
        self.border_radius = 2
        self.alignment = ft.alignment.center
        self.on_click = self._handle_click
        self.on_hover = self._handle_hover

        # 更新显示
        self._update_display()

    def _handle_click(self, e) -> None:
        """处理点击事件"""
        if self._on_toggle:
            self._on_toggle(self.position)

    def _handle_hover(self, e) -> None:
        """处理悬停事件"""
        if e.data == "true":
            self.bgcolor = COLORS.BUTTON_BG_HOVER
        else:
            self.bgcolor = COLORS.SURFACE if self._value == 0 else COLORS.PRIMARY
        self.update()

    def _update_display(self) -> None:
        """更新显示"""
        self.bgcolor = COLORS.PRIMARY if self._value == 1 else COLORS.SURFACE
        self.content = ft.Text(
            value=str(self._value),
            size=SIZES.FONT_SIZE_BINARY,
            color=COLORS.TEXT_PRIMARY,
            weight=ft.FontWeight.W_500,
        )

    def set_value(self, value: int) -> None:
        """
        设置值

        Args:
            value: 新值（0或1）
        """
        self._value = value
        self._update_display()


class BinaryPanel(ft.Container):
    """
    二进制位显示面板

    显示当前数值的二进制形式，支持点击切换特定位
    根据 BitMode 显示不同位数
    """

    def __init__(
        self,
        bit_mode: int = BIT_MODES.QWORD,
        on_bit_toggle: Optional[Callable[[int], None]] = None,
        **kwargs,
    ):
        """
        初始化二进制面板

        Args:
            bit_mode: 位模式（QWORD/DWORD/WORD/BYTE）
            on_bit_toggle: 位切换回调函数
        """
        super().__init__(**kwargs)

        self._bit_mode = bit_mode
        self._on_bit_toggle = on_bit_toggle
        self._current_value = 0

        # 存储所有位控件
        self._bits: List[BinaryBit] = []

        # 设置容器样式
        self.padding = ft.padding.all(SIZES.PADDING_SMALL)
        self.bgcolor = COLORS.SURFACE
        self.border_radius = 8

        # 构建内容
        self._build_content()

    def _build_content(self) -> None:
        """构建面板内容"""
        # 清空现有位
        self._bits.clear()

        # 创建位显示行
        rows = []

        # 计算行数（每行16位，分成4组，每组4位）
        num_bits = self._bit_mode
        num_rows = num_bits // 16

        for row_idx in range(num_rows):
            # 计算这一行的位位置范围
            start_pos = (num_rows - 1 - row_idx) * 16
            end_pos = start_pos + 16

            # 创建位组
            bit_groups = []

            for group_idx in range(4):
                group_start = start_pos + group_idx * 4
                group_end = group_start + 4

                # 创建组内的位
                group_bits = []
                for pos in range(group_end - 1, group_start - 1, -1):
                    bit = BinaryBit(
                        position=pos,
                        value=0,
                        on_toggle=self._handle_bit_toggle,
                    )
                    self._bits.append(bit)
                    group_bits.append(bit)

                # 组容器
                group_container = ft.Row(
                    controls=group_bits,
                    spacing=1,
                )
                bit_groups.append(group_container)

            # 位位置标签
            position_label = ft.Text(
                value=f"({end_pos - 1}-{start_pos})",
                size=10,
                color=COLORS.TEXT_SECONDARY,
            )

            # 行容器
            row_container = ft.Row(
                controls=[
                    ft.Row(controls=bit_groups, spacing=4),
                    position_label,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            )
            rows.append(row_container)

        # 设置内容
        self.content = ft.Column(
            controls=rows,
            spacing=4,
        )

    def _handle_bit_toggle(self, position: int) -> None:
        """
        处理位切换

        Args:
            position: 被切换的位位置
        """
        if self._on_bit_toggle:
            self._on_bit_toggle(position)

    def set_value(self, value: int) -> None:
        """
        设置当前值，更新所有位显示

        Args:
            value: 整数值
        """
        self._current_value = value

        # 更新每个位
        for bit in self._bits:
            bit_value = (value >> bit.position) & 1
            bit.set_value(bit_value)

    def set_bit_mode(self, mode: int) -> None:
        """
        设置位模式

        Args:
            mode: 位模式（QWORD/DWORD/WORD/BYTE）
        """
        if mode != self._bit_mode:
            self._bit_mode = mode
            self._build_content()
            self.set_value(self._current_value)

    def get_current_value(self) -> int:
        """获取当前值"""
        return self._current_value

    def get_bit_mode_name(self) -> str:
        """获取当前位模式名称"""
        return BIT_MODES.NAMES.get(self._bit_mode, "QWORD")