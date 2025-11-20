import streamlit as st

from analysis_engine import analyze_code, AnalysisError
from report_generator import generate_markdown_report


def main() -> None:
    st.set_page_config(
        page_title="AI Code Reviewer (Python)",
        page_icon="🧠",
        layout="wide",
    )

    st.title("🧠 AI Code Reviewer for Python")
    st.write(
        "Upload or paste Python code to automatically analyze it with **flake8**, "
        "**black**, and **radon**. Get linting, formatting suggestions, and "
        "complexity insights with a downloadable report."
    )

    st.sidebar.header("Instructions")
    st.sidebar.markdown(
        "- Choose how to provide your code: paste or upload `.py` file.\n"
        "- Click **Run Analysis**.\n"
        "- Review the **Summary**, **Linting**, **Formatting**, and **Complexity** tabs.\n"
        "- Download the full report and the formatted code."
    )

    input_mode = st.radio(
        "How would you like to provide your Python code?",
        options=["Paste code", "Upload .py file"],
        horizontal=True,
    )

    code_text = ""
    uploaded_file = None

    if input_mode == "Paste code":
        code_text = st.text_area(
            "Paste your Python code here:",
            height=350,
            placeholder="Paste Python code...",
        )
    else:
        uploaded_file = st.file_uploader(
            "Upload a Python (.py) file:",
            type=["py"],
        )

    run_analysis = st.button("Run Analysis", type="primary")

    if run_analysis:
        if input_mode == "Paste code":
            if not code_text.strip():
                st.error("Please paste some Python code before running the analysis.")
                return
            code_to_analyze = code_text
        else:
            if uploaded_file is None:
                st.error("Please upload a `.py` file before running the analysis.")
                return
            file_bytes = uploaded_file.read()
            try:
                code_to_analyze = file_bytes.decode("utf-8")
            except UnicodeDecodeError:
                code_to_analyze = file_bytes.decode("latin-1")

        with st.spinner("Running flake8, black, and radon analyses..."):
            try:
                analysis_result = analyze_code(code_to_analyze)
            except AnalysisError as exc:
                st.error(f"Analysis failed: {exc}")
                return

        # Build report text once, reuse for display & download
        report_markdown = generate_markdown_report(analysis_result)

        summary_tab, lint_tab, format_tab, complexity_tab, report_tab = st.tabs(
            ["Summary", "Linting (flake8)", "Formatting (black)", "Complexity (radon)", "Full Report"]
        )

        # --- Summary tab ---
        with summary_tab:
            st.subheader("Overall Summary")

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric(
                    "Flake8 issues",
                    len(analysis_result.flake8_issues),
                )
            with col2:
                if analysis_result.average_complexity is not None:
                    st.metric(
                        "Average complexity",
                        f"{analysis_result.average_complexity:.2f}",
                    )
                else:
                    st.metric("Average complexity", "N/A")
            with col3:
                changed = (
                    analysis_result.formatted_code.strip()
                    != analysis_result.original_code.strip()
                )
                st.metric("Formatting changes", "Yes" if changed else "No")

            st.markdown("### Key Improvement Areas")
            if not analysis_result.flake8_issues and not analysis_result.high_complexity_blocks:
                st.success(
                    "No flake8 issues found and all functions/classes have low complexity. "
                    "Your code looks clean and maintainable."
                )
            else:
                bullets = []
                if analysis_result.flake8_issues:
                    bullets.append(
                        f"- **{len(analysis_result.flake8_issues)} flake8 issues** detected "
                        "(style, quality, or possible bugs)."
                    )
                if analysis_result.high_complexity_blocks:
                    bullets.append(
                        f"- **{len(analysis_result.high_complexity_blocks)} high-complexity blocks** "
                        "(rank C or worse) that may be harder to maintain or test."
                    )
                if (
                    analysis_result.formatted_code.strip()
                    != analysis_result.original_code.strip()
                ):
                    bullets.append(
                        "- **Formatting changes recommended** by black (consistent style, spacing, and line length)."
                    )

                if bullets:
                    st.markdown("\n".join(bullets))

            st.markdown("### Downloads")
            col_left, col_right = st.columns(2)
            with col_left:
                st.download_button(
                    label="⬇️ Download full analysis report (Markdown)",
                    data=report_markdown.encode("utf-8"),
                    file_name="code_analysis_report.md",
                    mime="text/markdown",
                )
            with col_right:
                st.download_button(
                    label="⬇️ Download formatted code (black)",
                    data=analysis_result.formatted_code.encode("utf-8"),
                    file_name="formatted_code.py",
                    mime="text/x-python",
                )

        # --- Linting tab ---
        with lint_tab:
            st.subheader("flake8 Linting Results")
            if not analysis_result.flake8_issues:
                st.success("No flake8 issues found. 🎉")
            else:
                st.info(
                    "Each issue includes line/column, error code, and a short description."
                )
                lint_rows = [
                    {
                        "Line": issue.line,
                        "Column": issue.col,
                        "Code": issue.code,
                        "Message": issue.message,
                    }
                    for issue in analysis_result.flake8_issues
                ]
                st.dataframe(lint_rows, use_container_width=True)

        # --- Formatting tab ---
        with format_tab:
            st.subheader("Formatting (black) – Before & After")

            col_before, col_after = st.columns(2)

            with col_before:
                st.caption("Original code")
                st.code(analysis_result.original_code, language="python")

            with col_after:
                st.caption("Formatted by black")
                st.code(analysis_result.formatted_code, language="python")

            if (
                analysis_result.formatted_code.strip()
                == analysis_result.original_code.strip()
            ):
                st.success("black did not change the code – it is already well formatted.")
            else:
                st.warning(
                    "black suggested formatting changes. Review the 'After' version and "
                    "consider adopting it for consistency."
                )

        # --- Complexity tab ---
        with complexity_tab:
            st.subheader("Complexity Analysis (radon)")

            if not analysis_result.complexity_blocks:
                st.info("No functions, methods, or classes were detected for complexity analysis.")
            else:
                st.markdown("#### All blocks (sorted by complexity)")
                rows = [
                    {
                        "Name": block.name,
                        "Type": block.block_type,
                        "Line": block.lineno,
                        "Complexity": block.complexity,
                        "Rank": block.rank,
                    }
                    for block in analysis_result.complexity_blocks
                ]
                st.dataframe(rows, use_container_width=True)

                st.markdown("#### High-complexity blocks (rank C or worse)")
                if not analysis_result.high_complexity_blocks:
                    st.success("No high-complexity blocks detected (rank C or worse).")
                else:
                    high_rows = [
                        {
                            "Name": block.name,
                            "Type": block.block_type,
                            "Line": block.lineno,
                            "Complexity": block.complexity,
                            "Rank": block.rank,
                        }
                        for block in analysis_result.high_complexity_blocks
                    ]
                    st.dataframe(high_rows, use_container_width=True)

        # --- Full report tab ---
        with report_tab:
            st.subheader("Full Analysis Report (Markdown)")
            st.markdown(report_markdown)


if __name__ == "__main__":
    main()
