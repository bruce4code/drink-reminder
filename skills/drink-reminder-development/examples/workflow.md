# Development Workflow Examples

## Feature Development Workflow

### 1. Create Feature Branch
```bash
git checkout -b feat/custom-sound-support
```

### 2. Implement the Feature

#### Step 1: Update Model Layer
```python
# models/drink_data.py
class DrinkData:
    def __init__(self, data_file: str) -> None:
        # ... existing code ...
        self.sound_enabled: bool = True
        self.sound_file: str = "default.mp3"

    def set_sound(self, enabled: bool, file_path: str = "") -> None:
        """Configure sound settings.

        Args:
            enabled: Whether sound is enabled.
            file_path: Path to custom sound file.
        """
        self.sound_enabled = enabled
        if file_path:
            self.sound_file = file_path
        self._save_data()
```

#### Step 2: Update View Layer
```python
# views/drink_gui.py
class DrinkGUI:
    def __init__(self, on_drink: Callable[[], None]) -> None:
        # ... existing code ...
        self.sound_player = SoundPlayer()

    def play_reminder_sound(self) -> None:
        """Play reminder sound if enabled."""
        if self.model.sound_enabled:
            self.sound_player.play(self.model.sound_file)
```

#### Step 3: Update Controller Layer
```python
# controllers/reminder_controller.py
class ReminderController:
    def configure_sound(self, enabled: bool, file_path: str = "") -> None:
        """Configure reminder sound.

        Args:
            enabled: Whether to enable sound.
            file_path: Custom sound file path.
        """
        self.model.set_sound(enabled, file_path)
        logger.info(f"Sound configuration updated: enabled={enabled}")
```

### 3. Write Tests
```python
# tests/test_sound.py
import unittest
from models.drink_data import DrinkData

class TestSoundConfiguration(unittest.TestCase):
    def test_sound_toggle(self) -> None:
        """Test enabling and disabling sound."""
        data = DrinkData("test_data.json")
        data.set_sound(True)
        self.assertTrue(data.sound_enabled)
        
        data.set_sound(False)
        self.assertFalse(data.sound_enabled)

    def test_custom_sound_file(self) -> None:
        """Test setting custom sound file."""
        data = DrinkData("test_data.json")
        data.set_sound(True, "custom.mp3")
        self.assertEqual(data.sound_file, "custom.mp3")
```

### 4. Run Tests
```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_sound.py

# Run with coverage
python -m pytest tests/ --cov=src --cov-report=html
```

### 5. Commit Changes
```bash
# Stage changes
git add models/drink_data.py
git add views/drink_gui.py
git add controllers/reminder_controller.py
git add tests/test_sound.py

# Commit with conventional commit message
git commit -m "feat(models): Add custom sound support

- Add sound_enabled and sound_file to DrinkData
- Implement set_sound() method for configuration
- Add SoundPlayer integration in view layer
- Add sound configuration in controller layer
- Add unit tests for sound functionality

Closes #42"
```

### 6. Push and Create Pull Request
```bash
git push origin feat/custom-sound-support
```

## Bug Fix Workflow

### 1. Identify the Bug
```python
# Bug: Date comparison fails when loading data
# File: models/drink_data.py
def get_today_count(self) -> int:
    today = datetime.now().strftime("%Y-%m-%d")
    # Bug: This fails if today doesn't exist in data
    return self.data[today]["count"]  # KeyError!
```

### 2. Write Failing Test
```python
# tests/test_bug_fix.py
def test_get_today_count_new_day(self) -> None:
    """Test getting count for a new day."""
    data = DrinkData("test_data.json")
    # First access should return 0, not raise KeyError
    count = data.get_today_count()
    self.assertEqual(count, 0)
```

### 3. Fix the Bug
```python
# models/drink_data.py
def get_today_count(self) -> int:
    today = datetime.now().strftime("%Y-%m-%d")
    if today not in self.data:
        self.data[today] = {"count": 0, "times": []}
    return self.data[today]["count"]
```

### 4. Run Tests
```bash
python -m pytest tests/test_bug_fix.py -v
```

### 5. Commit the Fix
```bash
git add models/drink_data.py
git add tests/test_bug_fix.py
git commit -m "fix(models): Fix KeyError when accessing new day

- Add check for today's date in data
- Initialize new day with default values
- Add test case for new day scenario

Fixes #45"
```

## Refactoring Workflow

### 1. Identify Code to Refactor
```python
# Before: Duplicate time parsing logic
def is_reminder_time(self, current_time: datetime) -> bool:
    start = datetime.strptime(self.start_time, "%H:%M").time()
    end = datetime.strptime(self.end_time, "%H:%M").time()
    return start <= current_time.time() <= end

def is_active_period(self, current_time: datetime) -> bool:
    start = datetime.strptime(self.start_time, "%H:%M").time()
    end = datetime.strptime(self.end_time, "%H:%M").time()
    return start <= current_time.time() <= end
```

