import pdfplumber
import pandas as pd

def extract_rows_from_pdf(pdf_path, output_excel_path):
    rows = []

    with pdfplumber.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf.pages):
            print(f"Processing page {page_number + 1}...")

            words = page.extract_words(x_tolerance=2, y_tolerance=2, keep_blank_chars=True, use_text_flow=True)

            # Group words by y-coordinate
            lines = {}
            for word in words:
                y = round(word['top'], 1)  # Group by rounded vertical position
                if y not in lines:
                    lines[y] = []
                lines[y].append((word['x0'], word['text']))

            # Sort lines by Y position (top to bottom)
            for y in sorted(lines.keys()):
                line = sorted(lines[y], key=lambda x: x[0])  # sort left to right
                row_text = [text for _, text in line]
                rows.append(row_text)

    # Convert to DataFrame
    df = pd.DataFrame(rows)
    df.dropna(how='all', inplace=True)

    # Save to Excel
    df.to_excel(output_excel_path, index=False, header=False)
    print(f"\n✅ Extracted text table saved to '{output_excel_path}'")

# Run it
extract_rows_from_pdf("test3.pdf", "outputable.xlsx")
