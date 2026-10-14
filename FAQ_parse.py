"""Generate FAQPage JSON-LD from h3 questions and following paragraphs."""
import json

import requests
from bs4 import BeautifulSoup


def faq_schema(html):
    soup = BeautifulSoup(html, "html.parser")
    entities = []
    for heading in soup.find_all("h3"):
        question = heading.get_text(" ", strip=True)
        if not question.endswith("?"):
            continue
        paragraphs = []
        for sibling in heading.next_siblings:
            if sibling.name == "h3":
                break
            if sibling.name == "p":
                paragraphs.append(sibling.get_text(" ", strip=True))
        entities.append({"@type": "Question", "name": question,
                         "acceptedAnswer": {"@type": "Answer", "text": " ".join(paragraphs)}})
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": entities}


def render_faq(html):
    # Escaping '<' also prevents source text from terminating the script element.
    payload = json.dumps(faq_schema(html), ensure_ascii=False, indent=2).replace("<", "\\u003c")
    return '<script type="application/ld+json">\n' + payload + '\n</script>'


def validateJSON(jsondata):
    try:
        json.loads(jsondata)
        return True
    except (ValueError, TypeError):
        return False


def main():
    url = input("Input URL:\n").strip()
    response = requests.get(url, timeout=30)
    response.raise_for_status()
    print(render_faq(response.text))


if __name__ == "__main__":
    main()