### 2. Extract to Utility Function
```python
# utils/time_helpers.py
from datetime import datetime, time

def parse_time(time_str: str) -> time:
    """Parse time string to time object.

    Args:
        time_str: Time string in HH:MM format.

    Returns:
        Parsed time object.
    """
    return datetime.strptime(time_str, "%H:%M").time()

def is_time_in_range(
    check_time: time,
    start_time: time,
    end_time: time
) -> bool:
    """Check if time is within range.

    Args:
        check_time: Time to check.
        start_time: Start of range.
        end_time: End of range.

    Returns:
        True if time is in range, False otherwise.
    """
    return start_time <= check_time <= end_time
```

### 3. Update Code to Use Utility
```python
# After: Clean and DRY
from utils.time_helpers import parse_time, is_time_in_range

class ReminderController:
    def __init__(self) -> None:
        self._start_time = parse_time(self.start_time)
        self._end_time = parse_time(self.end_time)

    def is_reminder_time(self, current_time: datetime) -> bool:
        return is_time_in_range(
            current_time.time(),
            self._start_time,
            self._end_time
        )

    def is_active_period(self, current_time: datetime) -> bool:
        return is_time_in_range(
            current_time.time(),
            self._start_time,
            self._end_time
        )
```

### 4. Run Tests to Ensure No Regressions
```bash
python -m pytest tests/ -v
```

### 5. Commit Refactoring
```bash
git add utils/time_helpers.py
git add controllers/reminder_controller.py
git commit -m "refactor: Extract time parsing to utility functions

- Create utils/time_helpers.py with time utilities
- Extract parse_time() function for time string parsing
- Extract is_time_in_range() for time range checking
- Update ReminderController to use utility functions
- Eliminate code duplication

Improves code maintainability and testability"
```

## Documentation Update Workflow

### 1. Update README.md
```markdown
## Features

- Customizable reminder intervals
- Sound notifications (optional)
- Daily progress tracking
- Weekly statistics
- Custom reminder sounds

## Configuration

Edit `config.py` to customize:
- Reminder start/end times
- Interval between reminders
- Daily goal
- Sound settings
```

### 2. Update API Documentation
```python
def record_drink(self) -> None:
    """Record a drink event.

    This method increments the drink count for the current day
    and records the timestamp. The data is automatically saved
    to the data file.

    Example:
        >>> data = DrinkData("drink_data.json")
        >>> data.record_drink()
        >>> data.get_today_count()
        1

    Note:
        This method automatically creates a new entry for the
        current day if it doesn't exist.
    """
```

### 3. Commit Documentation
```bash
git add README.md
git add docs/api.md
git commit -m "docs: Update README and API documentation

- Add sound notification feature to README
- Update configuration section
- Add docstring examples for record_drink()
- Improve API documentation clarity"
```

## Release Workflow

### 1. Update Version
```python
# src/reminder/__init__.py
__version__ = "0.4.0"
```

### 2. Update CHANGELOG.md
```markdown
## [0.4.0] - 2024-01-15

### Added
- Custom sound support (#42)
- Sound configuration in settings
- Weekly statistics view

### Fixed
- KeyError when accessing new day (#45)
- Window positioning on multi-monitor setups

### Changed
- Extracted time parsing to utility functions
- Improved error handling in data loading

### Deprecated
- Old sound configuration method (will be removed in 0.5.0)
```

### 3. Tag Release
```bash
git tag -a v0.4.0 -m "Release version 0.4.0"
git push origin v0.4.0
```

### 4. Commit Release
```bash
git add src/reminder/__init__.py
git add CHANGELOG.md
git commit -m "chore: Release version 0.4.0

- Update version to 0.4.0
- Update CHANGELOG with release notes
- Tag release as v0.4.0"
```

## Code Review Workflow

### 1. Review Checklist
- [ ] Code follows project style guidelines
- [ ] All tests pass
- [ ] New tests added for new functionality
- [ ] Documentation updated
- [ ] No security vulnerabilities
- [ ] Performance impact considered
- [ ] Error handling implemented
- [ ] Logging added where appropriate

### 2. Review Comments
```markdown
## General Feedback

The implementation looks good overall. I have a few suggestions:

1. **Type Hints**: Add return type hints to all public methods
2. **Error Handling**: Add try-except for file operations
3. **Testing**: Add edge case tests for empty data

## Specific Comments

Line 45: Consider using `pathlib.Path` instead of string paths
Line 78: This could be extracted to a separate method
Line 120: Add docstring explaining the algorithm

## Approval

Once these items are addressed, I'm happy to approve this PR.
```

## Hotfix Workflow

### 1. Create Hotfix Branch from Main
```bash
git checkout main
git pull origin main
git checkout -b hotfix/critical-bug-fix
```

### 2. Apply Fix
```python
# Quick fix for critical bug
def get_today_count(self) -> int:
    today = datetime.now().strftime("%Y-%m-%d")
    return self.data.get(today, {}).get("count", 0)
```

### 3. Test and Commit
```bash
python -m pytest tests/ -v
git add models/drink_data.py
git commit -m "fix: Critical bug in get_today_count

Fix KeyError when accessing data for new day.
This is a critical fix affecting all users.

Hotfix for #45"
```

### 4. Merge to Main and Develop
```bash
git checkout main
git merge hotfix/critical-bug-fix
git push origin main

git checkout develop
git merge hotfix/critical-bug-fix
git push origin develop

git branch -d hotfix/critical-bug-fix
```
