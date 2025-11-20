# Python Code Analysis Report

## 1. High-Level Summary

- **17 flake8 issues** detected. These include style violations, potential bugs, and readability problems.
- **Average cyclomatic complexity** per analyzed block is **1.50**.
- ✅ No high-complexity blocks (rank C or worse) were found; complexity levels look healthy.
- **black suggested formatting changes**. Adopting the formatted version will improve consistency, readability, and maintainability across the codebase.

## 2. Linting (flake8)

| Line | Col | Code | Message |
| ---- | --- | ---- | ------- |
| 0 | 0 | `UNKNOWN` | C:\Users\LENOVO~1\AppData\Local\Temp\tmpdwoopd7p.py:1:1: F401 'math' imported but unused |
| 0 | 0 | `UNKNOWN` | C:\Users\LENOVO~1\AppData\Local\Temp\tmpdwoopd7p.py:3:1: E302 expected 2 blank lines, found 1 |
| 0 | 0 | `UNKNOWN` | C:\Users\LENOVO~1\AppData\Local\Temp\tmpdwoopd7p.py:5:5: F841 local variable 'radius' is assigned to but never used |
| 0 | 0 | `UNKNOWN` | C:\Users\LENOVO~1\AppData\Local\Temp\tmpdwoopd7p.py:7:8: E111 indentation is not a multiple of 4 |
| 0 | 0 | `UNKNOWN` | C:\Users\LENOVO~1\AppData\Local\Temp\tmpdwoopd7p.py:8:8: E111 indentation is not a multiple of 4 |
| 0 | 0 | `UNKNOWN` | C:\Users\LENOVO~1\AppData\Local\Temp\tmpdwoopd7p.py:9:18: W291 trailing whitespace |
| 0 | 0 | `UNKNOWN` | C:\Users\LENOVO~1\AppData\Local\Temp\tmpdwoopd7p.py:12:1: E302 expected 2 blank lines, found 1 |
| 0 | 0 | `UNKNOWN` | C:\Users\LENOVO~1\AppData\Local\Temp\tmpdwoopd7p.py:13:4: E111 indentation is not a multiple of 4 |
| 0 | 0 | `UNKNOWN` | C:\Users\LENOVO~1\AppData\Local\Temp\tmpdwoopd7p.py:14:4: F841 local variable 'y' is assigned to but never used |
| 0 | 0 | `UNKNOWN` | C:\Users\LENOVO~1\AppData\Local\Temp\tmpdwoopd7p.py:14:4: E111 indentation is not a multiple of 4 |
| 0 | 0 | `UNKNOWN` | C:\Users\LENOVO~1\AppData\Local\Temp\tmpdwoopd7p.py:14:9: E261 at least two spaces before inline comment |
| 0 | 0 | `UNKNOWN` | C:\Users\LENOVO~1\AppData\Local\Temp\tmpdwoopd7p.py:15:4: E111 indentation is not a multiple of 4 |
| 0 | 0 | `UNKNOWN` | C:\Users\LENOVO~1\AppData\Local\Temp\tmpdwoopd7p.py:15:20: E231 missing whitespace after ',' |
| 0 | 0 | `UNKNOWN` | C:\Users\LENOVO~1\AppData\Local\Temp\tmpdwoopd7p.py:16:4: E111 indentation is not a multiple of 4 |
| 0 | 0 | `UNKNOWN` | C:\Users\LENOVO~1\AppData\Local\Temp\tmpdwoopd7p.py:17:4: E111 indentation is not a multiple of 4 |
| 0 | 0 | `UNKNOWN` | C:\Users\LENOVO~1\AppData\Local\Temp\tmpdwoopd7p.py:19:1: E305 expected 2 blank lines after class or function definition, found 1 |
| 0 | 0 | `UNKNOWN` | C:\Users\LENOVO~1\AppData\Local\Temp\tmpdwoopd7p.py:20:1: W391 blank line at end of file |


## 3. Formatting (black)

black reformatted the code. The suggested formatted version is shown below.

### 3.1 Original Code

```python
import math

def calculate_area(r):
    pi = 3.14
    radius = r
    if r < 0:
       print("radius can't be negative")
       return
    area = pi*r*r  
    return area

def main():
   x = 10
   y = 0 # unused variable
   print("area is:",calculate_area(x))
   print("area of -5:", calculate_area(-5))
   print("done")

main()
```

### 3.2 Formatted Code (black)

```python
import math


def calculate_area(r):
    pi = 3.14
    radius = r
    if r < 0:
        print("radius can't be negative")
        return
    area = pi * r * r
    return area


def main():
    x = 10
    y = 0  # unused variable
    print("area is:", calculate_area(x))
    print("area of -5:", calculate_area(-5))
    print("done")


main()
```

## 4. Complexity Analysis (radon)

- **Average complexity per block**: `1.50`

### 4.1 All Analyzed Blocks

| Name | Type | Line | Complexity | Rank |
| ---- | ---- | ---- | ---------- | ---- |
| `calculate_area` | function | 3 | 2 | A |
| `main` | function | 12 | 1 | A |


### 4.2 High-Complexity Blocks (Rank C or Worse)

No high-complexity blocks (rank C or worse) were detected.


## 5. Recommended Improvements

- Address flake8 issues in order of severity (e.g., potential bugs and undefined variables first, then style and readability issues).
- For high-complexity blocks, consider:
  - Extracting helper functions to reduce the amount of logic in a single block.
  - Simplifying nested conditionals and loops.
  - Breaking down large classes into smaller, cohesive components.
- Adopt the black-formatted version of the code to keep style consistent across your project.
