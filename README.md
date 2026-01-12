# Matrix-Operations-Tool
The code implements an interactive **Matrix Operations Tool** in Python using NumPy for computation and Rich for a structured, colorful console UI.

## Overview

- **Purpose**: Let users input matrices and perform operations: addition, subtraction, multiplication, transpose, and determinant.
- **Tech stack**: Python, **NumPy** for matrix operations, **Rich** for interactive menus, tables, and styled output.

## Main Components

### Imports and Console

- `import numpy as np`: Loads NumPy for matrix creation and operations (dot, transpose, determinant).
- `from rich...`: Imports Rich components to build a nicer console interface (tables, panels, prompts, syntax highlighting).
- `console = Console()`: Single **Console** instance used for all prints.

### Matrix Input Function

```python
def input_matrix(name):
    rows = IntPrompt.ask(f"Rows for {name}")
    cols = IntPrompt.ask(f"Columns for {name}")
    matrix_data = []
    for i in range(rows):
        row_str = Prompt.ask(f"Row {i+1} ({cols} space-separated numbers)")
        row = list(map(float, row_str.split()))
        if len(row) != cols:
            raise ValueError(f"Row must have {cols} elements")
        matrix_data.append(row)
    return np.array(matrix_data)
```

- Prompts user for **rows** and **columns** using Rich’s `IntPrompt`.
- For each row:
  - Asks for space-separated numbers as a string.
  - Splits the string, converts to `float`, validates length, and appends to `matrix_data`.
- Returns a NumPy array using `np.array(matrix_data)` so all operations work efficiently.

### Result Display Function

```python
def display_result(title, result):
    if isinstance(result, np.ndarray):
        np.set_printoptions(precision=2, suppress=True, edgeitems=10, linewidth=100)
        code = Syntax(str(result), "python", theme="monokai")
        console.print(Panel(code, title=title, border_style="blue"))
    else:
        console.print(Panel(f"[bold cyan]{title}:[/] [yellow]{result:.4f}", border_style="green"))
```

- Checks if `result` is a NumPy array or a scalar value (e.g., determinant).
- For arrays:
  - Configures print options for readability (rounded to 2 decimals, no scientific notation).
  - Wraps the string representation in a **Syntax** block and then in a **Panel** for bordered, colored output.
- For scalars:
  - Prints a single value (like determinant) formatted to 4 decimals inside a green panel.

### Matrix Preview Function

```python
def show_matrices(A=None, B=None):
    table = Table(title="Input Matrices", show_header=True, header_style="bold magenta")
    table.add_column("Matrix A", style="cyan")
    table.add_column("Matrix B", style="green")
    if A is not None:
        np.set_printoptions(precision=2, suppress=True)
        table.add_row(str(A), "" if B is None else str(B))
    console.print(table)
```

- Uses a **Table** to show Matrix A and Matrix B side by side when needed.
- Only adds a row if A exists; B is optional depending on the operation.

### Operation Menu and Logic

```python
operations = {
    "1": ("Addition", lambda a, b: a + b),
    "2": ("Subtraction", lambda a, b: a - b),
    "3": ("Multiplication", lambda a, b: np.dot(a, b)),
    "4": "Transpose",
    "5": "Determinant"
}
```

- Maps menu options to operations:  
  - `1`, `2`, `3` use tuples with a name and a lambda function for two-matrix operations.
  - `4`, `5` are single-matrix operations handled separately in the code.

```python
table = Table("Operation", "Description", show_header=True, header_style="bold blue")
for key, desc in operations.items():
    table.add_row(key, str(desc).split("(")[0] if isinstance(desc, tuple) else desc)
console.print(table)

choice = Prompt.ask("Select operation", choices=list(operations.keys()))
```

- Displays available operations in a **Rich table** with two columns: option number and description.
- Forces user to choose one of the valid keys (`1`–`5`).

### Handling Each Operation

Inside the loop:

#### Addition, Subtraction, Multiplication

```python
if choice in ['1','2','3']:
    A = input_matrix("A")
    B = input_matrix("B")
    show_matrices(A, B)
    if choice == '1' and A.shape != B.shape:
        raise ValueError("Same shape required")
    if choice == '3' and A.shape[1] != B.shape[0]:
        raise ValueError("A columns != B rows")
    op_name, func = operations[choice]
    result = func(A, B)
    display_result(f"{op_name} Result", result)
```

- Reads matrices A and B from the user and displays them in a table.
- Validates:
  - Addition / subtraction require same shape `[m, n]`.
  - Multiplication requires A’s columns = B’s rows (standard matrix multiplication rule).
- Calls the corresponding lambda and displays the result nicely formatted.

#### Transpose

```python
elif choice == '4':
    A = input_matrix("Matrix")
    show_matrices(A)
    result = np.transpose(A)
    display_result("Transpose", result)
```

- Reads a single matrix and shows it.
- Uses `np.transpose(A)` to compute the transpose and displays it in a panel.

#### Determinant

```python
elif choice == '5':
    A = input_matrix("Square Matrix")
    if A.shape[0] != A.shape[1]:
        raise ValueError("Must be square")
    show_matrices(A)
    result = np.linalg.det(A)
    display_result("Determinant", result)
```

- Reads one matrix and checks it is square.
- Uses `np.linalg.det(A)` to compute the determinant and prints it as a formatted scalar.

### Error Handling and Loop Control

```python
except ValueError as e:
    console.print(f"[red]Error: {e}[/]")

if not Prompt.ask("Another operation", choices=["y", "n"], default="n") == "y":
    break
```

- Wraps the operation logic in `try/except` to catch validation issues (wrong shape, wrong row length, non-square matrix) and display them in red text.
- Asks if the user wants to perform another operation; exits the loop when the answer is `n`.

### Entry Point

```python
if __name__ == "__main__":
    np.set_printoptions(precision=4)
    main()
```

- Sets a default global print precision for NumPy so numbers are consistent.
- Runs `main()` when the script is executed directly.

***
