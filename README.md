# Calculator - Modular Design

A modern, modular calculator toolkit written in Python with clean separation of business logic and user interfaces.

## Features

- 🖥️ **Graphical User Interface (GUI)** - Built with Kivy for desktop
- 💻 **Command-Line Interface (CLI)** - For terminal-based operations
- ➕ Full arithmetic operations (addition, subtraction, multiplication, division)
- 🎯 Clean, modular architecture - UI completely separated from core logic
- 🧮 Supports floating-point arithmetic with decimal points

## Architecture

The project follows a modular design pattern:
- **`calculator/`** - Core business logic
- **`calculator/ui/`** - User interface implementations
  - `cli.py` - Command-line interface
  - `gui.py` - Graphical interface using Kivy

## Requirements

- Python >= 3.8
- Kivy 2.3.1

## Installation

1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### GUI (Graphical Mode)

```bash
python -m calculator.ui.gui
```

This launches an interactive desktop calculator with a button grid interface.

### CLI (Command-Line Mode)

```bash
python -m calculator.ui.cli EXPRESSION
```

where `EXPRESSION` is a mathematical expression to be evaluated.


## How to restore dependencies

Open a shell in this directory, and run the following command:

```bash
pip install -r requirements.txt
```
