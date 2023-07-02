"""
pd.py foo.pdf > foo.txt
    Extract text from 365DayBibleReadingPlan PDF file and print it
    to stdout.  Note that this script produces extraneous text. The
    output must be manually edited to remove the extraneous text.
"""

from pypdf import PdfReader, PageObject
import sys
import argparse
from pprint import pprint
from re import match, findall
from csv import writer as csv_writer

def extract_from_page(page: PageObject) -> list[str]:
    """finds all verses in a page

    Args:
        page (PageObject): One page from a PDF file

    Returns:
        list[str]: all of the strings that look like verse references
    """
    result = []

    def visitor_text(text, cm, tm, font, font_size):
        verses = findall(r'^[A-Z0-9][-A-Z0-9:, ]+', text)
        if(verses and len(verses[0]) > 2):
            result.append(verses[0].title())

    page.extract_text(visitor_text=visitor_text)
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Extract text from PDF file and print it to stdout.')
    parser.add_argument(
        'filename', 
        metavar='filename', 
        type=str, 
        nargs=1, 
        help='PDF file to extract text from')
    args = parser.parse_args()

    writer = csv_writer(sys.stdout)
    for page in PdfReader(args.filename[0]).pages:
        writer.writerow(extract_from_page(page))