# Drink Reminder Development Skill

## Skill Description
This skill provides comprehensive guidelines and workflows for developing and maintaining the Drink Reminder application, a Python-based desktop application that helps users maintain healthy drinking habits through timed reminders.

## Use Cases
- Adding new features to the drink reminder system
- Refactoring existing code following MVC architecture
- Writing and maintaining tests
- Creating documentation
- Debugging and fixing issues
- Updating configuration and dependencies

## Project Overview

### Technology Stack
- **Language**: Python 3.x
- **GUI Framework**: tkinter
- **Data Storage**: JSON
- **Architecture**: MVC (Model-View-Controller)
- **Testing**: unittest / pytest
- **Package Manager**: uv

### Project Structure
```
reminder/
├── main.py                          # Application entry point
├── src/reminder/
│   ├── __init__.py                  # Package initialization
│   ├── config.py                    # Configuration management
│   ├── models/                      # Data model layer
│   │   ├── __init__.py
│   │   └── drink_data.py            # Drink data management
│   ├── views/                       # View layer
│   │   ├── __init__.py
│   │   └── drink_gui.py             # GUI interface
│   ├── controllers/                 # Controller layer
│   │   ├── __init__.py
│   │   └── reminder_controller.py   # Reminder controller
│   └── utils/                       # Utility layer
│       ├── __init__.py
│       └── logger.py                # Logging utility
├── tests/                           # Test files
│   ├── test_reminder.py
│   ├── test_gui.py
│   └── test_time.py
├── ARCHITECTURE.md                  # Architecture documentation
└── README.md                        # Project documentation
```

## Development Guidelines

### Code Style
1. **PEP 8 Compliance**: Follow PEP 8 coding standards
2. **Type Hints**: Use type annotations for all function parameters and return values
3. **Docstrings**: All public functions and classes must have docstrings (Google or NumPy style)
4. **Line Length**: Maximum 88 characters (Black formatting)
5. **Naming**: Use clear, descriptive names for variables, functions, and classes
6. **Constants**: Avoid magic numbers; use constants or configuration items

### Architecture Principles
1. **MVC Pattern**: Maintain clear separation between Model, View, and Controller
2. **Single Responsibility**: Each class/function should have a single, well-defined purpose
3. **Low Coupling**: Minimize dependencies between layers
4. **High Cohesion**: Group related functionality together
5. **Dependency Injection**: Pass dependencies through constructors

### Layer Responsibilities
- **Model Layer** (`models/`): Data management, business logic, persistence
- **View Layer** (`views/`): GUI display, user interaction, event handling
- **Controller Layer** (`controllers/`): Coordination, business flow, main loop
- **Utils Layer** (`utils/`): Common utilities, logging, file operations
- **Config Layer** (`config.py`): Centralized configuration management

