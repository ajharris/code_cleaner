# Code Cleaner - Unused Code Detector & Remover

## Overview
Code Cleaner is a tool that scans **Python** and **JavaScript/TypeScript** projects to detect and optionally remove **unused functions, classes, and imports**. It ensures that only the unused portions of files are deleted while preserving the rest of the code.

## Features
- **Detects unused code** (functions, classes, and imports) in both Python and JavaScript/TypeScript.
- **Automatic removal** of unused code with a `--remove` flag.
- **Safe file modifications** ensuring only unused sections are removed.
- **Supports JavaScript (JSX, TypeScript) using Babel's AST parser**.

## Installation

### **Python Dependencies**
Ensure you have Python installed and set up a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install argparse
```

### **JavaScript Dependencies**
Ensure you have Node.js installed, then install Babel parser:
```bash
npm install @babel/parser
```

## Usage

### **Detect Unused Code Only**
```bash
python detect_unused_code.py path/to/project
```
This lists all unused functions, classes, and imports.

### **Detect and Remove Unused Code**
```bash
python detect_unused_code.py path/to/project --remove
```
This removes detected unused code from files automatically.

## Running Tests

### **Python Tests**
```bash
pytest tests
```

### **JavaScript Tests**
```bash
npx jest tests
```

## Future Enhancements
- GUI interface for selecting specific code sections for removal.
- Support for additional languages.
- More advanced analysis for dynamically imported modules.

## Contributing
If you'd like to contribute, feel free to fork the repository, create a feature branch, and submit a pull request.

## License
MIT License

