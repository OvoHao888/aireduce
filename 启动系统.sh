#!/usr/bin/env bash
#
# AI 降重系统 - 一键启动（Linux / macOS）
# 用法：chmod +x 启动系统.sh && ./启动系统.sh
#
set -uo pipefail

cd "$(dirname "$0")"

echo "============================================================"
echo "  AI 降重系统 - 一键启动"
echo "============================================================"
echo

# ---------------- 环境检查 ----------------
if ! command -v python3 >/dev/null 2>&1; then
    echo "[错误] 未找到 python3，请安装 Python 3.11 或更高版本"
    exit 1
fi

if ! command -v npm >/dev/null 2>&1; then
    echo "[错误] 未找到 npm，请安装 Node.js"
    exit 1
fi

# ---------------- 后端虚拟环境 ----------------
if [ ! -x "backend/venv/bin/python" ]; then
    echo "[1/4] 创建后端虚拟环境..."
    python3 -m venv backend/venv || { echo "[错误] 虚拟环境创建失败"; exit 1; }
fi

echo "[2/4] 安装后端依赖..."
backend/venv/bin/python -m pip install -r backend/requirements.txt || {
    echo "[错误] 后端依赖安装失败，请检查网络后重试"; exit 1;
}

# ---------------- 配置文件 ----------------
if [ ! -f "backend/.env" ]; then
    cp backend/.env.example backend/.env
    cat <<'EOF'

============================================================
  [需要配置] 已为你生成 backend/.env
============================================================
  启动前还需要两步：

  1. 创建数据库并导入表结构（需本机已安装 MySQL）：
       mysql -u root -p < backend/init.sql

  2. 用编辑器打开 backend/.env，至少填写：
       DB_PASSWORD   数据库口令
       SECRET_KEY    随机字符串，至少 32 位
       API_KEY       大模型 API Key（也可启动后在后台页面配置）

  配置完成后重新执行本脚本即可。
============================================================

EOF
    exit 0
fi

# ---------------- 前端依赖 ----------------
if [ ! -d "AIReduce/node_modules" ]; then
    echo "[3/4] 安装前端依赖（首次较慢）..."
    ( cd AIReduce && npm install ) || { echo "[错误] 前端依赖安装失败"; exit 1; }
fi

# ---------------- 启动 ----------------
echo "[4/4] 启动服务..."
( cd backend && venv/bin/python main.py ) &
BACKEND_PID=$!
( cd AIReduce && npm run dev ) &
FRONTEND_PID=$!

cleanup() {
    echo
    echo "正在停止服务..."
    kill "$BACKEND_PID" "$FRONTEND_PID" 2>/dev/null || true
    wait "$BACKEND_PID" "$FRONTEND_PID" 2>/dev/null || true
    echo "已停止。"
}
trap cleanup INT TERM

echo
echo "============================================================"
echo "  启动完成"
echo "============================================================"
echo "  后端接口 : http://127.0.0.1:8000"
echo "  接口文档 : http://127.0.0.1:8000/docs"
echo "  前端页面 : http://127.0.0.1:5173"
echo
echo "  管理后台（可选）：另开一个终端执行"
echo "      cd adminAireduce && npm install && npm run dev"
echo
echo "  按 Ctrl+C 停止全部服务。"
echo "============================================================"
echo

wait
