# PyQt6 SSH Terminal Widget (QtSSH_Widget)

This README provides an overview of the PyQt6 SSH Terminal Widget (QtSSH_Widget), detailing its functionality, dependencies, and usage.

## Overview

The PyQt6 SSH Terminal Widget provides an SSH terminal interface within a PyQt6 application. It allows users to connect to a remote machine using SSH credentials (IP address, username, and password). Once connected, users can execute commands on the remote machine directly from this widget.

## Dependencies

The PyQt6 SSH Terminal Widget is dependent on the following libraries:

- PyQt6
- PyQt6.QtWebEngineWidgets
- PyQt6.QtWebEngineCore
- PyQt6.QtWebChannel

In addition, this widget uses two custom modules:

- sshschemahandler: This module provides a custom URL scheme handler for Qt's QWebEngineView.
- sshshell: This module provides the backend SSH connection and command execution functionality.

Ensure that all these dependencies are properly installed and available in your environment.

## Usage

Here's a general guide on how to implement and use the PyQt6 SSH Terminal Widget in your PyQt6 application:

### Sample Usage

Below is a sample script (`ssh_example.py`) demonstrating how to instantiate the SSH Terminal widget in your PyQt6 application:

```python
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from qtssh_widget import Ui_Terminal

def main():
    app = QApplication(sys.argv)

    # Create a QMainWindow instance
    main_window = QMainWindow()
    main_window.resize(800, 600)  # Resize the window to 800x600

    # Create a Ui_Terminal instance
    terminal = Ui_Terminal({"host": "<HOST_IP>", "username": "<USERNAME>", "password": "<PASSWORD>"}, main_window)

    # Set terminal as the central widget of main_window
    main_window.setCentralWidget(terminal)
    main_window.setWindowTitle("PyQt6 - SSH Widget")

    main_window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
