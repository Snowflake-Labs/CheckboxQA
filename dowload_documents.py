import argparse
import json
from logging import warn

import requests
from pathlib import Path

from PyPDF2 import PdfWriter, PdfReader
from tqdm import tqdm


def extract_pages(pdf_path, pages):
    reader = PdfReader(str(pdf_path))
    writer = PdfWriter()

    for page_num in pages:
        writer.add_page(reader.pages[page_num - 1])  # Page numbers are 1-based in the JSON

    with open(pdf_path, 'wb') as output_pdf:
        writer.write(output_pdf)

def download_pdfs(json_path, out_dir):
    out_dir.mkdir(parents=True, exist_ok=True)

    # Read the JSON file
    with open(json_path, 'r') as file:
        data = json.load(file)

    # Iterate over the entries and download the PDFs
    for key, value in tqdm(data.items()):
        pdf_url = value['pdf_url']
        pdf_response = requests.get(pdf_url)
        if pdf_response.status_code == 200:
            pdf_path = out_dir / f"{key}.pdf"
            with open(pdf_path, 'wb') as pdf_file:
                pdf_file.write(pdf_response.content)
            if 'pages' in value and value['pages']:
                extract_pages(pdf_path, value['pages'])
        else:
            warn(f"Failed to download {pdf_url}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Download pdf files.')
    parser.add_argument('--out_dir', type=Path, default='./data/documents',
                        help='Where to store the downloaded pdfs')
    parser.add_argument('--json_path', type=Path, default='./data/document_url_map.json',
                        help='Path to the JSON file containing the document URL map')
    args = parser.parse_args()
    download_pdfs(args.json_path, args.out_dir)