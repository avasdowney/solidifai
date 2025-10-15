def extract_scad_blocks(text: str) -> list:
    """Extract all code blocks from a markdown-fenced string."""
    blocks = []
    parts = text.split("```")
    for i in range(1, len(parts), 2):
        block = parts[i].strip()
        if block:
            clean_block = _clean_scad(block)
            blocks.append(clean_block)
    return blocks


def _clean_scad(scad: str) -> str:
    return scad.replace("openscad", "").strip()
