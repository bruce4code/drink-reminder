# Code Style Examples

## Function with Type Hints and Docstring

```python
from typing import Optional, Dict, List
from datetime import datetime

def calculate_progress(current: int, goal: int) -> float:
    """Calculate the progress percentage.

    Args:
        current: Current count value.
        goal: Target goal value.

    Returns:
        Progress percentage as a float between 0 and 100.

    Raises:
        ValueError: If goal is zero or negative.
    """
    if goal <= 0:
        raise ValueError("Goal must be positive")
    
    if current >= goal:
        return 100.0
    
    return (current / goal) * 100.0
```

## Class with Type Hints and Docstring

```python
class ReminderManager:
    """Manages reminder scheduling and tracking.

    This class handles the core logic for scheduling and tracking
    drink reminders, including time checking and reminder history.

    Attributes:
        start_time: Start time for reminders (HH:MM format).
        end_time: End time for reminders (HH:MM format).
        interval_minutes: Interval between reminders in minutes.
        last_reminder_time: Timestamp of the last reminder.
    """

    def __init__(
        self,
        start_time: str,
        end_time: str,
        interval_minutes: int
    ) -> None:
        """Initialize the ReminderManager.

        Args:
            start_time: Start time in HH:MM format.
            end_time: End time in HH:MM format.
            interval_minutes: Interval between reminders in minutes.
        """
        self.start_time = start_time
        self.end_time = end_time
        self.interval_minutes = interval_minutes
        self.last_reminder_time: Optional[datetime] = None

    def is_reminder_time(self, current_time: datetime) -> bool:
        """Check if it's time for a reminder.

        Args:
            current_time: Current datetime to check.

        Returns:
            True if it's time for a reminder, False otherwise.
        """
        # Implementation here
        pass
```

## MVC Architecture Example

### Model Layer
```python
# models/drink_data.py
from typing import Dict, List
from datetime import datetime

class DrinkData:
    """Manages drink data persistence and business logic."""

    def __init__(self, data_file: str) -> None:
        """Initialize DrinkData with data file path.

        Args:
            data_file: Path to the JSON data file.
        """
        self.data_file = data_file
        self.data: Dict = self._load_data()

    def record_drink(self) -> None:
        """Record a drink event."""
        today = datetime.now().strftime("%Y-%m-%d")
        if today not in self.data:
            self.data[today] = {"count": 0, "times": []}
        
        self.data[today]["count"] += 1
        self.data[today]["times"].append(
            datetime.now().strftime("%H:%M")
        )
        self._save_data()

    def _load_data(self) -> Dict:
        """Load data from file.

        Returns:
            Dictionary containing drink data.
        """
        # Implementation
        pass

    def _save_data(self) -> None:
        """Save data to file."""
        # Implementation
        pass
```

### View Layer
```python
# views/drink_gui.py
import tkinter as tk
from typing import Callable, Optional

class DrinkGUI:
    """GUI interface for drink reminders."""

    def __init__(self, on_drink: Callable[[], None]) -> None:
        """Initialize DrinkGUI with callback.

        Args:
            on_drink: Callback function when user drinks.
        """
        self.on_drink = on_drink
        self.window: Optional[tk.Tk] = None

    def show_reminder(self) -> None:
        """Display reminder window."""
        if self.window is None:
            self.window = tk.Tk()
            self.window.title("喝水提醒")
            
            # Create UI elements
            label = tk.Label(
                self.window,
                text="该喝水啦！",
                font=("Arial", 24)
            )
            label.pack(pady=20)
            
            button = tk.Button(
                self.window,
                text="我喝了",
                command=self._on_drink_clicked
            )
            button.pack(pady=10)

    def _on_drink_clicked(self) -> None:
        """Handle drink button click."""
        self.on_drink()
        if self.window:
            self.window.destroy()
            self.window = None
```

