# 💧 喝水提醒程序

一个简单实用的喝水提醒工具，帮助你养成良好的喝水习惯。

[![Python Version](https://img.shields.io/badge/python-3.13+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## ✨ 功能特点

- ⏰ 14:00后每30分钟自动提醒
- 📊 统计每日喝水次数和进度
- 🎯 每日目标：8杯水
- 📈 保留最近7天的历史记录
- 🎨 友好的图形界面
- 💬 智能鼓励语和进度反馈
- 🔔 声音提示（Windows）
- ⏱️ 稍后提醒功能（延迟10分钟）

## 展示
<img width="452" height="412" alt="image" src="https://github.com/user-attachments/assets/a9e59d31-ad2e-46b5-bf62-4426f4d7da6e" />

<img width="302" height="182" alt="image" src="https://github.com/user-attachments/assets/ab115f6e-1496-424d-94b4-6e9f17098721" />



## 📦 安装

### 前置要求

- Python 3.13 或更高版本
- tkinter（通常随 Python 一起安装）

### 方法一：使用 uv（推荐）

```bash
# 安装 uv
pip install uv

# 克隆项目
git clone https://github.com/bruce4code/drink-reminder.git
cd drink-reminder

# 同步依赖
py -3 -m uv sync
```

### 方法二：直接克隆

```bash
git clone https://github.com/bruce4code/drink-reminder.git
cd drink-reminder
```

## 🚀 运行

### Windows

```bash
# 方式1：双击运行
run.bat

# 方式2：命令行运行
python main.py

# 方式3：使用 uv
py -3 -m uv run python main.py
```

### Linux/Mac

```bash
python3 main.py
```

## 📖 使用说明

1. 程序启动后会在后台运行，监控时间
2. 14:00后每30分钟（整点和半点）弹出提醒窗口
3. 提醒窗口显示：
   - 当前时间
   - 今日喝水进度
   - 鼓励语
   - 进度条
4. 操作选项：
   - **已喝水**：记录本次喝水，更新统计
   - **稍后提醒**：10分钟后再次提醒
   - **关闭**：关闭本次提醒
5. 数据自动保存在 `drink_log.json` 文件中

## ⚙️ 配置

可以在 `src/reminder/config.py` 中修改设置：

```python
START_HOUR = 14          # 开始提醒的小时
INTERVAL_MINUTES = 30    # 提醒间隔（分钟）
SNOOZE_MINUTES = 10      # 稍后提醒的分钟数
DAILY_GOAL = 8           # 每日目标喝水次数
HISTORY_DAYS = 7         # 保留历史记录天数
```

## 📁 项目结构

```
reminder/
├── src/
│   └── reminder/
│       ├── __init__.py          # 包初始化
│       ├── config.py            # 配置文件
│       └── drink_reminder.py    # 核心功能代码
├── main.py                      # 程序入口
├── run.bat                      # Windows快速启动脚本
├── drink_log.json              # 数据存储
├── pyproject.toml              # 项目配置
├── README.md                   # 项目说明
├── LICENSE                     # MIT许可证
└── .gitignore                  # Git忽略配置
```

## 💾 数据说明

程序会自动创建 `drink_log.json` 文件记录：
- 当前日期的喝水次数和时间
- 最近7天的历史记录
- 提醒次数统计

数据格式示例：
```json
{
  "current_date": "2026-02-28",
  "today": {
    "count": 4,
    "reminded": 5,
    "times": ["14:01", "14:30", "15:01", "15:42"]
  },
  "history": {}
}
```

## 🛠️ 技术栈

- Python 3.13+
- tkinter（GUI界面）
- json（数据存储）
- threading（后台任务）

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📝 开发

如果你想参与开发或修改代码：

```bash
# 克隆项目
git clone https://github.com/bruce4code/drink-reminder.git
cd drink-reminder

# 创建虚拟环境（可选）
py -3 -m uv venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# 运行程序
python main.py
```

## 📄 许可

本项目采用 [MIT License](LICENSE) 开源许可证。

## 🙏 致谢

感谢所有为健康生活习惯努力的人们！

---

如果这个项目对你有帮助，请给个 ⭐️ Star 支持一下！
