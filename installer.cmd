@REM get admin permissions for script
@echo off
:: BatchGotAdmin
:-------------------------------------
REM  --> check for permissions
    IF "%PROCESSOR_ARCHITECTURE%" EQU "amd64" (
>nul 2>&1 "%SYSTEMROOT%\SysWOW64\cacls.exe" "%SYSTEMROOT%\SysWOW64\config\system"
) ELSE (
>nul 2>&1 "%SYSTEMROOT%\system32\cacls.exe" "%SYSTEMROOT%\system32\config\system"
)

REM --> if error flag set, we do not have admin.
if '%errorlevel%' NEQ '0' (
    echo Requesting administrative privileges...
    goto UACPrompt
) else ( goto gotAdmin )

:UACPrompt
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    set params= %*
    echo UAC.ShellExecute "cmd.exe", "/c ""%~s0"" %params:"=""%", "", "runas", 1 >> "%temp%\getadmin.vbs"

    "%temp%\getadmin.vbs"
    del "%temp%\getadmin.vbs"
    exit /B

:gotAdmin
    pushd "%CD%"
    CD /D "%~dp0"

@REM start installation process

@REM confirm installation
echo Are you sure you want to install "capulator" (Y/N)
set/p "cho=>"
if %cho%==Y goto INSTALL
if %cho%==y goto INSTALL
if %cho%==n goto END
if %cho%==N goto END
echo Invalid choice.
goto END

@REM installs dependencies
:INSTALL
echo Installing Python Packages...
pip3 install Pillow
pip3 install cryptography
echo Packages Installed!

echo Moving Directories...
move Capulator C:\ProgramData
echo Direcrtories Moved!

@REM echo Inastallation Complete, You May Start "capulator.py"
@REM pause

echo Starting "capulator.py"
python3 capulator.py

@REM exits installer
:END
exit
