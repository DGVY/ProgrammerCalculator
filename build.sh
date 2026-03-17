#!/bin/bash
# -*- coding: utf-8 -*-
# 程序员计算器 - 打包脚本
# 用于构建Linux、Windows、Android平台的可执行文件

set -e

PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_DIR"

# 激活虚拟环境
if [ -d ".venv" ]; then
    source .venv/bin/activate
fi

echo "=========================================="
echo "程序员计算器 - 打包脚本"
echo "=========================================="

# 显示帮助信息
show_help() {
    echo "用法: $0 <平台>"
    echo ""
    echo "可用平台:"
    echo "  linux     - 构建Linux可执行文件"
    echo "  windows   - 构建Windows可执行文件 (需要在Windows上运行)"
    echo "  android   - 构建Android APK"
    echo "  web       - 构建Web应用"
    echo "  all       - 构建所有可用平台"
    echo "  help      - 显示此帮助信息"
    echo ""
    echo "示例:"
    echo "  $0 linux      # 构建Linux版本"
    echo "  $0 android    # 构建Android APK"
}

# 检查Flet是否安装
check_flet() {
    if ! command -v flet &> /dev/null; then
        echo "错误: Flet未安装"
        echo "请运行: pip install flet"
        exit 1
    fi
    echo "✓ Flet版本: $(flet --version 2>/dev/null || echo '未知')"
}

# 构建Linux版本
build_linux() {
    echo ""
    echo ">>> 构建Linux可执行文件..."
    flet build linux \
        --org com.programmercalc \
        --project calculator \
        --product-name "程序员计算器" \
        --product-version "1.0.0"
    echo "✓ Linux构建完成: build/linux/"
}

# 构建Windows版本
build_windows() {
    echo ""
    echo ">>> 构建Windows可执行文件..."
    echo "注意: Windows构建需要在Windows系统上运行"
    flet build windows \
        --org com.programmercalc \
        --project calculator \
        --product-name "程序员计算器" \
        --product-version "1.0.0"
    echo "✓ Windows构建完成: build/windows/"
}

# 构建Android APK
build_android() {
    echo ""
    echo ">>> 构建Android APK..."
    flet build apk \
        --org com.programmercalc \
        --project calculator \
        --product-name "程序员计算器" \
        --product-version "1.0.0"
    echo "✓ Android构建完成: build/apk/"
}

# 构建Web版本
build_web() {
    echo ""
    echo ">>> 构建Web应用..."
    flet build web \
        --project calculator \
        --product-name "程序员计算器" \
        --product-version "1.0.0"
    echo "✓ Web构建完成: build/web/"
}

# 主逻辑
case "${1:-help}" in
    linux)
        check_flet
        build_linux
        ;;
    windows)
        check_flet
        build_windows
        ;;
    android)
        check_flet
        build_android
        ;;
    web)
        check_flet
        build_web
        ;;
    all)
        check_flet
        build_linux
        build_android
        build_web
        echo ""
        echo "=========================================="
        echo "所有构建完成！"
        echo "=========================================="
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        echo "错误: 未知平台 '$1'"
        echo ""
        show_help
        exit 1
        ;;
esac