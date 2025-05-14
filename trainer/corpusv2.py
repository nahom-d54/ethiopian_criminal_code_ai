import pymupdf
import re
import unicodedata  # For cleaning non-breaking spaces, etc.
import json


def clean_text(text):
    """Basic text cleaning."""
    text = unicodedata.normalize("NFKD", text)  # Normalize unicode
    text = re.sub(r"\s+", " ", text)  # Replace multiple whitespace with single space
    return text.strip()


def extract_law_structure_pymupdf(pdf_path):
    documents = []

    current_book = ""
    current_book_name = ""
    current_chapter = ""
    current_chapter_name = ""
    current_title = ""
    current_title_name = ""
    current_section = ""
    current_section_name = ""
    current_article_number = ""
    current_article_name = ""
    current_article_lines = []

    # Regex patterns (same as before, ensure they are robust)
    book_pattern = re.compile(r"^\s*BOOK\s+([IVXLCDM]+)\s*$", re.IGNORECASE)
    chapter_pattern = re.compile(r"^\s*CHAPTER\s+([IVXLCDM]+)\s*$", re.IGNORECASE)
    title_pattern = re.compile(r"^\s*TITLE\s+([IVXLCDM]+)\s*$", re.IGNORECASE)
    section_pattern = re.compile(r"^\s*Section\s+([IVXLCDM\d]+)\s*[:.-]", re.IGNORECASE)
    article_pattern = re.compile(r"^\s*Article\s+(\d+)\s*[:.-]", re.IGNORECASE)

    expecting_book_name = False
    expecting_chapter_name = False
    expecting_title_name = False
    expecting_section_name = False

    def finalize_current_article():
        nonlocal \
            current_article_lines, \
            current_article_number, \
            current_article_name, \
            current_book, \
            current_book_name, \
            current_chapter, \
            current_chapter_name, \
            current_title, \
            current_title_name, \
            current_section, \
            current_section_name

        if current_article_number and current_article_lines:
            content = " ".join(
                clean_text(line) for line in current_article_lines if clean_text(line)
            )
            if content:
                documents.append(
                    {
                        "book_roman": current_book,
                        "book_name": clean_text(current_book_name),
                        "chapter_roman": current_chapter,
                        "chapter_name": clean_text(current_chapter_name),
                        "title_roman": current_title,
                        "title_name": clean_text(current_title_name),
                        "section_roman_or_arabic": current_section,
                        "section_name": clean_text(current_section_name),
                        "article_number": current_article_number,
                        "article_name": clean_text(current_article_name),
                        "content": content,
                    }
                )
        current_article_lines = []
        # current_article_number = "" # Resetting these here means an article name on its own line won't be captured if it's the *first* thing
        # current_article_name = "" # Let's reset these when a *new* article is found, not just when finalizing.
        # Or rather, the reset for number and name should happen when a *new* article is *started*.
        # The current logic: finalize_current_article is called, then new article details are set. This is okay.
        # What finalize_current_article *should* do is ensure its own state (lines, number, name) is cleared for the *next potential* accumulation if not immediately followed by a new Article marker.
        # For this structure, it's fine as `current_article_number` and `name` are reassigned upon matching a new Article.

    doc = pymupdf.open(pdf_path)
    for page_num, page in enumerate(doc):
        page_height = page.rect.height
        # Get text blocks, sorted by vertical position, then horizontal.
        # This usually gives a good reading order.
        blocks = page.get_text("blocks", sort=True)

        for b_x0, b_y0, b_x1, b_y1, block_text_content, block_no, block_type in blocks:
            if block_type != 0:  # 0 indicates a text block
                continue

            # Simple header/footer filtering for blocks that are likely page numbers
            # Check if the block is near the bottom and contains only digits
            # Threshold: e.g., bottom 7% of the page height
            is_potential_footer = (page_height - b_y1) < (page_height * 0.07)
            block_text_cleaned_for_page_num = block_text_content.strip()
            if is_potential_footer and block_text_cleaned_for_page_num.isdigit():
                # print(f"Skipping page number block: '{block_text_cleaned_for_page_num}' on page {page_num+1}")
                continue

            # More general header/footer zone skipping (optional, can be too aggressive)
            # if b_y0 < page_height * 0.05 or b_y1 > page_height * 0.93: # Top 5%, Bottom 7%
            #     # Be careful not to skip content that happens to be in these zones
            #     # print(f"Skipping block in header/footer zone: {block_text_content[:30]}...")
            #     continue

            lines_in_block = block_text_content.split("\n")
            for line_text_raw in lines_in_block:
                line = clean_text(line_text_raw)  # Clean each line from the block
                if not line:
                    continue

                # --- Core Parsing Logic (largely same as pdfplumber version) ---
                book_match = book_pattern.match(line)
                chapter_match = chapter_pattern.match(line)
                title_match = title_pattern.match(line)
                section_match = section_pattern.match(line)
                article_match = article_pattern.match(line)

                if book_match:
                    finalize_current_article()
                    current_book = book_match.group(1)
                    current_chapter = ""
                    current_title = ""
                    current_section = ""
                    current_book_name = ""
                    current_chapter_name = ""
                    current_title_name = ""
                    current_section_name = ""
                    current_article_number = (
                        ""  # Also reset article when new book starts
                    )
                    current_article_name = ""
                    expecting_book_name = True
                    expecting_chapter_name = False
                    expecting_title_name = False
                    expecting_section_name = False
                    continue
                elif chapter_match:
                    finalize_current_article()
                    current_chapter = chapter_match.group(1)
                    current_title = ""
                    current_section = ""
                    current_chapter_name = ""
                    current_title_name = ""
                    current_section_name = ""
                    current_article_number = ""  # Also reset article
                    current_article_name = ""
                    expecting_book_name = False
                    expecting_chapter_name = True
                    expecting_title_name = False
                    expecting_section_name = False
                    continue
                elif title_match:
                    finalize_current_article()
                    current_title = title_match.group(1)
                    current_section = ""
                    current_title_name = ""
                    current_section_name = ""
                    current_article_number = ""  # Also reset article
                    current_article_name = ""
                    expecting_book_name = False
                    expecting_chapter_name = False
                    expecting_title_name = True
                    expecting_section_name = False
                    continue
                elif section_match:
                    finalize_current_article()
                    current_section = section_match.group(1)
                    current_section_name = (
                        line[section_match.end() :].strip().lstrip(".- ").strip()
                    )
                    current_article_number = ""  # Also reset article
                    current_article_name = ""
                    expecting_book_name = False
                    expecting_chapter_name = False
                    expecting_title_name = False
                    if not current_section_name:
                        expecting_section_name = True
                    else:
                        expecting_section_name = False
                    continue
                elif article_match:
                    finalize_current_article()  # Finalize previous article
                    current_article_number = article_match.group(1)
                    current_article_name = (
                        line[article_match.end() :].strip().lstrip(".- ").strip()
                    )
                    current_article_lines = []  # Reset for new article's content
                    expecting_book_name = False
                    expecting_chapter_name = False
                    expecting_title_name = False
                    expecting_section_name = False
                    continue

                # If we are expecting a name for Book/Chapter/Title/Section
                is_structural_line = bool(
                    book_match
                    or chapter_match
                    or title_match
                    or section_match
                    or article_match
                )

                if expecting_book_name and not is_structural_line:
                    current_book_name = (current_book_name + " " + line).strip()
                    if line.isupper():
                        pass  # Continue if all caps (heuristic for multi-line titles)
                    else:
                        expecting_book_name = False
                    continue
                elif expecting_chapter_name and not is_structural_line:
                    current_chapter_name = (current_chapter_name + " " + line).strip()
                    if line.isupper():
                        pass
                    else:
                        expecting_chapter_name = False
                    continue
                elif expecting_title_name and not is_structural_line:
                    current_title_name = (current_title_name + " " + line).strip()
                    if line.isupper():
                        pass
                    else:
                        expecting_title_name = False
                    continue
                elif expecting_section_name and not is_structural_line:
                    current_section_name = (current_section_name + " " + line).strip()
                    expecting_section_name = (
                        False  # Assume section names are usually one line after marker
                    )
                    continue

                # Accumulate article content
                if current_article_number:
                    # If current_article_name is still empty (wasn't on the "Article X.-" line)
                    # and this line looks like a title (e.g. starts with capital, few words)
                    # and it's the first line collected for this article.
                    if (
                        not current_article_name
                        and re.match(r"^[A-Z][a-zA-Z\s,.'()-]+$", line)
                        and len(line.split()) < 10
                        and not current_article_lines
                    ):
                        current_article_name = line
                    else:
                        current_article_lines.append(
                            line_text_raw
                        )  # Append raw line to preserve original spacing for joining
                elif (
                    current_section
                    and not current_section_name
                    and not is_structural_line
                    and not expecting_section_name
                ):
                    # This case might be redundant due to expecting_section_name logic, but can be a fallback
                    if (
                        re.match(r"^[A-Z][a-zA-Z\s,.'()-]+$", line)
                        and len(line.split()) < 10
                    ):  # Heuristic for section name
                        current_section_name = line
                # --- End of Core Parsing Logic ---

    finalize_current_article()  # Finalize the very last article after all pages
    doc.close()
    return documents


