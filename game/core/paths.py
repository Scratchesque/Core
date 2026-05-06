from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

# This file resolves the user directory path from a string

def _resolve_case_insensitive_part(parent: Path, child_name: str) -> Path:
    exact_match = parent / child_name
    if exact_match.exists():
        return exact_match

    child_name_lower = child_name.lower()
    for candidate in parent.iterdir():
        if candidate.name.lower() == child_name_lower:
            return candidate

    return exact_match

def resolve_project_path(relative_path: str) -> Path:
    current = PROJECT_ROOT
    for part in Path(relative_path).parts:
        current = _resolve_case_insensitive_part(current, part)

    return current
