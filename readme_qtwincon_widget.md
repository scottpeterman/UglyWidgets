# PyQt6 Windows Terminal Widget (QtWinCon_Widget)

This README provides an overview of the PyQt6 Windows Terminal Widget (QtWinCon_Widget), detailing its functionality, dependencies, and usage.

## Overview

The PyQt6 Windows Terminal Widget provides a terminal interface within a PyQt6 application that can interact with different shells such as cmd, PowerShell, or Windows Subsystem for Linux (WSL2). Users can execute shell commands directly from this widget.

## Dependencies

The PyQt6 Windows Terminal Widget is dependent on the following libraries:

- PyQt6
- PyQt6.QtWebEngineWidgets
- PyQt6.QtWebEngineCore
- PyQt6.QtWebChannel

In addition, this widget uses two custom modules:

- winschemahandler: This module provides a custom URL scheme handler for Qt's QWebEngineView.
- winshell: This module provides the backend for executing shell commands.

Ensure that all these dependencies are properly installed and available in your environment.

## Usage

Here's a general guide on how to implement and use the PyQt6 Windows Terminal Widget in your PyQt6 application:

### Sample Usage

Below is a sample script (`wincon_example.py`) demonstrating how to instantiate the Windows Terminal widget in your PyQt6 application:

```python
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from qtwincon_widget import Ui_Terminal

def main():
    app = QApplication(sys.argv)

    # Create a QMainWindow instance
    main_window = QMainWindow()
    main_window.resize(800, 600)  # Resize the window to 800x600

    # Create a Ui_Terminal instance
    shell = "cmd.exe"  # You can also use "powershell.exe" or "wsl.exe"
    terminal = Ui_Terminal(shell, main_window)

    # Set terminal as the central widget of main_window
    main_window.setCentralWidget(terminal)
    main_window.setWindowTitle(f"PyQt6 - Terminal Widget - Shell is: {shell}")

    main_window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
