#!/usr/bin/env python3
"""
Regenerate the FAQPage JSON-LD block in index.html from the visible
.faq-item markup for more convenient editing.

Usage: ./tools/regen-faq-jsonld.py   (run from repo root)
"""

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path

INDEX_PATH = Path(__file__).resolve().parent.parent / "index.html"


class FAQExtractor(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.items = []
        self._depth = None  # nesting depth of the current .faq-item's answer div, or None
        self._in_question = False
        self._question = []
        self._answer_parts = []

    def handle_starttag(self, tag, attrs):
        classes = dict(attrs).get("class", "").split()
        if tag == "div" and "faq-item" in classes:
            self._question = []
            self._answer_parts = []
        elif tag in ("p", "div") and "faq-q" in classes:
            self._in_question = True
        elif tag in ("p", "div") and "faq-a" in classes:
            self._depth = 0
        elif self._depth is not None:
            self._depth += 1
            if tag == "a":
                self._answer_parts.append(" ")

    def handle_endtag(self, tag):
        if self._in_question and tag in ("p", "div"):
            self._in_question = False
        elif self._depth is not None:
            if self._depth == 0:
                answer = " ".join(" ".join(self._answer_parts).split())
                question = " ".join(" ".join(self._question).split())
                if question and answer:
                    self.items.append((question, answer))
                self._depth = None
            else:
                self._depth -= 1
                if tag in ("p", "li"):
                    self._answer_parts.append(" ")

    def handle_data(self, data):
        if self._in_question:
            self._question.append(data)
        elif self._depth is not None:
            self._answer_parts.append(data)


def build_jsonld(items):
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": question,
                "acceptedAnswer": {"@type": "Answer", "text": answer},
            }
            for question, answer in items
        ],
    }


def main():
    html = INDEX_PATH.read_text()

    faq_section_match = re.search(
        r'<div class="faq">.*?</div>\s*(?=</section>)', html, re.DOTALL
    )
    if not faq_section_match:
        sys.exit("regen-faq-jsonld: could not find <div class=\"faq\">...</div>")

    parser = FAQExtractor()
    parser.feed(faq_section_match.group(0))
    if not parser.items:
        sys.exit("regen-faq-jsonld: found no .faq-item entries")

    jsonld = build_jsonld(parser.items)
    new_script = (
        '<script type="application/ld+json">\n'
        + json.dumps(jsonld, indent=4)
        + "\n</script>"
    )

    script_pattern = re.compile(
        r'<script type="application/ld\+json">\s*\{\s*"@context":\s*"https://schema\.org".*?</script>',
        re.DOTALL,
    )
    new_html, count = script_pattern.subn(lambda _: new_script, html, count=1)
    if count != 1:
        sys.exit("regen-faq-jsonld: could not find existing FAQPage JSON-LD block")

    INDEX_PATH.write_text(new_html)
    print(f"regen-faq-jsonld: wrote {len(parser.items)} questions to {INDEX_PATH.name}")


if __name__ == "__main__":
    main()
