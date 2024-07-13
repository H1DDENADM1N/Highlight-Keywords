@echo off
chcp 65001 >nul

REM Used to add a system-level context menu for the Highlight-Keywords-EmbeddedPython version.
REM Do not use this script when running from source

pushd "%~dp0"
reg query "HKU\S-1-5-19" >nul 2>&1 || (
    powershell -Command "Start-Process '%~sdpnx0' -Verb RunAs" && exit
)

:MENU
echo Please move the folder to a stable path before adding the right-click menu item.

echo.
echo  1. Add Explorer right-click menu items
echo.
echo  2. Remove Explorer right-click menu items
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
echo Add Completed
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
echo Remove Completed
timeout /t 5 >nul
cls
goto MENU
