# Drink Reminder Development Skill

这是一个为 TRAE IDE AI Agent 设计的技能配置文件，用于指导 AI 在喝水提醒项目中进行开发工作。

## 📁 目录结构

```
skills/drink-reminder-development/
├── SKILL.md              # 主技能文件（AI Agent 读取）
├── README.md             # 本文件
└── examples/             # 代码和开发示例
    ├── commit-messages.md    # Git 提交信息示例
    ├── code-style.md         # 代码风格示例
    └── workflow.md           # 开发工作流示例
```

## 🚀 使用方法

### 在 TRAE IDE 中使用

1. **自动识别**：TRAE IDE 会自动识别项目中的 `skills/` 目录
2. **加载技能**：AI Agent 会读取 `SKILL.md` 文件并应用其中的规则
3. **智能辅助**：AI 会根据技能配置提供符合项目规范的代码建议

### 技能内容

`SKILL.md` 文件包含以下内容：

- **项目概述**：喝水提醒程序的基本信息和目标
- **技术栈**：Python、Tkinter、JSON 等技术选型
- **MVC 架构规范**：Model、View、Controller 各层的职责和实现规范
- **Git 提交规范**：Conventional Commits 规范和提交信息格式
- **代码风格规范**：命名约定、类型提示、文档字符串等
- **测试规范**：测试文件组织、测试命名、覆盖率要求
- **开发工作流**：分支策略、代码审查流程等

## 📚 示例文件

### commit-messages.md

包含各种类型的 Git 提交信息示例：
- `feat:` - 新功能
- `fix:` - Bug 修复
- `docs:` - 文档更新
- `refactor:` - 代码重构
- `test:` - 测试相关
- `chore:` - 构建/工具相关
- `perf:` - 性能优化
- `ci:` - CI/CD 相关
- `build:` - 构建相关
- `revert:` - 回滚提交

### code-style.md

包含代码风格示例：
- 函数定义（类型提示 + 文档字符串）
- 类定义（类型提示 + 文档字符串）
- MVC 架构各层实现示例
- 测试代码示例
- 配置文件示例
- 导入顺序示例
- 错误处理示例
- 日志记录示例

### workflow.md

包含开发工作流示例：
- 功能开发流程
- Bug 修复流程
- 代码重构流程
- 文档更新流程
- 发布流程
- 代码审查流程
- 紧急修复流程

## 🎯 技能的优势

### 1. 一致性
- 确保所有 AI 生成的代码遵循统一的风格和规范
- 保持提交信息格式一致
- 统一项目架构和设计模式

### 2. 效率提升
- AI Agent 无需重复解释项目规范
- 快速生成符合项目要求的代码
- 减少代码审查和修改时间

### 3. 质量保证
- 强制执行代码质量标准
- 确保类型提示和文档字符串完整
- 遵循最佳实践和安全规范

### 4. 知识传承
- 记录项目特定的规范和约定
- 新团队成员可以快速了解项目要求
- 降低项目维护成本

## 🔧 自定义技能

### 修改 SKILL.md

根据项目需求修改 `SKILL.md` 文件：

```markdown
# 添加新的技术栈
## 技术栈
- Python 3.9+
- Tkinter
- JSON
- [新增技术]  # 添加新技术

# 添加新的代码规范
## 代码风格规范
- 使用 4 空格缩进
- [新增规范]  # 添加新规范
```

### 添加新的示例

在 `examples/` 目录下添加新的示例文件：

```bash
# 创建新的示例文件
touch examples/new-topic.md
```

## 📖 相关资源

- [TRAE IDE Skills 文档](https://docs.trae.ai/ide/skills)
- [Conventional Commits 规范](https://www.conventionalcommits.org/)
- [Python PEP 8 风格指南](https://peps.python.org/pep-0008/)
- [Python 类型提示文档](https://docs.python.org/3/library/typing.html)

## 🤝 贡献

如果需要更新技能配置，请：

1. 修改 `SKILL.md` 或示例文件
2. 更新 `README.md` 中的相关说明
3. 提交 PR 并说明修改原因

## 📝 版本历史

### v1.0.0 (2024-01-15)
- 初始版本
- 包含完整的 MVC 架构规范
- 添加 Git 提交规范
- 添加代码风格和测试规范
- 提供丰富的代码和工作流示例

## 📧 联系方式

如有问题或建议，请通过以下方式联系：
- 提交 Issue
- 发起 Pull Request
- 联系项目维护者

---

**注意**：此技能文件专门为喝水提醒项目设计，其他项目使用时需要根据具体需求进行调整。
