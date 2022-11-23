"""
Create a script that will take a URL, get the HTML from the URL, parse the HTML and generate
FAQpage schema.org markup

The questions are in <h3> tags that end in a "?", the answers are in the sibling <p> tags until the next <h3> tag.
"""

import requests
from bs4 import BeautifulSoup
import json

# Get the HTML from the URL
print("Input URL:")
url = input()
r = requests.get(url)
html = r.text

# Parse the HTML
soup = BeautifulSoup(html, "html.parser")


# Get the questions and answers, turn them into plain text removing all formatting, turn punctuation in the answers into HTML entities

questions = []
answers = []
for h3 in soup.find_all("h3"):
    if h3.text.endswith("?"):
        questions.append(h3.text)
        answer = ""
        for sibling in h3.next_siblings:
            if sibling.name == "h3":
                break
            if sibling.name == "p":
                answer += sibling.text
        answers.append(answer)

# Turn the punctuation in the answers into HTML entities
answers = [a.replace("?", "&quest;") for a in answers]
answers = [a.replace("!", "&excl;") for a in answers]
answers = [a.replace(".", "&period;") for a in answers]
answers = [a.replace('"', "&quot;") for a in answers]

# Create the FAQPage schema.org markup
# Create the FAQPage schema.org markup
faqpage = """<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
"""

# Create the question and answer markup

for i in range(len(questions)):
    faqpage += """    {
      "@type": "Question",
      "name": "%s",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "%s"
      }
    },
""" % (
        questions[i],
        answers[i],
    )

# Remove the last comma
faqpage = faqpage[:-2]

# Close the FAQPage schema.org markup
faqpage += """  ]
}
</script>"""

# validate the json


def validateJSON(jsondata):
    try:
        json.loads(jsondata)
    except ValueError as err:
        return False
    return True


validation = validateJSON(faqpage)

if validation == True:
    print(faqpage)
else:
    print("The generated JSON is not valid")


# # Print the FAQPage schema.org markup
# print(faqpage)
