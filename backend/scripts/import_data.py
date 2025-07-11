"""
数据导入脚本
"""
import sys
import os
from pathlib import Path
from datetime import datetime
import pandas as pd
from passlib.context import CryptContext

# 添加项目根目录到路径
sys.path.append(str(Path(__file__).parent.parent))

from app.db.base import engine, Base, SessionLocal
from app.models.water_quality import WaterQuality
from app.models.user import User
from config import settings

# 密码加密上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_tables():
    """创建数据库表"""
    print("创建数据库表...")
    Base.metadata.create_all(bind=engine)
    print("数据库表创建完成")


def clean_and_convert_data(df):
    """清理和转换数据"""
    print("清理和转换数据...")
    
    # 列名映射
    column_mapping = {
        '取样日期': 'sampling_date',
        '取样时间': 'sampling_time',
        '检测日期': 'detection_date',
        '编号': 'code',
        '河道名称': 'river_name',
        'COD': 'cod_value',
        'COD等级': 'cod_level',
        '氨氮': 'ammonia_nitrogen_value',
        '氨氮等级': 'ammonia_nitrogen_level',
        '总磷': 'total_phosphorus_value',
        '总磷等级': 'total_phosphorus_level',
        '高锰酸钾': 'potassium_permanganate_value',
        '高锰酸钾等级': 'potassium_permanganate_level',
        '综合水质等级': 'comprehensive_quality_level',
        '综合等级数': 'comprehensive_level_number',
        '方式': 'method'
    }
    
    # 重命名列
    df = df.rename(columns=column_mapping)
    
    # 处理缺失值
    df['sampling_time'] = df['sampling_time'].fillna("")
    df['code'] = df['code'].fillna("")
    df['method'] = df['method'].fillna("")
    
    # 数值型字段保持NaN，稍后处理
    numeric_columns = ['cod_value', 'ammonia_nitrogen_value', 'total_phosphorus_value', 'potassium_permanganate_value']
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # 字符串型字段用空字符串填充
    string_columns = ['cod_level', 'ammonia_nitrogen_level', 'total_phosphorus_level', 'potassium_permanganate_level', 'comprehensive_quality_level']
    for col in string_columns:
        df[col] = df[col].fillna("")
    
    # 综合等级数字段
    df['comprehensive_level_number'] = pd.to_numeric(df['comprehensive_level_number'], errors='coerce')
    
    # 确保日期类型正确
    df['sampling_date'] = pd.to_datetime(df['sampling_date'])
    df['detection_date'] = pd.to_datetime(df['detection_date'])
    
    # 添加系统字段
    df['created_at'] = datetime.now()
    df['updated_at'] = datetime.now()
    df['remarks'] = None
    
    print(f"数据清理完成，共 {len(df)} 条记录")
    return df


def import_excel_data(file_path):
    """导入Excel数据"""
    print(f"开始导入Excel数据: {file_path}")
    
    # 检查文件是否存在
    if not os.path.exists(file_path):
        print(f"文件不存在: {file_path}")
        return False
    
    try:
        # 读取Excel文件
        df = pd.read_excel(file_path)
        print(f"成功读取Excel文件，共 {len(df)} 行数据")
        
        # 清理和转换数据
        df_cleaned = clean_and_convert_data(df)
        
        # 创建数据库会话
        db = SessionLocal()
        
        try:
            # 检查是否已有数据
            existing_count = db.query(WaterQuality).count()
            if existing_count > 0:
                print(f"数据库中已有 {existing_count} 条记录")
                response = input("是否清空现有数据并重新导入? (y/N): ")
                if response.lower() == 'y':
                    db.query(WaterQuality).delete()
                    db.commit()
                    print("已清空现有数据")
                else:
                    print("跳过数据导入")
                    return True
            
            # 批量插入数据
            print("开始批量插入数据...")
            batch_size = 100
            total_records = len(df_cleaned)
            
            for i in range(0, total_records, batch_size):
                batch_data = df_cleaned.iloc[i:i+batch_size]
                records = []
                
                for _, row in batch_data.iterrows():
                    record = WaterQuality(
                        sampling_date=row['sampling_date'],
                        sampling_time=row['sampling_time'] if row['sampling_time'] else None,
                        detection_date=row['detection_date'],
                        code=row['code'] if row['code'] else None,
                        river_name=row['river_name'],
                        method=row['method'] if row['method'] else None,
                        cod_value=row['cod_value'] if pd.notna(row['cod_value']) else None,
                        cod_level=row['cod_level'] if row['cod_level'] else None,
                        ammonia_nitrogen_value=row['ammonia_nitrogen_value'] if pd.notna(row['ammonia_nitrogen_value']) else None,
                        ammonia_nitrogen_level=row['ammonia_nitrogen_level'] if row['ammonia_nitrogen_level'] else None,
                        total_phosphorus_value=row['total_phosphorus_value'] if pd.notna(row['total_phosphorus_value']) else None,
                        total_phosphorus_level=row['total_phosphorus_level'] if row['total_phosphorus_level'] else None,
                        potassium_permanganate_value=row['potassium_permanganate_value'] if pd.notna(row['potassium_permanganate_value']) else None,
                        potassium_permanganate_level=row['potassium_permanganate_level'] if row['potassium_permanganate_level'] else None,
                        comprehensive_quality_level=row['comprehensive_quality_level'] if row['comprehensive_quality_level'] else None,
                        comprehensive_level_number=row['comprehensive_level_number'] if pd.notna(row['comprehensive_level_number']) else None,
                        created_at=row['created_at'],
                        updated_at=row['updated_at'],
                        remarks=row['remarks']
                    )
                    records.append(record)
                
                db.add_all(records)
                db.commit()
                print(f"已导入 {min(i + batch_size, total_records)}/{total_records} 条记录")
            
            print(f"数据导入完成，共导入 {total_records} 条记录")
            return True
            
        except Exception as e:
            print(f"导入数据时出错: {str(e)}")
            db.rollback()
            return False
        finally:
            db.close()
            
    except Exception as e:
        print(f"读取Excel文件时出错: {str(e)}")
        return False


def create_admin_user():
    """创建管理员用户"""
    print("创建管理员用户...")
    
    db = SessionLocal()
    try:
        # 检查是否已有管理员用户
        existing_admin = db.query(User).filter(User.email == settings.ADMIN_EMAIL).first()
        if existing_admin:
            print(f"管理员用户已存在: {settings.ADMIN_EMAIL}")
            return True
        
        # 创建管理员用户
        hashed_password = pwd_context.hash(settings.ADMIN_PASSWORD)
        admin_user = User(
            email=settings.ADMIN_EMAIL,
            username="admin",
            hashed_password=hashed_password,
            full_name="系统管理员",
            is_active=True,
            is_admin=True
        )
        
        db.add(admin_user)
        db.commit()
        print(f"管理员用户创建成功: {settings.ADMIN_EMAIL}")
        print(f"默认密码: {settings.ADMIN_PASSWORD}")
        return True
        
    except Exception as e:
        print(f"创建管理员用户时出错: {str(e)}")
        db.rollback()
        return False
    finally:
        db.close()


def main():
    """主函数"""
    print("=" * 50)
    print("水质数据管理系统 - 数据导入脚本")
    print("=" * 50)
    
    # 创建数据库表
    create_tables()
    
    # 创建管理员用户
    create_admin_user()
    
    # 导入Excel数据
    excel_file = "437条水质数据.xlsx"
    if import_excel_data(excel_file):
        print("\n数据导入成功!")
    else:
        print("\n数据导入失败!")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("数据导入完成!")
    print("=" * 50)


if __name__ == "__main__":
    main() 