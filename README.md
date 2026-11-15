# LibraDesk — Library Inventory Manager

A desktop application for managing a library book inventory using Tkinter and SQLite.

**Original source:** [`library_management_system.py`](library_management_system.py) (preserved exactly from the uploaded file).

## Technologies

- Python 3.10+
- Tkinter (included in standard Windows Python installs)
- SQLite (Python standard library)

## Features verified from the source

- Add, edit, delete, search and list books
- Track ISBN, author, category, total and available quantities
- Show dashboard summary counts and validate book quantities

## Run on Windows

1. Download/clone the project and open its folder in File Explorer.
2. Click the File Explorer address bar, type `cmd`, and press Enter.
3. Run:

   ```cmd
   python library_management_system.py
   ```

You can also open the script in **Python IDLE**, then select **Run → Run Module (F5)**.

No third-party packages are required for this project. Keep the Python window open while using the application.

## Limitations

This version manages books only: it does **not** implement member registration, book issue/return forms or loan-due dates. The issued-count display reflects the database values, but the UI has no borrowing workflow.

This is a learning/portfolio project. The original script has been checked with Python syntax parsing, and selected non-GUI logic has been smoke-tested. **Its complete Tkinter interface was not tested in an actual Windows desktop session.**

## GitHub

Commit the Python file, this README and `.gitignore`. Generated `.db` files and personal records are ignored by Git. Store real data outside public GitHub repositories.
