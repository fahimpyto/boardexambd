"""
PDF to Images Converter
=======================
- Run this file in any folder. It lists every PDF in that folder
  AND all its subfolders.
- Select a PDF by number, and each page becomes an image (1.png, 2.png, 3.png ...)
- Images are saved inside a new folder named after the PDF file.

Requires:  pip install PyMuPDF
"""

import os
import sys

try:
    import pymupdf as fitz  # PyMuPDF (new versions)
except ImportError:
    try:
        import fitz  # PyMuPDF (old versions)
    except ImportError:
        print("PyMuPDF is not installed. Install it with:")
        print("    pip install PyMuPDF")
        input("Press Enter to exit...")
        sys.exit(1)


# ---------------- Settings ----------------
IMAGE_FORMAT = "png"   # "png" or "jpeg"
ZOOM = 2.0             # scale factor (2.0 = good quality, ~150-200 DPI)
# -------------------------------------------


def find_pdfs():
    """Return all PDFs in the current folder and every subfolder."""
    pdfs = []
    for root, dirs, files in os.walk("."):
        for f in files:
            if f.lower().endswith(".pdf"):
                # Use a clean relative path for display (e.g. "pdf\my file.pdf")
                path = os.path.normpath(os.path.join(root, f))
                pdfs.append(path)
    pdfs.sort(key=str.lower)
    return pdfs


def list_pdfs(pdfs):
    print("\n================ PDF FILES ================")
    if not pdfs:
        print("No PDF files found in this folder or its subfolders!")
        return False
    for i, name in enumerate(pdfs, start=1):
        size_mb = os.path.getsize(name) / (1024 * 1024)
        print(f"  {i}.  {name}   ({size_mb:.2f} MB)")
    print("===========================================")
    return True


def choose_pdf(pdfs):
    """Ask the user to pick one PDF from the list."""
    while True:
        choice = input("\nEnter the number of the PDF to convert: ").strip()
        if choice.isdigit():
            num = int(choice)
            if 1 <= num <= len(pdfs):
                return pdfs[num - 1]
        print(f"Invalid choice. Please enter a number between 1 and {len(pdfs)}.")


def convert_pdf_to_images(pdf_path):
    """Convert every page of the PDF into an image inside a folder."""
    pdf_dir = os.path.dirname(pdf_path) or "."
    base_name = os.path.splitext(os.path.basename(pdf_path))[0]

    # Save the images folder in the SAME folder the PDF is in
    folder_name = os.path.join(pdf_dir, base_name)

    # Make the output folder (skip if it already exists)
    if os.path.isdir(folder_name):
        print(f"\nFolder already exists: '{folder_name}'")
        ans = input("Overwrite images inside it? (y/n): ").strip().lower()
        if ans != "y":
            print("Cancelled. No images were changed.")
            return
    else:
        os.makedirs(folder_name)
        print(f"Created folder: '{folder_name}'")

    print("\nOpening PDF...")
    doc = fitz.open(pdf_path)
    total = doc.page_count
    print(f"Total pages: {total}")
    print("Converting...")

    matrix = fitz.Matrix(ZOOM, ZOOM)  # zoom for higher quality

    for page_num in range(total):
        page = doc.load_page(page_num)
        pix = page.get_pixmap(matrix=matrix, alpha=False)

        # Save image with simple name: 1, 2, 3 ...
        # (e.g. "invoices.pdf" -> "invoices/1.png")
        image_path = os.path.join(folder_name, f"{page_num + 1}.{IMAGE_FORMAT}")
        if IMAGE_FORMAT == "jpeg":
            pix.save(image_path, jpg_quality=92)
        else:
            pix.save(image_path)

        print(f"  Page {page_num + 1}/{total}  ->  {folder_name}/{page_num + 1}.{IMAGE_FORMAT}")

    doc.close()
    print("\nDone! All images saved in folder:", folder_name)


def main():
    print("=" * 44)
    print("        PDF  ->  IMAGES CONVERTER")
    print("=" * 44)
    print("Working folder:", os.getcwd())

    pdfs = find_pdfs()
    if not list_pdfs(pdfs):
        input("\nPress Enter to exit...")
        return

    pdf_name = choose_pdf(pdfs)
    convert_pdf_to_images(pdf_name)
    input("\nPress Enter to exit...")


if __name__ == "__main__":
    main()