# --- Main execution (similar to before, for testing) ---
if __name__ == "__main__":
    pdf_file = "C:\\Users\\nahom\\Desktop\\assignment\\ET_Criminal_Code.pdf"

    try:
        documents = extract_law_structure_pymupdf(pdf_file)

        if documents:
            for i, doc_item in enumerate(documents):
                print(f"--- Document {i + 1} ---")
                print(f"  Book: {doc_item['book_roman']} ({doc_item['book_name']})")
                print(
                    f"  Chapter: {doc_item['chapter_roman']} ({doc_item['chapter_name']})"
                )
                print(f"  Title: {doc_item['title_roman']} ({doc_item['title_name']})")
                print(
                    f"  Section: {doc_item['section_roman_or_arabic']} ({doc_item['section_name']})"
                )
                print(
                    f"  Article: {doc_item['article_number']} ({doc_item['article_name']})"
                )
                print(f"  Content: {doc_item['content'][:200]}...")
                print("-" * 20)
                break
            with open("corpus-v2-out.json", "w") as f:
                json.dump(documents, f, indent=4)
                print("Documents saved to corpus-v2-out.json")
        else:
            print("No documents extracted. Check PDF content and parsing logic.")

    except pymupdf.FileNotFoundError:
        print(
            f"ERROR: PDF file '{pdf_file}' not found. Please ensure it exists in the correct path."
        )
    except Exception as e:
        print(f"An error occurred during PDF processing: {e}")
        print(
            "Ensure 'PyMuPDF' (import pymupdf) and 'reportlab' (for dummy PDF) are installed."
        )
