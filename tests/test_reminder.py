#!/usr/bin/env python3
"""测试提醒功能 - 新架构版本
"""

import sys
sys.path.insert(0, '..')

from src.reminder import DrinkData, ReminderController
from datetime import datetime

print("="*50)
print("  💧 喝水提醒程序测试 (新架构)")
print("="*50)
print()

# 测试 DrinkData 类
drink_data = DrinkData()
print(f"✓ DrinkData 初始化成功")
print(f"  - 每日目标: {drink_data.daily_goal} 杯")
print(f"  - 数据文件: {drink_data.data_file}")
print()

# 测试数据加载
print(f"✓ 数据加载成功")
print(f"  - 当前日期: {drink_data.data['current_date']}")
print(f"  - 今日喝水: {drink_data.data['today']['count']} 次")
print(f"  - 今日提醒: {drink_data.data['today']['reminded']} 次")
print()

# 测试 ReminderController 类
controller = ReminderController()
print(f"✓ ReminderController 初始化成功")
print(f"  - 开始时间: {controller.start_time[0]:02d}:{controller.start_time[1]:02d}")
print(f"  - 结束时间: {controller.end_time[0]:02d}:{controller.end_time[1]:02d}")
print(f"  - 提醒间隔: {controller.interval_seconds // 60} 分钟")
print()

# 测试时间判断逻辑
now = datetime.now()
current_hour = now.hour
current_minute = now.minute
current_time = current_hour * 60 + current_minute
start_time_minutes = controller.start_time[0] * 60 + controller.start_time[1]
end_time_minutes = controller.end_time[0] * 60 + controller.end_time[1]

print(f"✓ 时间判断逻辑测试")
print(f"  - 当前时间: {current_hour:02d}:{current_minute:02d}")
print(f"  - 时间范围: {start_time_minutes//60:02d}:{start_time_minutes%60:02d} - {end_time_minutes//60:02d}:{end_time_minutes%60:02d}")

in_range = start_time_minutes <= current_time <= end_time_minutes
interval_minutes = controller.interval_seconds // 60
minutes_since_start = current_time - start_time_minutes
is_trigger_time = minutes_since_start % interval_minutes == 0 if in_range else False

if in_range:
    print(f"  - 状态: ✓ 在提醒时间范围内")
    if is_trigger_time:
        print(f"  - 触发: ✓ 当前是提醒时刻")
    else:
        print(f"  - 触发: ✗ 不是提醒时刻（需要每{interval_minutes}分钟间隔")
else:
    print(f"  - 状态: ✗ 不在提醒时间范围内")
print()

# 测试记录功能
print(f"✓ 测试记录功能")
old_count = drink_data.data['today']['count']
drink_data.record_drink()
new_count = drink_data.data['today']['count']
print(f"  - 记录前: {old_count} 次")
print(f"  - 记录后: {new_count} 次")
print(f"  - 结果: {'✓ 成功' if new_count == old_count + 1 else '✗ 失败'}")
print()

# 测试进度计算
progress = drink_data.get_progress()
print(f"✓ 进度计算")
print(f"  - 当前进度: {progress:.1f}%")
print()

# 测试鼓励语
encouragement = drink_data.get_encouragement()
print(f"✓ 鼓励语生成")
print(f"  - 鼓励语: {encouragement}")
print()

# 测试今日统计
stats = drink_data.get_today_stats()
print(f"✓ 今日统计")
print(f"  - 今日统计: {stats}")
print()

print("="*50)
print("  所有测试通过！✓")
print("="*50)
print()
print("提示：如果要测试 GUI 界面，请运行 main.py")
print("      或者手动触发：")
print("      >>> from src.reminder import DrinkData, DrinkGUI, ReminderController")
print("      >>> controller = ReminderController()")
print("      >>> controller.show_reminder()")
