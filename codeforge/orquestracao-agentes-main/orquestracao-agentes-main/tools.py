import re
from pathlib import Path

BASE_DIR = Path("generated_app")


def ensure_project_directory():
    BASE_DIR.mkdir(parents=True, exist_ok=True)


def write_file(filename, content):
    ensure_project_directory()

    path = BASE_DIR / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.strip(), encoding="utf-8")

    return f"Arquivo criado: {path}"


def read_file(filename):
    path = BASE_DIR / filename

    if not path.exists():
        return f"Arquivo não encontrado: {filename}"

    return path.read_text(encoding="utf-8")


def list_files():
    ensure_project_directory()

    files = []

    for path in BASE_DIR.rglob("*"):
        if path.is_file():
            files.append(str(path.relative_to(BASE_DIR)))

    return files


def save_generated_code(response):
    ensure_project_directory()

    pattern = r"FILE:\s*(.+?)\n(.*?)(?=\nFILE:|\Z)"
    matches = re.findall(pattern, response, re.DOTALL)

    created = []

    for filename, content in matches:
        filename = filename.strip()
        content = content.strip()

        # Remove blocos Markdown de código,
        # caso o modelo tenha usado ```html, ```css etc.
        content = re.sub(r"^```[a-zA-Z0-9_+-]*\s*\n", "", content)
        content = re.sub(r"\n```\s*$", "", content)

        write_file(filename, content)
        created.append(filename)

    return created