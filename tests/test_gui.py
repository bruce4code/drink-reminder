#!/usr/bin/env python3
"""测试 GUI 界面 - 新架构版本
"""

import sys
sys.path.insert(0, '..')

from src.reminder import ReminderController

print("="*50)
print("  💧 测试提醒窗口 (新架构)")
print("  即将弹出提醒窗口...")
print("="*50)
print()

# 创建控制器对象
controller = ReminderController()

# 显示 GUI
controller.show_reminder()

print()
print("窗口已关闭")
