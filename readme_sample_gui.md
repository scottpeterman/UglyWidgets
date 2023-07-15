# sample_gui_with_prompt.py

This project presents four reusable PyQt6 widgets that can be integrated into any PyQt6 application. The widgets include an SSH Terminal, a Windows Terminal with support for cmd, PowerShell, and WSL2, an ace.js based editor, and a file explorer widget.

## Sample Use Of Widget Descriptions

### 1. SSH Terminal Widget (QtSSH_Widget)

This widget provides an SSH terminal interface within the application. It allows users to connect to a remote machine using SSH credentials (IP address, username, and password). The credentials are entered in a dialog box that opens when the widget is instantiated. Once connected, users can execute commands on the remote machine directly from this widget.

### 2. Windows Terminal Widget (QtWinCon_Widget)

This widget provides a Windows Terminal within the application. It supports cmd, PowerShell, and WSL2, thus offering flexibility for users in choosing their preferred shell. Users can use this terminal to execute Windows commands directly from the application.

### 3. Ace.js-based Editor Widget (QtAce_Widget)

This widget integrates an ace.js-based editor in the application. Ace is a high-performance code editor for the web, offering syntax highlighting for over 110 languages, and 20 themes out of the box. The Ace widget brings this functionality into your PyQt6 application, allowing users to edit code with syntax highlighting and other features.

### 4. File Explorer Widget (FileTree)

This widget presents a file explorer interface, allowing users to navigate through the local file system in a hierarchical tree structure. This makes it easy to browse directories and files, offering the ability to interact such as opening files in the Ace editor or executing them in the terminal widgets.

## Additional Information

Please replace this section with any other information that might be relevant for the users of your widgets, such as installation instructions, usage examples, dependencies, or any other relevant details.
