@echo off
chcp 65001 >nul

REM ============================================================
REM  AI 降重系统 - 一键启动（Windows）
REM  用法：双击本文件
REM ============================================================

cd /d "%~dp0"

echo ============================================================
echo   AI 降重系统 - 一键启动
echo ============================================================
echo.

REM ---------------- 环境检查 ----------------
where python >nul 2>nul
if errorlevel 1 goto :no_python

where npm >nul 2>nul
if errorlevel 1 goto :no_npm

REM ---------------- 后端虚拟环境 ----------------
if exist "backend\venv\Scripts\python.exe" goto :venv_ok

echo [1/4] 创建后端虚拟环境...
python -m venv backend\venv
if errorlevel 1 goto :venv_fail

:venv_ok
echo [2/4] 安装后端依赖...
backend\venv\Scripts\python.exe -m pip install -r backend\requirements.txt
if errorlevel 1 goto :pip_fail

REM ---------------- 配置文件 ----------------
if exist "backend\.env" goto :env_ok

copy "backend\.env.example" "backend\.env" >nul
echo.
echo ============================================================
echo   [需要配置] 已为你生成 backend\.env
echo ============================================================
echo   启动前还需要两步：
echo.
echo   1. 创建数据库并导入表结构（需本机已安装 MySQL）：
echo        mysql -u root -p ^< backend\init.sql
echo.
echo   2. 用编辑器打开 backend\.env，至少填写：
echo        DB_PASSWORD   数据库口令
echo        SECRET_KEY    随机字符串，至少 32 位
echo        API_KEY       大模型 API Key（也可启动后在后台页面配置）
echo.
echo   配置完成后重新双击本文件即可。
echo ============================================================
echo.
pause
exit /b 0

:env_ok
REM ---------------- 前端依赖 ----------------
if exist "AIReduce\node_modules" goto :deps_ok

echo [3/4] 安装前端依赖（首次较慢）...
pushd AIReduce
call npm install
if errorlevel 1 goto :npm_fail
popd

:deps_ok
REM ---------------- 启动 ----------------
echo [4/4] 启动服务...
start "AI降重 - 后端" cmd /k "cd /d %~dp0backend && venv\Scripts\python.exe main.py"
timeout /t 3 /nobreak >nul
start "AI降重 - 前端" cmd /k "cd /d %~dp0AIReduce && npm run dev"

echo.
echo ============================================================
echo   启动完成
echo ============================================================
echo   后端接口 : http://127.0.0.1:8000
echo   接口文档 : http://127.0.0.1:8000/docs
echo   前端页面 : http://127.0.0.1:5173
echo.
echo   管理后台（可选）：另开一个命令行窗口执行
echo       cd adminAireduce
echo       npm install
echo       npm run dev
echo.
echo   注意：关闭本窗口不会停止服务，
echo         请到「AI降重 - 后端 / 前端」两个窗口按 Ctrl+C 停止。
echo ============================================================
echo.
pause
exit /b 0

REM ---------------- 错误分支 ----------------
:no_python
echo [错误] 未找到 python，请安装 Python 3.11 或更高版本并加入 PATH
pause
exit /b 1

:no_npm
echo [错误] 未找到 npm，请安装 Node.js 并加入 PATH
pause
exit /b 1

:venv_fail
echo [错误] 虚拟环境创建失败
pause
exit /b 1

:pip_fail
echo [错误] 后端依赖安装失败，请检查网络后重试
pause
exit /b 1

:npm_fail
popd
echo [错误] 前端依赖安装失败，请检查网络后重试
pause
exit /b 1
