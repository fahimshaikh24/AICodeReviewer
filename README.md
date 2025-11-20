# AI Code Reviewer for Python

This is a Streamlit-based **AI Code Reviewer** application for Python. It analyzes your code using **flake8**, **black**, and **radon** and produces a human-readable report that summarizes style issues, formatting improvements, and complexity hotspots.

The goal of this project is to give you a **single, interactive UI** where you can drop in any Python file and immediately see:

- Where your code breaks common style and quality rules
- How the code would look after being formatted with `black`
- Which functions/methods/classes are too complex and worth refactoring

---

## 1. Features

### 1.1 Linting (flake8)

- Runs `flake8` against the original source code.
- Shows a **table of lint issues** with:
  - Line and column numbers
  - Error code (e.g., `E302`, `F401`, etc.)
  - Human-readable message
- Helps you quickly locate and prioritize style problems and potential bugs.

### 1.2 Formatting (black)

- Uses `black` via its Python API to format your code.
- Displays **before/after code blocks** side by side:
  - Left: your original code
  - Right: black-formatted code
- Indicates whether black had to make any changes.
- Lets you download the formatted version as a ready-to-use `.py` file.

### 1.3 Complexity Analysis (radon)

- Uses `radon` to compute **cyclomatic complexity** for each function, method, and class.
- Shows:
  - Name
  - Type (function / method / class)
  - Line number
  - Numeric complexity score
  - Complexity **rank** (`A`–`F`, where `A` is simple and `F` is extremely complex)
- Highlights **high-complexity blocks (rank C or worse)** in a separate table so you can focus refactoring efforts where they matter most.

### 1.4 Summary & Reporting

- Summary tab with key metrics:
  - Total number of flake8 issues
  - Average cyclomatic complexity
  - Whether formatting changes were needed
- Generates a **Markdown report** containing:
  - High-level bullet-point summary
  - Detailed flake8 issues table
  - Original vs. formatted code blocks
  - Full complexity tables and high-complexity highlights
  - Suggested next steps and refactoring guidance
- You can download this report as `code_analysis_report.md`.

---

## 2. Project Structure

```text
ai-code-reviewer/
├── app.py               # Streamlit UI entry point
├── analysis_engine.py   # Core analysis logic (flake8, black, radon)
├── report_generator.py  # Markdown report builder
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

### 2.1 `app.py`

- Configures the Streamlit page and layout.
- Provides two input modes:
  - **Paste code** into a text area
  - **Upload** a `.py` file
- Calls `analyze_code` from `analysis_engine.py` and routes results into:
  - Summary tab
  - Linting tab
  - Formatting tab
  - Complexity tab
  - Full report tab
- Exposes download buttons for both the Markdown report and the formatted code.

### 2.2 `analysis_engine.py`

- Contains the core data models and processing pipeline:
  - `Flake8Issue` – single lint issue
  - `ComplexityBlock` – single complexity entry for a function/method/class
  - `AnalysisResult` – aggregated result returned to the UI
- Uses:
  - `black` API (`format_str`) for formatting
  - `flake8` via subprocess on a temp file for linting
  - `radon.cc_visit` and `cc_rank` for complexity
- Encapsulates all tool-specific details so the UI remains clean.

### 2.3 `report_generator.py`

- Converts an `AnalysisResult` into a **single Markdown document**.
- Builds:
  - Summary bullets
  - Linting tables
  - Complexity tables
  - Original and formatted code blocks
  - Suggested improvements section
- Used both for the **Full Report** tab in the app and for the **downloadable report file**.

---

## 3. Installation

1. Create and activate a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   # On PowerShell
   .venv\Scripts\Activate.ps1
   ```

2. Upgrade `pip` (recommended):

   ```bash
   python -m pip install --upgrade pip
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

> If you encounter issues with platform-specific wheels (for example, Pillow / image-related dependencies), make sure you are using a Python version that is supported by all packages in `requirements.txt`.

---

## 4. Running the App

From the project root, run:

```bash
streamlit run app.py
```

Then open the URL shown in the terminal (usually `http://localhost:8501`).

---

## 5. Usage Workflow

1. **Start the app** using the command above.
2. **Provide code**:
   - Paste Python code into the text area, or
   - Upload a `.py` file from your system.
3. Click **Run Analysis**.
4. Review the results:
   - **Summary** – quick overview and key metrics.
   - **Linting (flake8)** – list of issues with locations and messages.
   - **Formatting (black)** – compare original vs. formatted code.
   - **Complexity (radon)** – per-block complexity and high-complexity focus.
   - **Full Report** – rendered Markdown report.
5. **Download artifacts**:
   - Full Markdown report (`code_analysis_report.md`).
   - Formatted code (`formatted_code.py`).

---

## 6. Notes and Limitations

- All analysis is performed **locally** on your machine; no code is sent anywhere.
- The quality of flake8 results depends on the configured default rules; this project uses flake8 with its standard configuration unless you extend it.
- The app currently analyzes **one file at a time**. For multi-module projects, you can run it separately on each file or extend the app to support directories.
- Complexity scores from `radon` are a heuristic; use them as a guide for refactoring, not as strict pass/fail criteria.