### Controller Layer
```python
# controllers/reminder_controller.py
from models.drink_data import DrinkData
from views.drink_gui import DrinkGUI

class ReminderController:
    """Coordinates model and view for reminder functionality."""

    def __init__(self) -> None:
        """Initialize ReminderController."""
        self.model = DrinkData("drink_data.json")
        self.view = DrinkGUI(on_drink=self.record_drink)

    def record_drink(self) -> None:
        """Record a drink event."""
        self.model.record_drink()

    def show_reminder(self) -> None:
        """Show reminder window."""
        self.view.show_reminder()

    def run(self) -> None:
        """Run the main reminder loop."""
        # Implementation
        pass
```

## Testing Example

```python
import unittest
from datetime import datetime
from models.drink_data import DrinkData

class TestDrinkData(unittest.TestCase):
    """Test cases for DrinkData class."""

    def setUp(self) -> None:
        """Set up test fixtures."""
        self.data_file = "test_data.json"
        self.drink_data = DrinkData(self.data_file)

    def tearDown(self) -> None:
        """Clean up test fixtures."""
        import os
        if os.path.exists(self.data_file):
            os.remove(self.data_file)

    def test_record_drink(self) -> None:
        """Test recording a drink event."""
        initial_count = self.drink_data.get_today_count()
        self.drink_data.record_drink()
        final_count = self.drink_data.get_today_count()
        
        self.assertEqual(final_count, initial_count + 1)

    def test_get_progress(self) -> None:
        """Test progress calculation."""
        self.drink_data.record_drink()
        self.drink_data.record_drink()
        
        progress = self.drink_data.get_progress()
        self.assertGreater(progress, 0)
        self.assertLessEqual(progress, 100)

if __name__ == "__main__":
    unittest.main()
```

## Configuration Example

```python
# config.py
from typing import Final

# Reminder settings
REMINDER_START_TIME: Final[str] = "09:00"
REMINDER_END_TIME: Final[str] = "21:00"
REMINDER_INTERVAL: Final[int] = 60  # minutes
SNOOZE_TIME: Final[int] = 5  # minutes

# Goal settings
DAILY_GOAL: Final[int] = 8  # glasses

# Data settings
DATA_FILE: Final[str] = "drink_data.json"
HISTORY_DAYS: Final[int] = 30  # days

# Logging settings
LOG_LEVEL: Final[str] = "INFO"
LOG_FILE: Final[str] = "reminder.log"
```

## Import Order Example

```python
# Standard library imports
import os
import sys
from typing import Dict, List, Optional
from datetime import datetime

# Third-party imports
import tkinter as tk
from PIL import Image, ImageTk

# Local imports
from src.reminder.models.drink_data import DrinkData
from src.reminder.views.drink_gui import DrinkGUI
from src.reminder.controllers.reminder_controller import ReminderController
from src.reminder.config import (
    REMINDER_START_TIME,
    REMINDER_END_TIME,
    REMINDER_INTERVAL
)
```

## Error Handling Example

```python
def load_data(file_path: str) -> Dict:
    """Load data from JSON file.

    Args:
        file_path: Path to the JSON file.

    Returns:
        Dictionary containing the loaded data.

    Raises:
        FileNotFoundError: If file doesn't exist.
        ValueError: If file contains invalid JSON.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"Data file not found: {file_path}")
        raise
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in file: {file_path}")
        raise ValueError(f"Invalid JSON format: {e}")
    except Exception as e:
        logger.error(f"Unexpected error loading data: {e}")
        raise
```

## Logging Example

```python
import logging
from utils.logger import get_logger

logger = get_logger(__name__)

class ReminderController:
    """Reminder controller with logging."""

    def __init__(self) -> None:
        """Initialize controller."""
        logger.info("Initializing ReminderController")
        self.model = DrinkData("drink_data.json")
        self.view = DrinkGUI(on_drink=self.record_drink)
        logger.debug("Controller initialized successfully")

    def record_drink(self) -> None:
        """Record a drink event."""
        logger.info("Recording drink event")
        try:
            self.model.record_drink()
            logger.debug("Drink recorded successfully")
        except Exception as e:
            logger.error(f"Failed to record drink: {e}")
            raise
```
