import re

from app.config import EXPECTED_OUTPUTS_DIR


def load_expected_output(file_name: str) -> str:
    file_path = EXPECTED_OUTPUTS_DIR / file_name

    if not file_path.exists():
        return ""

    return file_path.read_text(encoding="utf-8").strip()


def normalize_text(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text


def parse_sources(source_text: str) -> list[str]:
    if not source_text.strip():
        return []

    return [source.strip().lower() for source in source_text.split(",") if source.strip()]


def parse_output_fields(output_text: str) -> dict:
    parsed_fields = {
        "issue_category": "",
        "likely_cause": "",
        "recommended_next_step": "",
        "sources": "",
    }

    for line in output_text.splitlines():
        line = line.strip()

        if line.startswith("Issue Category:"):
            parsed_fields["issue_category"] = line.replace("Issue Category:", "", 1).strip()
        elif line.startswith("Likely Cause:"):
            parsed_fields["likely_cause"] = line.replace("Likely Cause:", "", 1).strip()
        elif line.startswith("Recommended Next Step:"):
            parsed_fields["recommended_next_step"] = line.replace("Recommended Next Step:", "", 1).strip()
        elif line.startswith("Sources:"):
            parsed_fields["sources"] = line.replace("Sources:", "", 1).strip()
        elif line.startswith("Key Sources:"):
            parsed_fields["sources"] = line.replace("Key Sources:", "", 1).strip()

    return parsed_fields


def compute_source_overlap(generated_sources: str, expected_sources: str) -> dict:
    generated_set = set(parse_sources(generated_sources))
    expected_set = set(parse_sources(expected_sources))

    if not expected_set:
        return {
            "overlap_count": 0,
            "expected_count": 0,
            "coverage_ratio": 0.0,
            "all_expected_present": False,
        }

    overlap_count = len(generated_set.intersection(expected_set))
    coverage_ratio = overlap_count / len(expected_set)

    return {
        "overlap_count": overlap_count,
        "expected_count": len(expected_set),
        "coverage_ratio": coverage_ratio,
        "all_expected_present": expected_set.issubset(generated_set),
    }


def compare_outputs(generated_output: str, expected_output: str) -> dict:
    if not expected_output:
        return {
            "expected_available": False,
            "exact_match": False,
            "normalized_field_matches": {},
            "exact_field_matches": {},
            "source_overlap": {},
            "generated_fields": parse_output_fields(generated_output),
            "expected_fields": {},
            "generated_output": generated_output,
            "expected_output": expected_output,
        }

    generated_normalized = normalize_text(generated_output)
    expected_normalized = normalize_text(expected_output)

    generated_fields = parse_output_fields(generated_output)
    expected_fields = parse_output_fields(expected_output)

    exact_field_matches = {
        "issue_category": generated_fields["issue_category"].lower() == expected_fields["issue_category"].lower(),
        "likely_cause": generated_fields["likely_cause"].lower() == expected_fields["likely_cause"].lower(),
        "recommended_next_step": generated_fields["recommended_next_step"].lower() == expected_fields["recommended_next_step"].lower(),
        "sources": generated_fields["sources"].lower() == expected_fields["sources"].lower(),
    }

    normalized_field_matches = {
        "issue_category": normalize_text(generated_fields["issue_category"]) == normalize_text(expected_fields["issue_category"]),
        "likely_cause": normalize_text(generated_fields["likely_cause"]) == normalize_text(expected_fields["likely_cause"]),
        "recommended_next_step": normalize_text(generated_fields["recommended_next_step"]) == normalize_text(expected_fields["recommended_next_step"]),
        "sources": normalize_text(generated_fields["sources"]) == normalize_text(expected_fields["sources"]),
    }

    source_overlap = compute_source_overlap(
        generated_fields["sources"],
        expected_fields["sources"],
    )

    return {
        "expected_available": True,
        "exact_match": generated_output.lower().strip() == expected_output.lower().strip(),
        "normalized_match": generated_normalized == expected_normalized,
        "exact_field_matches": exact_field_matches,
        "normalized_field_matches": normalized_field_matches,
        "source_overlap": source_overlap,
        "generated_fields": generated_fields,
        "expected_fields": expected_fields,
        "generated_output": generated_output,
        "expected_output": expected_output,
    }
