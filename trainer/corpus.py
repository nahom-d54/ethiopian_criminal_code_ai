import pdfplumber
import re
# Optional: Save to JSON
import json

with pdfplumber.open("ET_Criminal_Code.pdf") as pdf:
    raw_lines = []
    for page in pdf.pages:
        raw_lines.extend(page.extract_text().splitlines())



faiss_docs = []

current_book = current_title = current_chapter = None
current_article = None
buffer = []

def flush_article():
    if current_article and buffer:
        current_article["content"] = " ".join(buffer).strip()
        faiss_docs.append(current_article)

for line in raw_lines:
    line = line.strip()

    # BOOK
    if re.match(r"^BOOK\s+[IVXLCDM]+", line, re.IGNORECASE):
        flush_article()
        current_book = line
        current_title = current_chapter = None
        current_article = None
        buffer = []
    
    # TITLE
    elif line.startswith("TITLE"):
        flush_article()
        current_title = line
        current_chapter = None
        current_article = None
        buffer = []

    # CHAPTER
    elif line.startswith("CHAPTER"):
        flush_article()
        current_chapter = line
        current_article = None
        buffer = []

    # ARTICLE
    elif re.match(r"^Article\s+\d+\.-", line):
        flush_article()
        article_num = re.search(r"(Article\s+\d+\.-)", line).group(1)
        title = line.split(article_num)[-1].strip()
        current_article = {
            "id": article_num,
            "title": title,
            "content": "",
            "book": current_book,
            "title_group": current_title,
            "chapter": current_chapter
        }
        buffer = []

    # CONTENT
    elif line and current_article:
        buffer.append(line)

# Flush the last one
flush_article()

# Save to JSON
with open("faiss_articles.json", "w", encoding="utf-8") as f:
    json.dump(faiss_docs, f, ensure_ascii=False, indent=2)