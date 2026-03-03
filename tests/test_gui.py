#!/usr/bin/env python3
"""测试 GUI 界面"""

import sys
sys.path.insert(0, '..')

from src.reminder.drink_reminder import DrinkReminder, DrinkReminderGUI

print("="*50)
print("  💧 测试提醒窗口")
print("  即将弹出提醒窗口...")
print("="*50)
print()

# 创建提醒对象
reminder = DrinkReminder()

# 显示 GUI
gui = DrinkReminderGUI(reminder)
gui.show_reminder()

print()
print("窗口已关闭")
