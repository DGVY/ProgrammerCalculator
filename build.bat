@echo off
chcp 65001 >nul
REM 程序员计算器 - Windows打包脚本
REM 用于构建Windows平台的可执行文件

setlocal enabledelayedexpansion

echo ==========================================
echo 程序员计算器 - Windows打包脚本
echo ==========================================

REM 检查参数
if "%1"=="" goto help
if "%1"=="help" goto help
if "%1"=="--help" goto help
if "%1"=="-h" goto help

REM 检查Flet是否安装
flet --version >nul 2>&1
if errorlevel 1 (
    echo 错误: Flet未安装
    echo 请运行: pip install flet
    exit /b 1
)

REM 根据参数执行构建
if "%1"=="windows" goto build_windows
if "%1"=="android" goto build_android
if "%1"=="web" goto build_web
if "%1"=="all" goto build_all

echo 错误: 未知平台 '%1'
goto help

:build_windows
echo.
echo ^>^>^> 构建Windows可执行文件...
flet build windows --org com.programmercalc --project calculator --product-name "程序员计算器" --product-version "1.0.0"
echo ✓ Windows构建完成: build\windows\
goto end

:build_android
echo.
echo ^>^>^> 构建Android APK...
echo 注意: Android构建可能需要Android SDK
flet build apk --org com.programmercalc --project calculator --product-name "程序员计算器" --product-version "1.0.0"
echo ✓ Android构建完成: build\apk\
goto end

:build_web
echo.
echo ^>^>^> 构建Web应用...
flet build web --project calculator --product-name "程序员计算器" --product-version "1.0.0"
echo ✓ Web构建完成: build\web\
goto end

:build_all
call :build_windows
call :build_android
call :build_web
echo.
echo ==========================================
echo 所有构建完成！
echo ==========================================
goto end

:help
echo 用法: %0 ^<平台^>
echo.
echo 可用平台:
echo   windows   - 构建Windows可执行文件
echo   android   - 构建Android APK
echo   web       - 构建Web应用
echo   all       - 构建所有平台
echo   help      - 显示此帮助信息
echo.
echo 示例:
echo   %0 windows    # 构建Windows版本
echo   %0 android    # 构建Android APK
goto end

:end
endlocal