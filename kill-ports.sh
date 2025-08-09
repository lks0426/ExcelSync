#!/bin/bash

# ExcelSync 端口清理脚本
# 用于关闭 3000, 3001, 8000, 8001 端口上的进程

echo "🔄 开始清理 ExcelSync 相关端口..."
echo "========================================"

# 定义要清理的端口
PORTS=(3000 3001 8000 8001)

# 遍历每个端口并关闭
for port in "${PORTS[@]}"; do
    echo "🔍 检查端口 $port..."
    
    # 检查端口是否被使用
    if sudo fuser $port/tcp &>/dev/null; then
        echo "❌ 端口 $port 正在被使用，正在关闭..."
        sudo fuser -k $port/tcp 2>/dev/null
        sleep 1
        
        # 再次检查是否成功关闭
        if sudo fuser $port/tcp &>/dev/null; then
            echo "⚠️  端口 $port 可能仍在使用中"
        else
            echo "✅ 端口 $port 已成功关闭"
        fi
    else
        echo "✅ 端口 $port 已经可用"
    fi
done

echo "========================================"
echo "🎉 端口清理完成！"
echo ""
echo "端口状态："
for port in "${PORTS[@]}"; do
    if sudo fuser $port/tcp &>/dev/null; then
        echo "  端口 $port: ❌ 仍在使用"
    else
        echo "  端口 $port: ✅ 可用"
    fi
done

echo ""
echo "💡 提示："
echo "  - 前端启动: cd frontend && npm run dev"
echo "  - 后端启动: cd backend && python app.py"