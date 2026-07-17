# Python & SQL Financial Data Pipeline Curriculum

Welcome to the automated financial database pipeline curriculum! In this course, you will transition from learning basic Python syntax to advanced SQL query integration, ultimately building an automated financial data pipeline. 

## The Golden Workflow (How to Handle Each Week)

1. **Read:** Open the week's folder, read the `README.md`, and review the concepts and best practices.
2. **Initialize Database:** If it is Week 07 or later, run the week's localized setup script (explained below) to configure the database for that lesson.
3. **Practice:** Complete the fill-in-the-blank `practice.py` (or `practice.sql`) using the designated `# TODO` comments.
4. **Test Practice:** Run `pytest` on the practice file to verify the code is working.
5. **Assignment:** Build the open-ended programmatic `assignment.py` (or `assignment.sql`) from scratch based on the requirements.
6. **Test Assignment:** Run `pytest` on the assignment to earn credit and mark the week complete.

## How to Open the VS Code Terminal

To run commands, you'll need to open the terminal in VS Code:
- **Windows/Linux:** Press `Ctrl + \`` (the backtick key, usually above Tab).
- **Mac:** Press `Cmd + \``.
- **Menu:** Navigate to the top menu and select **Terminal** -> **New Terminal**.

## Initial Setup (Step-by-Step)

Before you begin, you need to set up the project environment. **Python 3.12 or higher** is strictly required.

1. Open your terminal as described above.
2. Ensure you are in the root directory of the repository (`PySQLClass`).
3. Run the setup script for your operating system:

**Windows:**
```cmd
setup_project_windows.bat
```

**macOS/Linux:**
```bash
chmod +x setup_project_mac_linux.sh && ./setup_project_mac_linux.sh
```

## Weekly Transitions & Local Database Bootstrapping

When moving to a new week (**Folders 07 to 20**), you **must** configure your sandbox database for that specific lesson. 

1. Open your terminal.
2. Navigate into the folder for the week (e.g., `cd folder_07_basic_select`).
3. Run the following command:
   ```bash
   python setup_database.py
   ```

**Why is this necessary?** 
Running this script resets `finance.db` to the exact database structure and data baseline needed for that specific week. It ensures your tests run smoothly, allows you to practice out of order, and safely resets your progress if you ever get stuck or make a mistake!
