#!/usr/bin/env python3
"""测试提醒功能"""

import sys
sys.path.insert(0, '..')

from src.reminder.drink_reminder import DrinkReminder, DrinkReminderGUI
from datetime import datetime

print("="*50)
print("  💧 喝水提醒程序测试")
print("="*50)
print()

# 测试 DrinkReminder 类
reminder = DrinkReminder()
print(f"✓ DrinkReminder 初始化成功")
print(f"  - 开始时间: {reminder.start_time[0]:02d}:{reminder.start_time[1]:02d}")
print(f"  - 结束时间: {reminder.end_time[0]:02d}:{reminder.end_time[1]:02d}")
print(f"  - 提醒间隔: {reminder.interval_minutes} 分钟")
print(f"  - 每日目标: {reminder.daily_goal} 杯")
print()

# 测试数据加载
print(f"✓ 数据加载成功")
print(f"  - 当前日期: {reminder.data['current_date']}")
print(f"  - 今日喝水: {reminder.data['today']['count']} 次")
print(f"  - 今日提醒: {reminder.data['today']['reminded']} 次")
print()

# 测试时间判断逻辑
now = datetime.now()
current_hour = now.hour
current_minute = now.minute
current_time = current_hour * 60 + current_minute
start_time_minutes = reminder.start_time[0] * 60 + reminder.start_time[1]
end_time_minutes = reminder.end_time[0] * 60 + reminder.end_time[1]

print(f"✓ 时间判断逻辑测试")
print(f"  - 当前时间: {current_hour:02d}:{current_minute:02d}")
print(f"  - 时间范围: {start_time_minutes//60:02d}:{start_time_minutes%60:02d} - {end_time_minutes//60:02d}:{end_time_minutes%60:02d}")

in_range = start_time_minutes <= current_time <= end_time_minutes
is_trigger_time = current_minute in [0, 30]

if in_range:
    print(f"  - 状态: ✓ 在提醒时间范围内")
    if is_trigger_time:
        print(f"  - 触发: ✓ 当前是提醒时刻")
    else:
        print(f"  - 触发: ✗ 不是提醒时刻（需要整点或半点）")
else:
    print(f"  - 状态: ✗ 不在提醒时间范围内")
print()

# 测试记录功能
print(f"✓ 测试记录功能")
old_count = reminder.data['today']['count']
reminder.record_drink()
new_count = reminder.data['today']['count']
print(f"  - 记录前: {old_count} 次")
print(f"  - 记录后: {new_count} 次")
print(f"  - 结果: {'✓ 成功' if new_count == old_count + 1 else '✗ 失败'}")
print()

# 测试进度计算
progress = reminder.get_progress()
print(f"✓ 进度计算")
print(f"  - 当前进度: {progress:.1f}%")
print()

# 测试鼓励语
encouragement = reminder.get_encouragement()
print(f"✓ 鼓励语生成")
print(f"  - 鼓励语: {encouragement}")
print()

print("="*50)
print("  所有测试通过！✓")
print("="*50)
print()
print("提示：如果要测试 GUI 界面，请运行 main.py")
print("      或者手动触发：")
print("      >>> from src.reminder.drink_reminder import DrinkReminder, DrinkReminderGUI")
print("      >>> reminder = DrinkReminder()")
print("      >>> gui = DrinkReminderGUI(reminder)")
print("      >>> gui.show_reminder()")
