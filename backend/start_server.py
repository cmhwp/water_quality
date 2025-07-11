#!/usr/bin/env python3
"""
服务器启动脚本
"""
import sys
import subprocess
import os

def check_and_install_dependencies():
    """检查和安装依赖"""
    print("检查依赖包...")
    
    try:
        import fastapi
        import uvicorn
        import sqlalchemy
        import pydantic
        import passlib
        import jose
        import pandas
        import openpyxl
        from pydantic import EmailStr
        print("✅ 所有依赖包已安装")
        return True
    except ImportError as e:
        print(f"❌ 缺少依赖包: {e}")
        print("正在安装依赖包...")
        
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                         check=True, capture_output=True, text=True)
            print("✅ 依赖包安装完成")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ 依赖包安装失败: {e}")
            return False

def check_database():
    """检查数据库"""
    print("检查数据库...")
    
    if not os.path.exists("water_quality.db"):
        print("❌ 数据库文件不存在")
        print("正在创建数据库和导入数据...")
        
        try:
            subprocess.run([sys.executable, "scripts/import_data.py"], 
                         check=True, capture_output=True, text=True)
            print("✅ 数据库创建完成")
            return True
        except subprocess.CalledProcessError as e:
            print(f"❌ 数据库创建失败: {e}")
            return False
    else:
        print("✅ 数据库文件存在")
        return True

def start_server():
    """启动服务器"""
    print("启动服务器...")
    
    try:
        import uvicorn
        from main import app
        
        print("=" * 50)
        print("🚀 水质数据管理系统启动中...")
        print("=" * 50)
        print("📖 API文档: http://localhost:8000/api/v1/docs")
        print("🔍 ReDoc: http://localhost:8000/api/v1/redoc")
        print("💻 健康检查: http://localhost:8000/health")
        print("=" * 50)
        print("默认管理员账户:")
        print("📧 邮箱: admin@waterquality.com")
        print("🔑 密码: admin123")
        print("=" * 50)
        
        uvicorn.run(
            "main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info"
        )
        
    except Exception as e:
        print(f"❌ 服务器启动失败: {e}")
        return False

def main():
    """主函数"""
    print("=" * 50)
    print("水质数据管理系统 - 启动脚本")
    print("=" * 50)
    
    # 检查依赖
    if not check_and_install_dependencies():
        sys.exit(1)
    
    # 检查数据库
    if not check_database():
        sys.exit(1)
    
    # 启动服务器
    start_server()

if __name__ == "__main__":
    main() 