### Git Commit Convention
Use **Conventional Commits** format:
```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code formatting
- `refactor`: Code refactoring
- `test`: Test related
- `chore`: Build/tool/dependency updates
- `perf`: Performance optimization
- `ci`: CI/CD configuration
- `build`: Build system
- `revert`: Revert commit

**Scopes**:
- `models`: Data model layer
- `views`: View layer
- `controllers`: Controller layer
- `utils`: Utility layer
- `config`: Configuration management
- `tests`: Test files
- `docs`: Documentation

**Examples**:
- `feat(controllers): Add new reminder controller`
- `fix(models): Fix date parsing error in data loading`
- `docs(readme): Update installation instructions`
- `refactor: Optimize time checking logic`

### Testing Guidelines
1. **Test Coverage**: Target >80% coverage
2. **Test Naming**: Use `test_*.py` format
3. **Test Framework**: Use `unittest` or `pytest`
4. **Independence**: Tests should run independently without external state
5. **Clear Assertions**: Use descriptive assertion messages
6. **Mock External Dependencies**: Mock file I/O, time, etc.

### Documentation Standards
1. **Docstrings**: All public functions/classes require docstrings
2. **Style**: Use Google or NumPy style docstrings
3. **Comments**: Add inline comments for complex logic
4. **README**: Keep README.md updated with latest changes
5. **Architecture**: Maintain ARCHITECTURE.md with design decisions

### Performance Considerations
1. **Main Loop**: Avoid time-consuming operations in the main loop
2. **Async/Threading**: Use async or threading for long-running tasks
3. **Caching**: Implement caching where appropriate
4. **I/O Optimization**: Optimize data loading and saving operations

### Security Best Practices
1. **User Data**: Never commit user data files (drink_data.json) to Git
2. **Hardcoding**: Avoid hardcoding sensitive information
3. **Input Validation**: Validate all user inputs
4. **Error Handling**: Use try-except for file operations and external calls

### Version Management
Follow **Semantic Versioning**:
- Format: MAJOR.MINOR.PATCH
- MAJOR: Incompatible API changes
- MINOR: Backward-compatible feature additions
- PATCH: Backward-compatible bug fixes

## Development Workflow

### Feature Development
1. Create feature branch from `main`
2. Implement changes following architecture guidelines
3. Write/update tests
4. Run tests to ensure all pass
5. Update documentation
6. Commit with conventional commit message
7. Push and create pull request (if applicable)
8. Merge to `main`
9. Delete feature branch

### Bug Fixing
1. Identify the issue
2. Create a test case that reproduces the bug
3. Fix the issue
4. Verify the fix with tests
5. Update documentation if needed
6. Commit with `fix` type
7. Push and merge

### Refactoring
1. Identify code that needs improvement
2. Ensure tests cover the code
3. Refactor following guidelines
4. Run tests to ensure no regressions
5. Commit with `refactor` type

## Common Tasks

### Adding a New Feature
1. Identify which layer(s) need changes
2. Update Model layer if data structure changes
3. Update View layer if UI changes needed
4. Update Controller layer for business logic
5. Write tests for new functionality
6. Update documentation
7. Commit with `feat` type

### Modifying Configuration
1. Update `src/reminder/config.py`
2. Ensure backward compatibility if possible
3. Update tests if needed
4. Document configuration changes
5. Commit with `chore(config)` or `feat(config)`

### Writing Tests
1. Create test file in `tests/` directory
2. Import necessary modules
3. Write test cases with clear names
4. Use setUp/tearDown for setup/cleanup
5. Run tests and ensure they pass
6. Commit with `test` type

### Updating Documentation
1. Update relevant documentation files
2. Ensure accuracy and clarity
3. Add examples if helpful
4. Commit with `docs` type

## Key Constraints and Cautions

### Must Follow
- Always use Conventional Commits format
- Maintain MVC architecture separation
- Write tests for all new features
- Update documentation for significant changes
- Never commit user data files

### Must Avoid
- Breaking MVC architecture principles
- Committing sensitive data
- Hardcoding configuration values
- Skipping tests
- Writing unclear commit messages

### Critical Points
- User data file (drink_data.json) must be in .gitignore
- All public APIs must have type hints and docstrings
- Tests must pass before merging
- Configuration changes should be backward compatible

## Recommended Tools and Commands

### Development
```bash
# Install dependencies
uv sync

# Run the application
python main.py

# Run tests
python -m pytest tests/
# or
python -m unittest discover tests/

# Format code
black src/ tests/

# Lint code
flake8 src/ tests/
```

### Git Operations
```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Stage changes
git add .

# Commit with conventional format
git commit -m "feat(scope): description"

# Push to remote
git push origin feature/your-feature-name

# Merge to main
git checkout main
git merge feature/your-feature-name
```

## Examples

### Example 1: Adding a New Reminder Feature
```
Task: Add ability to customize reminder sound

Steps:
1. Update config.py to add sound_file configuration
2. Modify DrinkGUI.play_sound() to use custom sound
3. Add tests for sound configuration
4. Update README with sound customization instructions
5. Commit: feat(views): Add custom reminder sound support
```

### Example 2: Fixing a Bug
```
Task: Fix date comparison bug in data loading

Steps:
1. Write test case that reproduces the bug
2. Identify issue in drink_data.py
3. Fix date comparison logic
4. Verify fix with tests
5. Commit: fix(models): Fix date comparison in data loading
```

### Example 3: Refactoring
```
Task: Extract time parsing to utility function

Steps:
1. Create parse_time() function in utils/
2. Update controller to use new utility
3. Update tests
4. Commit: refactor: Extract time parsing to utility function
```

## Additional Resources
- [ARCHITECTURE.md](../../ARCHITECTURE.md) - Detailed architecture documentation
- [README.md](../../README.md) - Project documentation
- [Python PEP 8](https://peps.python.org/pep-0008/) - Python style guide
- [Conventional Commits](https://www.conventionalcommits.org/) - Commit specification

## Version History
- v1.0.0 - Initial skill definition
