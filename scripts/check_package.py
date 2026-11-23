#!/usr/bin/env python3
"""Read-only public package validation; no network or customer processing."""
from pathlib import Path
from urllib.parse import unquote
import re
import sys

def check(root):
    errors = []
    required = ['SKILL.md', 'README.md', 'README_EN.md', 'VERSION', 'LICENSE',
                'references/四步工作流.md', 'templates/README.md', 'assets/workflow.svg',
                'agents/openai.yaml', 'repository-publication-manifest.yaml', 'repository-audit-report.md']
    for name in required:
        if not (root / name).is_file():
            errors.append('missing: ' + name)
    skill = (root / 'SKILL.md').read_text(encoding='utf-8')
    if not skill.startswith('---\nname: export-buyer-discovery\n'):
        errors.append('invalid skill name/frontmatter')
    version = (root / 'VERSION').read_text().strip()
    if not re.fullmatch(r'\d+\.\d+\.\d+(?:-[a-zA-Z0-9.]+)?', version):
        errors.append('invalid VERSION')
    patterns = [r'/Users/[^\s]+', r'/home/[^\s]+', r'\b(?:ghp_|gho_|github_pat_)[A-Za-z0-9_]{16,}\b',
                r'\bsk-[A-Za-z0-9_-]{16,}\b', r'\bBearer\s+[A-Za-z0-9._-]{16,}\b']
    for path in root.rglob('*'):
        rel = path.relative_to(root)
        if any(p.startswith('.') for p in rel.parts) or not path.is_file():
            continue
        if path.suffix not in {'.md', '.yaml', '.yml', '.csv', '.svg', '.json'}:
            continue
        text = path.read_text(encoding='utf-8')
        for pattern in patterns:
            if re.search(pattern, text):
                errors.append('sensitive pattern: ' + str(rel))
        if path.suffix == '.md':
            for raw in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)', text):
                target = raw.strip().split('#',1)[0]
                if not target or target.startswith(('https://','http://','mailto:')):
                    continue
                dest = (path.parent / unquote(target)).resolve()
                if not dest.is_relative_to(root.resolve()) or not dest.exists():
                    errors.append('invalid local link: ' + str(rel) + ' -> ' + target)
    if 'Apache License' not in (root / 'LICENSE').read_text():
        errors.append('license is not Apache-2.0')
    if version not in (root / 'README.md').read_text() or version not in (root / 'README_EN.md').read_text():
        errors.append('README version mismatch')
    return errors

if __name__ == '__main__':
    result = check(Path(__file__).resolve().parents[1])
    print('Package check: ' + ('PASS' if not result else 'FAIL'))
    for error in result:
        print(error)
    sys.exit(bool(result))
