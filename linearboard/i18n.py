"""Translate application errors at the HTTP boundary without changing stored data."""
import json
from pathlib import Path
import re

ENGLISH = json.loads((Path(__file__).parent / 'locales/en.json').read_text())
PATTERNS = []
for source, target in ENGLISH.items():
    if '{0}' in source:
        before, after = source.split('{0}')
        PATTERNS.append((re.compile(re.escape(before) + '(.*?)' + re.escape(after), re.DOTALL), target))


def preferred_language(header=''):
    """Respect quality values and explicit exclusions; preserve the API's Chinese default."""
    choices = []
    for position, item in enumerate(header.split(',')):
        parts = item.strip().split(';')
        tag = parts[0].strip().lower()
        quality = 1.0
        try:
            for parameter in parts[1:]:
                if parameter.strip().startswith('q='):
                    quality = float(parameter.strip()[2:])
        except ValueError:
            continue
        if not 0 < quality <= 1:
            continue
        if tag == 'en' or tag.startswith('en-'):
            choices.append((quality, -position, 'en'))
        elif tag == 'zh' or tag.startswith('zh-'):
            choices.append((quality, -position, 'zh-TW'))
    return max(choices)[2] if choices else 'zh-TW'


def translate_error(message, language):
    if language != 'en':
        return message
    if message in ENGLISH:
        return ENGLISH[message]
    for pattern, target in PATTERNS:
        match = pattern.fullmatch(message)
        if match:
            return target.replace('{0}', match.group(1))
    return message
