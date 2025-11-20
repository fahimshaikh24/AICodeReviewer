from typing import List

from analysis_engine import AnalysisResult, Flake8Issue, ComplexityBlock


def _format_flake8_section(issues: List[Flake8Issue]) -> str:
    if not issues:
        return "No flake8 issues were detected.\n"

    lines = [
        "| Line | Col | Code | Message |",
        "| ---- | --- | ---- | ------- |",
    ]
    for issue in issues:
        lines.append(
            f"| {issue.line} | {issue.col} | `{issue.code}` | {issue.message} |"
        )
    return "\n".join(lines) + "\n"


def _format_complexity_section(blocks: List[ComplexityBlock]) -> str:
    if not blocks:
        return "No functions, methods, or classes were found for complexity analysis.\n"

    lines = [
        "| Name | Type | Line | Complexity | Rank |",
        "| ---- | ---- | ---- | ---------- | ---- |",
    ]
    for blk in blocks:
        lines.append(
            f"| `{blk.name}` | {blk.block_type} | {blk.lineno} | {blk.complexity} | {blk.rank} |"
        )
    return "\n".join(lines) + "\n"


def _format_high_complexity_section(blocks: List[ComplexityBlock]) -> str:
    high = [blk for blk in blocks if blk.rank.upper() >= "C"]
    if not high:
        return "No high-complexity blocks (rank C or worse) were detected.\n"

    lines = [
        "The following blocks are considered **high-complexity** (rank C or worse):\n",
        "| Name | Type | Line | Complexity | Rank |",
        "| ---- | ---- | ---- | ---------- | ---- |",
    ]
    for blk in high:
        lines.append(
            f"| `{blk.name}` | {blk.block_type} | {blk.lineno} | {blk.complexity} | {blk.rank} |"
        )
    return "\n".join(lines) + "\n"


def _summary_bullets(result: AnalysisResult) -> str:
    bullets = []

    if result.flake8_issues:
        bullets.append(
            f"- **{len(result.flake8_issues)} flake8 issues** detected. "
            "These include style violations, potential bugs, and readability problems."
        )
    else:
        bullets.append(
            "- ✅ No flake8 issues were detected. The code adheres to common style guidelines."
        )

    if result.average_complexity is not None:
        bullets.append(
            f"- **Average cyclomatic complexity** per analyzed block is "
            f"**{result.average_complexity:.2f}**."
        )
    else:
        bullets.append(
            "- No functions, methods, or classes were found for complexity analysis."
        )

    if result.high_complexity_blocks:
        bullets.append(
            f"- **{len(result.high_complexity_blocks)} high-complexity blocks** "
            "(rank C or worse) were detected. Consider refactoring these into "
            "smaller, more focused functions or simplifying conditional logic."
        )
    else:
        bullets.append(
            "- ✅ No high-complexity blocks (rank C or worse) were found; complexity levels look healthy."
        )

    if (
        result.formatted_code.strip()
        != result.original_code.strip()
    ):
        bullets.append(
            "- **black suggested formatting changes**. Adopting the formatted version will "
            "improve consistency, readability, and maintainability across the codebase."
        )
    else:
        bullets.append(
            "- ✅ The code is already formatted consistently according to black's defaults."
        )

    return "\n".join(bullets)


def generate_markdown_report(result: AnalysisResult) -> str:
    """
    Build a full Markdown report summarizing the analysis.

    This is used both for on-screen display and for the downloadable report file.
    """
    lines: List[str] = []

    lines.append("# Python Code Analysis Report\n")

    lines.append("## 1. High-Level Summary\n")
    lines.append(_summary_bullets(result))
    lines.append("")

    lines.append("## 2. Linting (flake8)\n")
    if result.flake8_error:
        lines.append("> ⚠️ flake8 reported an error while running:\n")
        lines.append(f"> {result.flake8_error}\n")
    lines.append(_format_flake8_section(result.flake8_issues))
    lines.append("")

    lines.append("## 3. Formatting (black)\n")
    changed = result.formatted_code.strip() != result.original_code.strip()
    if changed:
        lines.append(
            "black reformatted the code. The suggested formatted version is shown below.\n"
        )
    else:
        lines.append("black made no changes; the code is already well formatted.\n")

    lines.append("### 3.1 Original Code\n")
    lines.append("```python")
    lines.append(result.original_code.rstrip())
    lines.append("```")
    lines.append("")

    lines.append("### 3.2 Formatted Code (black)\n")
    lines.append("```python")
    lines.append(result.formatted_code.rstrip())
    lines.append("```")
    lines.append("")

    lines.append("## 4. Complexity Analysis (radon)\n")
    if result.average_complexity is not None:
        lines.append(
            f"- **Average complexity per block**: `{result.average_complexity:.2f}`\n"
        )
    lines.append("### 4.1 All Analyzed Blocks\n")
    lines.append(_format_complexity_section(result.complexity_blocks))
    lines.append("")

    lines.append("### 4.2 High-Complexity Blocks (Rank C or Worse)\n")
    lines.append(_format_high_complexity_section(result.complexity_blocks))
    lines.append("")

    lines.append("## 5. Recommended Improvements\n")
    lines.append(
        "- Address flake8 issues in order of severity (e.g., potential bugs and "
        "undefined variables first, then style and readability issues).\n"
        "- For high-complexity blocks, consider:\n"
        "  - Extracting helper functions to reduce the amount of logic in a single block.\n"
        "  - Simplifying nested conditionals and loops.\n"
        "  - Breaking down large classes into smaller, cohesive components.\n"
        "- Adopt the black-formatted version of the code to keep style consistent across "
        "your project.\n"
    )

    return "\n".join(lines).strip() + "\n"
