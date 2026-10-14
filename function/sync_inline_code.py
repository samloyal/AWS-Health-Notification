import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SOURCE = ROOT / "function" / "lambda_function.py"
TEMPLATE = ROOT / "CNPhDCentral.yaml"
BLOCK_START = "        ZipFile: |\n"
INDENT = " " * 10


def is_resource_key(line: str) -> bool:
    return line.startswith("  ") and not line.startswith("   ") and bool(line.strip())


def sync(template: str, source: str) -> str:
    head, _, tail = template.partition(BLOCK_START)
    lines = tail.splitlines(keepends=True)
    end = next(i for i, line in enumerate(lines) if is_resource_key(line))
    block = lines[:end]
    trailing = []
    while block and not block[-1].strip():
        trailing.insert(0, block.pop())
    inline = "".join(INDENT + line if line.strip() else "\n" for line in source.splitlines(keepends=True))
    return head + BLOCK_START + inline + "".join(trailing) + "".join(lines[end:])


def main() -> int:
    source = SOURCE.read_text(encoding="utf-8")
    template = TEMPLATE.read_text(encoding="utf-8")
    updated = sync(template, source)
    if "--check" in sys.argv:
        if updated != template:
            print("CNPhDCentral.yaml inline code is stale; run function/sync_inline_code.py")
            return 1
        print("inline code is in sync")
        return 0
    TEMPLATE.write_text(updated, encoding="utf-8")
    print("updated CNPhDCentral.yaml")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
