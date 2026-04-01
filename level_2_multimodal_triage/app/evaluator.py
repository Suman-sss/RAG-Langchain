from pathlib import Path

from app.config import EXPECTED_OUTPUTS_DIR


def load_expected_output(file_name: str) -> str:
    file_path = EXPECTED_OUTPUTS_DIR / file_name

    if not file_path.exists():
        return ""

    return file_path.read_text(encoding="utf-8").strip()


def compare_outputs(generated_output: str, expected_output: str) -> dict:
    generated_lower = generated_output.lower().strip()
    expected_lower = expected_output.lower().strip()

    return {
        "expected_available": bool(expected_output),
        "exact_match": generated_lower == expected_lower,
        "generated_output": generated_output,
        "expected_output": expected_output,
    }
