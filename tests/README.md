# 测试文件说明

本目录包含喝水提醒程序的所有测试文件。

## 测试文件列表

### 1. test_reminder.py
测试核心提醒功能，包括：
- DrinkReminder 类初始化
- 数据加载和保存
- 时间判断逻辑
- 记录喝水功能
- 进度计算
- 鼓励语生成

**运行方式：**
```bash
cd tests
python test_reminder.py
```

### 2. test_gui.py
测试图形界面功能，会弹出提醒窗口。

**运行方式：**
```bash
cd tests
python test_gui.py
```

### 3. test_time.py
测试时间范围判断逻辑，验证不同时间点是否应该触发提醒。

**运行方式：**
```bash
cd tests
python test_time.py
```

## 从项目根目录运行

也可以从项目根目录直接运行测试：

```bash
# Windows
python tests\test_reminder.py
python tests\test_gui.py
python tests\test_time.py

# Linux/Mac
python tests/test_reminder.py
python tests/test_gui.py
python tests/test_time.py
```

## 注意事项

- 测试文件会创建或修改 `drink_log.json` 数据文件
- `test_gui.py` 会弹出 GUI 窗口，需要手动关闭
- 所有测试文件都使用相对路径导入，确保从正确位置运行
