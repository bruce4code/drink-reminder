# 喝水提醒程序源码解析

## 📋 目录
1. [整体架构](#整体架构)
2. [DrinkReminder 类 - 数据管理](#drinkreminder-类)
3. [DrinkReminderGUI 类 - 界面显示](#drinkremindergui-类)
4. [main 函数 - 主循环](#main-函数)
5. [关键技术点](#关键技术点)

---

## 整体架构

程序采用 **MVC 模式**的简化版本：
- **Model (数据层)**：`DrinkReminder` 类 - 管理数据和业务逻辑
- **View (视图层)**：`DrinkReminderGUI` 类 - 负责界面显示
- **Controller (控制层)**：`main()` 函数 - 协调时间检测和界面调用

```
┌─────────────────────────────────────────┐
│           main() 主循环                  │
│  - 时间检测                              │
│  - 触发提醒                              │
└──────────────┬──────────────────────────┘
               │
               ├──────────────┐
               ▼              ▼
    ┌──────────────┐   ┌──────────────┐
    │ DrinkReminder│   │DrinkReminderGUI│
    │  (数据管理)   │◄──│  (界面显示)    │
    └──────────────┘   └──────────────┘
           │
           ▼
    ┌──────────────┐
    │drink_log.json│
    │  (数据存储)   │
    └──────────────┘
```

---

## DrinkReminder 类

### 职责
负责所有数据相关的操作：加载、保存、记录、统计

### 核心属性
```python
def __init__(self):
    self.data_file = "drink_log.json"      # 数据文件路径
    self.start_time = (9, 30)              # 开始时间 9:30
    self.end_time = (18, 30)               # 结束时间 18:30
    self.interval_minutes = 30             # 提醒间隔 30分钟
    self.daily_goal = 8                    # 每日目标 8杯
```

### 方法详解

#### 1. `__init__()` - 初始化
```python
def __init__(self):
    # 设置数据文件路径（确保在项目根目录）
    # 调用 load_data() 加载数据
```
**作用**：创建对象时自动加载数据

---

#### 2. `load_data()` - 加载数据
```python
def load_data(self):
    if os.path.exists(self.data_file):
        # 文件存在 → 读取 JSON
        with open(self.data_file, 'r', encoding='utf-8') as f:
            self.data = json.load(f)
    else:
        # 文件不存在 → 创建空数据
        self.data = self.create_empty_data()
    
    # 检查日期，如果是新的一天 → 重置数据
    today = datetime.now().strftime("%Y-%m-%d")
    if self.data.get("current_date") != today:
        self.reset_today(today)
```
**关键点**：
- 自动检测日期变化
- 跨天自动重置数据

---

#### 3. `create_empty_data()` - 创建空数据结构
```python
def create_empty_data(self):
    today = datetime.now().strftime("%Y-%m-%d")
    return {
        "current_date": today,
        "today": {
            "count": 0,      # 今日喝水次数
            "reminded": 0,   # 今日提醒次数
            "times": []      # 喝水时间列表
        },
        "history": {}        # 历史记录
    }
```
**数据结构**：
```json
{
  "current_date": "2026-03-02",
  "today": {
    "count": 3,
    "reminded": 5,
    "times": ["10:00", "12:30", "15:00"]
  },
  "history": {
    "2026-03-01": {
      "count": 5,
      "reminded": 8,
      "times": [...]
    }
  }
}
```

---

#### 4. `reset_today()` - 重置今日数据
```python
def reset_today(self, today):
    # 1. 保存昨天的数据到 history
    if self.data.get("current_date"):
        old_date = self.data["current_date"]
        self.data["history"][old_date] = self.data["today"].copy()
    
    # 2. 重置今日数据
    self.data["current_date"] = today
    self.data["today"] = {
        "count": 0,
        "reminded": 0,
        "times": []
    }
    
    # 3. 只保留最近7天的历史
    if len(self.data["history"]) > 7:
        dates = sorted(self.data["history"].keys())
        for old_date in dates[:-7]:
            del self.data["history"][old_date]
    
    self.save_data()
```
**作用**：
- 跨天时自动归档昨天数据
- 限制历史记录为 7 天

---

#### 5. `save_data()` - 保存数据
```python
def save_data(self):
    try:
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"保存数据失败: {e}")
```
**特点**：
- `ensure_ascii=False`：支持中文
- `indent=2`：格式化输出，便于阅读

---

#### 6. `record_drink()` - 记录喝水
```python
def record_drink(self):
    current_time = datetime.now().strftime("%H:%M")
    self.data["today"]["count"] += 1
    self.data["today"]["times"].append(current_time)
    self.save_data()
    print(f"[{current_time}] 记录喝水，今日第 {self.data['today']['count']} 次")
```
**流程**：
1. 获取当前时间
2. 增加计数
3. 记录时间
4. 保存到文件

---

#### 7. `record_reminder()` - 记录提醒
```python
def record_reminder(self):
    self.data["today"]["reminded"] += 1
    self.save_data()
```
**作用**：统计提醒次数，用于计算响应率

---

#### 8. `get_progress()` - 获取进度
```python
def get_progress(self):
    count = self.data["today"]["count"]
    return min(count / self.daily_goal * 100, 100)
```
**计算公式**：
```
进度 = (已喝水次数 / 目标次数) × 100%
最大值限制为 100%
```

---

#### 9. `get_encouragement()` - 获取鼓励语
```python
def get_encouragement(self):
    count = self.data["today"]["count"]
    reminded = self.data["today"]["reminded"]
    
    if reminded == 0:
        return "该喝水啦！"
    
    rate = count / reminded if reminded > 0 else 0
    
    if rate >= 0.8:
        messages = ["太棒了！继续保持！💪", ...]
    elif rate >= 0.5:
        messages = ["不错哦！再接再厉！👍", ...]
    else:
        messages = ["喝水太少啦！要多喝水哦~😊", ...]
    
    import random
    return random.choice(messages)
```
**逻辑**：
- 响应率 ≥ 80%：高度鼓励
- 响应率 ≥ 50%：中度鼓励
- 响应率 < 50%：提醒督促

---

## DrinkReminderGUI 类

### 职责
负责所有界面相关的操作：显示窗口、处理用户交互

### 核心属性
```python
def __init__(self, reminder):
    self.reminder = reminder           # DrinkReminder 对象
    self.root = None                   # tkinter 窗口对象
    self.snooze_minutes = 10           # 稍后提醒分钟数
```

### 方法详解

#### 1. `show_reminder()` - 显示提醒窗口
这是最核心的方法，负责创建整个 GUI 界面。

```python
def show_reminder(self):
    # 1. 记录提醒次数
    self.reminder.record_reminder()
    
    # 2. 创建窗口
    self.root = tk.Tk()
    self.root.title("💧 喝水提醒")
    
    # 3. 设置窗口大小和位置（居中显示）
    window_width = 450
    window_height = 380
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
    
    # 4. 窗口置顶
    self.root.attributes('-topmost', True)
    
    # 5. 创建界面元素
    # - 标题
    # - 鼓励语
    # - 当前时间
    # - 统计信息
    # - 进度条
    # - 按钮（已喝水、稍后提醒、关闭）
    
    # 6. 播放提示音
    self._play_sound()
    
    # 7. 启动事件循环
    self.root.mainloop()
```

**界面布局**：
```
┌─────────────────────────────────┐
│      💧 喝水提醒                 │
│                                 │
│   太棒了！继续保持！💪           │
│                                 │
│   当前时间：10:00:00            │
│                                 │
│   今日已喝：3 / 8 杯            │
│                                 │
│   ████████░░░░░░░░ 37.5%       │
│                                 │
│  [✓ 已喝水] [稍后提醒] [关闭]   │
└─────────────────────────────────┘
```

---

#### 2. `_play_sound()` - 播放提示音（跨平台）
```python
def _play_sound(self):
    import platform
    system = platform.system()
    
    try:
        if system == "Windows":
            import winsound
            winsound.Beep(800, 300)  # 800Hz, 300ms
        elif system == "Darwin":  # macOS
            import os
            os.system('afplay /System/Library/Sounds/Glass.aiff')
        elif system == "Linux":
            import os
            os.system('paplay /usr/share/sounds/freedesktop/stereo/bell.oga')
    except Exception as e:
        pass  # 静默失败
```
**跨平台支持**：
- Windows: `winsound.Beep()`
- macOS: `afplay` 系统命令
- Linux: `paplay` 或 `beep`

---

#### 3. `on_drink()` - 点击"已喝水"
```python
def on_drink(self):
    # 1. 记录喝水
    self.reminder.record_drink()
    
    # 2. 显示鼓励消息
    count = self.reminder.data["today"]["count"]
    message = f"太棒了！这是今天第 {count} 杯水！💧"
    
    # 3. 创建提示窗口
    tip_window = tk.Toplevel(self.root)
    # ... 显示消息
    
    # 4. 关闭主窗口
    self.root.destroy()
```
**流程**：
1. 记录数据
2. 弹出鼓励窗口
3. 关闭提醒窗口

---

#### 4. `on_snooze()` - 点击"稍后提醒"
```python
def on_snooze(self):
    self.root.destroy()
    print(f"稍后提醒：{self.snooze_minutes} 分钟后再次提醒")
    
    # 启动延迟提醒
    def delayed_reminder():
        time.sleep(self.snooze_minutes * 60)
        self.show_reminder()
    
    thread = threading.Thread(target=delayed_reminder, daemon=True)
    thread.start()
```
**关键技术**：
- 使用 `threading` 创建后台线程
- `daemon=True`：守护线程，主程序退出时自动结束
- 延迟后重新调用 `show_reminder()`

---

#### 5. `on_close()` - 点击"关闭"
```python
def on_close(self):
    self.root.destroy()
```
**作用**：仅关闭窗口，不记录任何数据

---

## main 函数

### 职责
程序的主控制循环，负责时间检测和触发提醒

```python
def main():
    # 1. 打印启动信息
    print("="*50)
    print("  💧 喝水提醒程序启动")
    print(f"  提醒规则: 9:30-18:30每30分钟提醒一次")
    print("="*50)
    
    # 2. 创建 DrinkReminder 对象
    reminder = DrinkReminder()
    
    # 3. 显示今日统计
    count = reminder.data["today"]["count"]
    reminded = reminder.data["today"]["reminded"]
    print(f"今日已喝水：{count} 次")
    print(f"今日已提醒：{reminded} 次")
    
    # 4. 主循环
    while True:
        try:
            now = datetime.now()
            current_hour = now.hour
            current_minute = now.minute
            
            # 5. 时间判断
            current_time = current_hour * 60 + current_minute
            start_time_minutes = reminder.start_time[0] * 60 + reminder.start_time[1]
            end_time_minutes = reminder.end_time[0] * 60 + reminder.end_time[1]
            
            # 6. 检查是否在提醒时间范围内
            if start_time_minutes <= current_time <= end_time_minutes:
                # 7. 检查是否是整点或半点
                if current_minute == 0 or current_minute == 30:
                    print(f"[{now.strftime('%H:%M:%S')}] 触发提醒")
                    
                    # 8. 显示提醒窗口
                    gui = DrinkReminderGUI(reminder)
                    gui.show_reminder()
                    
                    # 9. 等待到下一分钟，避免重复提醒
                    time.sleep(60)
            
            # 10. 每10秒检查一次
            time.sleep(10)
            
        except KeyboardInterrupt:
            print("\n\n程序已停止")
            break
        except Exception as e:
            print(f"发生错误: {e}")
            time.sleep(60)
```

### 时间判断逻辑详解

```python
# 将时间转换为分钟数便于比较
current_time = 9 * 60 + 45 = 585 分钟  # 9:45
start_time = 9 * 60 + 30 = 570 分钟   # 9:30
end_time = 18 * 60 + 30 = 1110 分钟   # 18:30

# 判断是否在范围内
if 570 <= 585 <= 1110:  # True
    # 判断是否是触发时刻
    if minute in [0, 30]:  # 9:45 → False
        # 触发提醒
```

**为什么每10秒检查一次？**
- 平衡性能和响应速度
- 避免 CPU 占用过高
- 确保不会错过提醒时刻

**为什么触发后 sleep(60)？**
- 避免在同一分钟内重复触发
- 等待到下一分钟再继续检测

---

## 关键技术点

### 1. 数据持久化
```python
# 使用 JSON 格式存储
json.dump(data, f, ensure_ascii=False, indent=2)
```
**优点**：
- 人类可读
- 易于调试
- 跨平台兼容

### 2. 日期自动重置
```python
today = datetime.now().strftime("%Y-%m-%d")
if self.data.get("current_date") != today:
    self.reset_today(today)
```
**触发时机**：每次加载数据时检查

### 3. 跨平台路径处理
```python
if not os.path.isabs(self.data_file):
    root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    self.data_file = os.path.join(root_dir, self.data_file)
```
**作用**：确保数据文件在项目根目录

### 4. GUI 窗口居中
```python
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2
self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
```

### 5. 后台线程延迟提醒
```python
thread = threading.Thread(target=delayed_reminder, daemon=True)
thread.start()
```
**daemon=True**：主程序退出时自动结束线程

### 6. 异常处理
```python
try:
    # 主逻辑
except KeyboardInterrupt:
    # Ctrl+C 优雅退出
except Exception as e:
    # 其他错误继续运行
```

---

## 程序执行流程图

```
启动程序
   ↓
创建 DrinkReminder 对象
   ↓
加载/创建数据文件
   ↓
检查日期（跨天重置）
   ↓
进入主循环 ←─────────┐
   ↓                  │
获取当前时间          │
   ↓                  │
在时间范围内？        │
   ├─ 否 ─→ sleep(10) ┘
   ↓ 是
是整点或半点？
   ├─ 否 ─→ sleep(10) ┘
   ↓ 是
创建 GUI 对象
   ↓
显示提醒窗口
   ↓
用户操作
   ├─ 已喝水 → 记录数据 → 关闭
   ├─ 稍后提醒 → 启动延迟线程 → 关闭
   └─ 关闭 → 直接关闭
   ↓
sleep(60) 避免重复
   ↓
回到主循环 ──────────┘
```

---

## 总结

### 设计优点
1. **职责分离**：数据管理和界面显示分离
2. **数据持久化**：自动保存，跨天归档
3. **跨平台支持**：Windows/macOS/Linux
4. **用户友好**：进度条、鼓励语、声音提示
5. **容错性强**：异常处理完善

### 可改进点
1. 配置文件化：将时间设置移到配置文件
2. 日志系统：添加详细的运行日志
3. 统计分析：添加周报、月报功能
4. 自定义提醒：支持自定义提醒间隔
5. 系统托盘：最小化到系统托盘

---

希望这份解析能帮助你理解整个程序的实现！🎉
