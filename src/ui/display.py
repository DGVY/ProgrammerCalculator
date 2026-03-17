# -*- coding: utf-8 -*-
"""
程序员计算器 - 进制显示区组件
显示HEX/DEC/OCT/BIN四种进制的数值，支持切换当前编辑进制
"""

import flet as ft
from typing import Callable, Optional
from enum import Enum

from src.utils.constants import COLORS, SIZES


class BaseMode(str, Enum):
    """进制模式枚举"""

    HEX = "HEX"  # 十六进制
    DEC = "DEC"  # 十进制
    OCT = "OCT"  # 八进制
    BIN = "BIN"  # 二进制


class BaseDisplayRow(ft.Container):
    """
    单个进制显示行

    显示进制标签和对应的数值，支持点击选择
    """

    def __init__(
        self,
        base: BaseMode,
        value: str,
        selected: bool = False,
        on_click: Optional[Callable[[BaseMode], None]] = None,
        **kwargs,
    ):
        """
        初始化进制显示行

        Args:
            base: 进制模式
            value: 显示的数值字符串
            selected: 是否被选中
            on_click: 点击回调函数
        """
        super().__init__(**kwargs)

        self.base = base
        self._value = value
        self._selected = selected
        self._on_click = on_click

        # 设置容器样式
        self.padding = ft.padding.only(left=16, right=16, top=8, bottom=8)
        self.on_click = self._handle_click
        self.border_radius = 4

        # 更新显示
        self._update_style()
        self._build_content()

    def _handle_click(self, e) -> None:
        """处理点击事件"""
        if self._on_click:
            self._on_click(self.base)

    def _update_style(self) -> None:
        """更新选中状态样式"""
        if self._selected:
            self.bgcolor = COLORS.SURFACE
            self.border = ft.border.only(
                left=ft.BorderSide(3, COLORS.PRIMARY)
            )
        else:
            self.bgcolor = "transparent"
            self.border = None

    def _build_content(self) -> None:
        """构建内容"""
        # 进制标签颜色映射
        base_colors = {
            BaseMode.HEX: COLORS.HEX_COLOR,
            BaseMode.DEC: COLORS.DEC_COLOR,
            BaseMode.OCT: COLORS.OCT_COLOR,
            BaseMode.BIN: COLORS.BIN_COLOR,
        }

        # 创建内容
        self.content = ft.Row(
            controls=[
                # 进制标签
                ft.Container(
                    content=ft.Text(
                        value=self.base.value,
                        size=SIZES.FONT_SIZE_LABEL,
                        weight=ft.FontWeight.W_600,
                        color=base_colors.get(self.base, COLORS.TEXT_SECONDARY),
                    ),
                    width=40,
                ),
                # 数值显示
                ft.Text(
                    value=self._value,
                    size=SIZES.FONT_SIZE_BUTTON,
                    color=COLORS.TEXT_PRIMARY,
                    expand=True,
                    text_align=ft.TextAlign.RIGHT,
                    no_wrap=True,
                    overflow=ft.TextOverflow.ELLIPSIS,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

    def set_value(self, value: str) -> None:
        """
        设置显示值

        Args:
            value: 新的数值字符串
        """
        self._value = value
        self._build_content()

    def set_selected(self, selected: bool) -> None:
        """
        设置选中状态

        Args:
            selected: 是否选中
        """
        self._selected = selected
        self._update_style()


class DisplayPanel(ft.Container):
    """
    进制显示面板

    显示所有四种进制的数值，支持切换当前编辑的进制
    """

    def __init__(
        self,
        on_base_change: Optional[Callable[[BaseMode], None]] = None,
        **kwargs,
    ):
        """
        初始化显示面板

        Args:
            on_base_change: 进制切换回调函数
        """
        super().__init__(**kwargs)

        self._on_base_change = on_base_change
        self._current_base = BaseMode.DEC
        self._current_value = 0

        # 初始化进制显示行
        self._displays: dict[BaseMode, BaseDisplayRow] = {}

        # 设置容器样式
        self.padding = ft.padding.all(SIZES.PADDING_SMALL)
        self.bgcolor = COLORS.SURFACE
        self.border_radius = 8

        # 构建内容
        self._build_content()

    def _build_content(self) -> None:
        """构建面板内容"""
        # 创建各进制显示行
        for base in [BaseMode.HEX, BaseMode.DEC, BaseMode.OCT, BaseMode.BIN]:
            self._displays[base] = BaseDisplayRow(
                base=base,
                value="0",
                selected=(base == self._current_base),
                on_click=self._handle_base_click,
            )

        # 主数值显示区域（右上角大号数字）
        self._main_display = ft.Container(
            content=ft.Text(
                value="0",
                size=SIZES.FONT_SIZE_DISPLAY,
                weight=ft.FontWeight.W_300,
                color=COLORS.TEXT_PRIMARY,
                text_align=ft.TextAlign.RIGHT,
            ),
            padding=ft.padding.only(
                left=SIZES.PADDING_MEDIUM,
                right=SIZES.PADDING_MEDIUM,
                top=SIZES.PADDING_SMALL,
                bottom=SIZES.PADDING_MEDIUM,
            ),
            alignment=ft.alignment.center_right,
        )

        # 组装内容
        self.content = ft.Column(
            controls=[
                # 主显示区
                self._main_display,
                ft.Divider(height=1, color=COLORS.BUTTON_BG),
                # 进制显示区
                ft.Column(
                    controls=[self._displays[base] for base in BaseMode],
                    spacing=2,
                ),
            ],
            spacing=0,
        )

    def _handle_base_click(self, base: BaseMode) -> None:
        """
        处理进制切换点击

        Args:
            base: 被点击的进制
        """
        if base != self._current_base:
            # 更新选中状态
            self._displays[self._current_base].set_selected(False)
            self._current_base = base
            self._displays[self._current_base].set_selected(True)

            # 触发回调
            if self._on_base_change:
                self._on_base_change(base)

    def set_value(self, value: int) -> None:
        """
        设置当前值，更新所有进制显示

        Args:
            value: 整数值
        """
        self._current_value = value

        # 更新主显示
        main_text = self._main_display.content
        main_text.value = self._format_value(value, self._current_base)
        self._main_display.update()

        # 更新各进制显示
        for base in BaseMode:
            self._displays[base].set_value(self._format_value(value, base))

    def _format_value(self, value: int, base: BaseMode) -> str:
        """
        根据进制格式化数值

        Args:
            value: 整数值
            base: 目标进制

        Returns:
            格式化后的字符串
        """
        if value == 0:
            return "0"

        if base == BaseMode.HEX:
            return f"{value:X}"
        elif base == BaseMode.DEC:
            return str(value)
        elif base == BaseMode.OCT:
            return format(value, "o")
        elif base == BaseMode.BIN:
            return format(value, "b")

        return str(value)

    def get_current_base(self) -> BaseMode:
        """获取当前编辑的进制"""
        return self._current_base

    def get_value(self) -> int:
        """获取当前值"""
        return self._current_value