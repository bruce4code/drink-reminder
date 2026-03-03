#!/usr/bin/env python3
"""测试时间范围逻辑"""

start_time = (9, 30)
end_time = (18, 30)

test_times = [
    (9, 0),   # 9:00 - 不提醒（太早）
    (9, 30),  # 9:30 - 提醒 ✓
    (10, 0),  # 10:00 - 提醒 ✓
    (12, 0),  # 12:00 - 提醒 ✓
    (12, 30), # 12:30 - 提醒 ✓
    (18, 0),  # 18:00 - 提醒 ✓
    (18, 30), # 18:30 - 提醒 ✓
    (18, 31), # 18:31 - 不提醒（太晚）
    (19, 0),  # 19:00 - 不提醒（太晚）
]

print("时间范围测试：9:30-18:30")
print("=" * 40)

for hour, minute in test_times:
    current_time = hour * 60 + minute
    start_time_minutes = start_time[0] * 60 + start_time[1]
    end_time_minutes = end_time[0] * 60 + end_time[1]
    
    in_range = start_time_minutes <= current_time <= end_time_minutes
    is_trigger_time = minute in [0, 30]
    should_remind = in_range and is_trigger_time
    
    status = "✓ 提醒" if should_remind else "✗ 不提醒"
    print(f"{hour:02d}:{minute:02d} - {status}")
