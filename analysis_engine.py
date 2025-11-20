import subprocess
import tempfile
from dataclasses import dataclass
from typing import List, Optional, Tuple

import black
from radon.complexity import cc_visit, cc_rank


class AnalysisError(Exception):
    """Raised when any of the analysis stages fails in an unrecoverable way."""


@dataclass
class Flake8Issue:
    line: int
    col: int
    code: str
    message: str


@dataclass
class ComplexityBlock:
    name: str
    lineno: int
    complexity: int
    rank: str
    block_type: str  # e.g. "function", "class", "method"


@dataclass
class AnalysisResult:
    original_code: str
    formatted_code: str
    flake8_issues: List[Flake8Issue]
    complexity_blocks: List[ComplexityBlock]
    high_complexity_blocks: List[ComplexityBlock]
    average_complexity: Optional[float]
    flake8_error: Optional[str] = None


def _run_black(code: str) -> str:
    """Format code using black's Python API."""
    try:
        mode = black.FileMode()
        return black.format_str(code, mode=mode)
    except Exception as exc:  # pragma: no cover - extremely rare
        raise AnalysisError(f"black formatting failed: {exc}") from exc


def _run_flake8(code: str) -> Tuple[List[Flake8Issue], Optional[str]]:
    """
    Run flake8 via subprocess on a temporary file and parse its output.

    Returns (issues, error_message). error_message is None on success.
    """
    issues: List[Flake8Issue] = []
    error_message: Optional[str] = None

    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".py",
        delete=False,
        encoding="utf-8",
    ) as tmp:
        tmp.write(code)
        tmp_path = tmp.name

    try:
        # --format string -> path:line:col: code message
        result = subprocess.run(
            ["flake8", "--format=%(path)s:%(row)d:%(col)d: %(code)s %(text)s", tmp_path],
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        # flake8 not installed or not in PATH
        return [], "flake8 is not installed or not found in PATH. Install it via `pip install flake8`."

    if result.returncode not in (0, 1):
        # 0: no issues; 1: issues; other: error
        error_message = (
            f"flake8 execution failed with return code {result.returncode}: {result.stderr.strip()}"
        )
        return [], error_message

    for line in result.stdout.splitlines():
        # Format: /tmp/tmpxyz.py:line:col: CODE message...
        try:
            _, rest = line.split(":", 1)
            line_part, col_part, rest2 = rest.split(":", 2)
            line_no = int(line_part.strip())
            col_no = int(col_part.strip())
            rest2 = rest2.strip()
            code_part, msg_part = rest2.split(" ", 1)
            issues.append(
                Flake8Issue(
                    line=line_no,
                    col=col_no,
                    code=code_part.strip(),
                    message=msg_part.strip(),
                )
            )
        except ValueError:
            # If parsing fails, treat the whole line as a message on line 0
            issues.append(
                Flake8Issue(
                    line=0,
                    col=0,
                    code="UNKNOWN",
                    message=line.strip(),
                )
            )

    return issues, error_message


def _run_radon_complexity(code: str) -> Tuple[List[ComplexityBlock], Optional[float]]:
    """
    Use radon's Python API to get cyclomatic complexity per block (function/method/class).

    Returns (blocks, average_complexity).
    """
    blocks: List[ComplexityBlock] = []
    try:
        radon_blocks = cc_visit(code)
    except Exception as exc:  # pragma: no cover - defensive
        raise AnalysisError(f"radon complexity analysis failed: {exc}") from exc

    total_complexity = 0.0

    for b in radon_blocks:
        # b is typically a Function or Class block, with attributes:
        # name, lineno, complexity, etc.
        comp_value = float(b.complexity)
        total_complexity += comp_value
        block_type = getattr(b, "entity", None) or b.__class__.__name__.lower()
        blocks.append(
            ComplexityBlock(
                name=b.name,
                lineno=b.lineno,
                complexity=int(comp_value),
                rank=cc_rank(comp_value),
                block_type=block_type,
            )
        )

    avg_complexity: Optional[float]
    if blocks:
        avg_complexity = total_complexity / len(blocks)
    else:
        avg_complexity = None

    # Sort by complexity descending
    blocks.sort(key=lambda blk: blk.complexity, reverse=True)

    return blocks, avg_complexity


def analyze_code(code: str) -> AnalysisResult:
    """
    Run all analyses (black, flake8, radon) and return a structured result.

    This function is the main entry point for the Streamlit app.
    """
    if not isinstance(code, str):
        raise AnalysisError("Code must be a string.")

    original_code = code

    # 1. Formatting (black)
    formatted_code = _run_black(original_code)

    # 2. Linting (flake8)
    flake8_issues, flake8_error = _run_flake8(original_code)

    # 3. Complexity (radon)
    complexity_blocks, average_complexity = _run_radon_complexity(original_code)

    # High complexity: rank C or worse
    high_complexity_blocks = [
        blk for blk in complexity_blocks if blk.rank.upper() >= "C"
    ]

    return AnalysisResult(
        original_code=original_code,
        formatted_code=formatted_code,
        flake8_issues=flake8_issues,
        complexity_blocks=complexity_blocks,
        high_complexity_blocks=high_complexity_blocks,
        average_complexity=average_complexity,
        flake8_error=flake8_error,
    )
