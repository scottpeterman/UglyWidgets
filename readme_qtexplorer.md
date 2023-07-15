# PyQt6 File Explorer Widget (FileTree)

This README provides an overview of the PyQt6 File Explorer Widget, detailing its functionality, dependencies, and usage.

## Overview

The PyQt6 File Explorer Widget is a tree-based file explorer within a PyQt6 application. It allows users to select a directory and view its content in a tree structure. When a file is double-clicked, it will be opened with a separate script `qtace_app.py`.

## Dependencies

The PyQt6 File Explorer Widget is dependent on the following libraries:

- PyQt6
- PyQt6.QtWidgets
- PyQt6.QtGui
- PyQt6.QtCore
- os
- sys
- subprocess

Ensure that all these dependencies are properly installed and available in your environment.

## Usage

Here's a general guide on how to implement and use the PyQt6 File Explorer Widget in your PyQt6 application:

### Sample Usage

Below is a sample script demonstrating how to instantiate the File Explorer widget in your PyQt6 application:

```python
from PyQt6 import QtWidgets
from qtexplorer import FileTree
import sys

def main():
    app = QtWidgets.QApplication(sys.argv)

    # Create a FileTree instance
    fileTree = FileTree()
    fileTree.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
