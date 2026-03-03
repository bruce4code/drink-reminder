# 喝水提醒程序 - 架构设计文档

## 概述

喝水提醒程序采用 **MVC (Model-View-Controller)** 架构设计，实现了数据层、视图层和控制层的清晰分离，提高了代码的可维护性、可扩展性和可测试性。

## 目录结构

```
reminder/
├── main.py                          # 程序主入口
├── src/
│   └── reminder/
│       ├── __init__.py              # 包初始化文件（导出主要类和配置）
│       ├── config.py                # 配置管理
│       ├── models/                  # 数据模型层
│       │   ├── __init__.py
│       │   └── drink_data.py        # 喝水数据管理
│       ├── views/                   # 视图层
│       │   ├── __init__.py
│       │   └── drink_gui.py         # GUI 界面
│       ├── controllers/             # 控制器层
│       │   ├── __init__.py
│       │   └── reminder_controller.py  # 提醒控制器
│       └── utils/                   # 工具层
│           ├── __init__.py
│           └── logger.py            # 日志工具
├── tests/
│   ├── test_reminder.py             # 提醒功能测试
│   ├── test_gui.py                  # GUI 测试
│   └── test_time.py                 # 时间逻辑测试
└── drink_data.json                  # 数据文件（运行时生成）
```

## 架构层次

### 1. Model 层（数据模型层）

**文件**: `src/reminder/models/drink_data.py`

**职责**:
- 数据持久化管理（加载/保存 JSON 文件）
- 业务逻辑处理（喝水记录、进度计算、鼓励语生成）
- 数据操作（日期重置、历史记录管理）

**主要类**: `DrinkData`

**核心方法**:
- `load_data()`: 加载数据
- `save_data()`: 保存数据
- `reset_today()`: 重置今日数据
- `record_drink()`: 记录喝水
- `record_reminder()`: 记录提醒
- `get_progress()`: 获取进度百分比
- `get_encouragement()`: 获取鼓励语
- `get_today_stats()`: 获取今日统计
- `get_history()`: 获取历史记录

### 2. View 层（视图层）

**文件**: `src/reminder/views/drink_gui.py`

**职责**:
- 界面显示和交互
- 用户事件处理
- 跨平台提示音播放

**主要类**: `DrinkGUI`

**核心方法**:
- `show_reminder()`: 显示提醒窗口
- `play_sound()`: 播放提示音
- `on_drink()`: 处理喝水按钮点击
- `on_snooze()`: 处理稍后提醒
- `on_close()`: 处理关闭按钮

### 3. Controller 层（控制器层）

**文件**: `src/reminder/controllers/reminder_controller.py`

**职责**:
- 协调 Model 和 View
- 时间检测和业务逻辑
- 主循环控制

**主要类**: `ReminderController`

**核心方法**:
- `__init__()`: 初始化控制器
- `record_drink()`: 记录喝水
- `record_reminder()`: 记录提醒
- `is_reminder_time()`: 判断是否是提醒时间
- `show_reminder()`: 显示提醒窗口
- `run()`: 运行主循环

### 4. Utils 层（工具层）

**文件**: `src/reminder/utils/logger.py`

**职责**:
- 提供统一的日志记录功能
- 支持控制台和文件输出

**主要函数**: `get_logger()`

### 5. Config 层（配置层）

**文件**: `src/reminder/config.py`

**职责**:
- 集中管理所有配置项
- 便于配置修改和维护

**主要配置项**:
- 提醒设置：开始/结束时间、间隔、稍后提醒时间
- 目标设置：每日喝水次数
- 数据设置：数据文件名、历史记录保留天数
- 日志设置：日志级别、日志文件名

## 数据流程

### 正常提醒流程

```
1. main.py 启动程序
   ↓
2. ReminderController 初始化
   ↓
3. DrinkData 加载数据
   ↓
4. 主循环开始
   ↓
5. is_reminder_time() 检测时间
   ↓
6. 如果是提醒时间 → show_reminder()
   ↓
7. DrinkGUI 显示界面
   ↓
8. 用户交互（喝水/稍后/关闭）
   ↓
9. 调用相应方法更新 DrinkData
   ↓
10. 回到主循环继续
```

## 设计优点

1. **职责分离清晰**: 每层只负责自己的功能，降低了耦合度
2. **易于维护**: 修改某一层不会影响其他层
3. **易于扩展**: 添加新功能只需在相应层添加代码
4. **易于测试**: 各层可以独立进行单元测试
5. **配置集中化**: 所有配置在一个文件中，便于管理
6. **日志系统**: 统一的日志记录，便于问题排查

## 使用示例

### 基本使用

```python
from src.reminder import ReminderController

# 创建控制器
controller = ReminderController()

# 运行程序
controller.run()
```

### 手动触发提醒

```python
from src.reminder import ReminderController

controller = ReminderController()
controller.show_reminder()
```

### 使用数据模型

```python
from src.reminder import DrinkData

data = DrinkData()
data.record_drink()
progress = data.get_progress()
print(f"当前进度: {progress:.1f}%")
```

## 版本历史

- **v0.1.0**: 初始版本，单文件架构
- **v0.2.0**: 添加了一些功能，仍然是单文件
- **v0.3.0**: 重构为 MVC 架构，代码结构优化

## 未来改进方向

1. **添加设置界面**: 允许用户在 GUI 中修改配置
2. **统计分析功能**: 提供更丰富的数据统计和图表
3. **系统托盘集成**: 后台运行，托盘图标显示
4. **通知增强**: 支持系统通知
5. **数据同步**: 支持云端数据同步
