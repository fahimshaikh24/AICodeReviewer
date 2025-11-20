# AI Code Reviewer for Python

This is a Streamlit-based **AI Code Reviewer** application for Python. It analyzes your code using:

- **flake8** – style, quality, and potential bug detection  
- **black** – opinionated code formatter  
- **radon** – cyclomatic complexity analysis  

The app provides:

- Linting results with line-level details  
- Before/after formatting suggestions  
- Complexity analysis including high-complexity blocks  
- A clean, human-readable summary of required improvements  
- Downloadable full analysis report (Markdown)  
- Downloadable black-formatted code  

---

## 1. Installation

1. Create and activate a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   # On PowerShell
   .venv\Scripts\Activate.ps1
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

---

## 2. Running the App

From the project root, run:

```bash
streamlit run app.py
```

Then open the URL shown in the terminal (usually `http://localhost:8501`).

---

## 3. Usage

1. Choose how to provide code:
   - **Paste code** into the text area, or  
   - **Upload** a `.py` file.

2. Click **Run Analysis**.

3. Explore the tabs:
   - **Summary** – high-level overview and quick metrics  
   - **Linting (flake8)** – detailed list of issues  
   - **Formatting (black)** – side-by-side before/after view  
   - **Complexity (radon)** – complexity per block and highlights for high complexity  
   - **Full Report** – complete Markdown report

4. Download:
   - The **full Markdown report**  
   - The **formatted code** as a `.py` file

---

## 4. Notes

- The app runs `black`, `flake8`, and `radon` locally.  
- Make sure your Python environment has these tools available (they are included in `requirements.txt`).  
- The analysis runs entirely on your machine; no code is sent to external services.
