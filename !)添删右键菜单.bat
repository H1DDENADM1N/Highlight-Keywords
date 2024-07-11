@echo off
chcp 65001 >nul

REM 用于给 Highlight-Keywords-EmbeddedPython 版本 添加 系统级上下文菜单
REM 从源码运行不要使用此脚本

pushd "%~dp0"
reg query "HKU\S-1-5-19" >nul 2>&1 || (
    powershell -Command "Start-Process '%~sdpnx0' -Verb RunAs" && exit
)

:MENU
echo 请先将文件夹移动到稳定的路径，再添加右键菜单项。

echo.
echo  1、添加资源管理器右键菜单项
echo.
echo  2、移除资源管理器右键菜单项
choice /C 123 /N >nul 2>nul
if "%ERRORLEVEL%"=="2" goto RemoveMenu
if "%ERRORLEVEL%"=="1" goto AddMenu

:AddMenu
reg add "HKEY_CLASSES_ROOT\SystemFileAssociations\.txt\shell\Item0" /f /v "MUIVerb" /d "Highlight Keywords" >nul
reg add "HKEY_CLASSES_ROOT\SystemFileAssociations\.txt\shell\Item0" /f /v "Icon" /d "%~dp0assets\icon.ico,0" >nul
reg add "HKEY_CLASSES_ROOT\SystemFileAssociations\.txt\shell\Item0\command" /f /ve /d "%~dp0highlight_keywords.exe \"%%1\"" >nul

reg add "HKEY_CLASSES_ROOT\SystemFileAssociations\.md\shell\Item0" /f /v "MUIVerb" /d "Highlight Keywords" >nul
reg add "HKEY_CLASSES_ROOT\SystemFileAssociations\.md\shell\Item0" /f /v "Icon" /d "%~dp0assets\icon.ico,0" >nul
reg add "HKEY_CLASSES_ROOT\SystemFileAssociations\.md\shell\Item0\command" /f /ve /d "%~dp0highlight_keywords.exe \"%%1\"" >nul

reg add "HKEY_CLASSES_ROOT\SystemFileAssociations\.ocr\shell\Item0" /f /v "MUIVerb" /d "Highlight Keywords" >nul
reg add "HKEY_CLASSES_ROOT\SystemFileAssociations\.ocr\shell\Item0" /f /v "Icon" /d "%~dp0assets\icon.ico,0" >nul
reg add "HKEY_CLASSES_ROOT\SystemFileAssociations\.ocr\shell\Item0\command" /f /ve /d "%~dp0highlight_keywords.exe \"%%1\"" >nul

echo.
echo 添加完成
timeout /t 3 >nul
cls
goto MENU

:RemoveMenu
reg delete "HKEY_CLASSES_ROOT\SystemFileAssociations\.txt\shell\Item0\command" /f /ve >nul 2>&1
reg delete "HKEY_CLASSES_ROOT\SystemFileAssociations\.txt\shell\Item0" /f /v "Icon" >nul 2>&1
reg delete "HKEY_CLASSES_ROOT\SystemFileAssociations\.txt\shell\Item0" /f /v "MUIVerb" >nul 2>&1
reg delete "HKEY_CLASSES_ROOT\SystemFileAssociations\.txt\shell\Item0" /f >nul 2>&1

reg delete "HKEY_CLASSES_ROOT\SystemFileAssociations\.md\shell\Item0\command" /f /ve >nul 2>&1
reg delete "HKEY_CLASSES_ROOT\SystemFileAssociations\.md\shell\Item0" /f /v "Icon" >nul 2>&1
reg delete "HKEY_CLASSES_ROOT\SystemFileAssociations\.md\shell\Item0" /f /v "MUIVerb" >nul 2>&1
reg delete "HKEY_CLASSES_ROOT\SystemFileAssociations\.md\shell\Item0" /f >nul 2>&1

reg delete "HKEY_CLASSES_ROOT\SystemFileAssociations\.ocr\shell\Item0\command" /f /ve >nul 2>&1
reg delete "HKEY_CLASSES_ROOT\SystemFileAssociations\.ocr\shell\Item0" /f /v "Icon" >nul 2>&1
reg delete "HKEY_CLASSES_ROOT\SystemFileAssociations\.ocr\shell\Item0" /f /v "MUIVerb" >nul 2>&1
reg delete "HKEY_CLASSES_ROOT\SystemFileAssociations\.ocr\shell\Item0" /f >nul 2>&1

echo.
echo 移除完成
timeout /t 5 >nul
cls
goto MENU
