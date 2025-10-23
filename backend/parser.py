import fitz  # PyMuPDF
import re
import json
import argparse
import sys
import os
from datetime import datetime

# ==============================================================================
# === UNIVERSAL PARSER WITH PRECISION PATTERNS (CORRECTED) ===
# ==============================================================================

class UniversalCCParser:
    """
    This final version uses highly specific regex patterns tailored to the observed
    output.txt format. It avoids greedy matching pitfalls by looking for values
    in the specific block where they appear after text extraction.
    """
    def __init__(self, text):
        self.text_with_newlines = text
        # We will also find all dates in the document once, as they appear in a reliable order.
        self._all_dates = re.findall(r'(\d{1,2}\s\w{3}\s\d{4})', self.text_with_newlines)

    def _search(self, pattern, text=None):
        """Helper to search and return a cleaned group, using DOTALL and IGNORECASE."""
        if text is None:
            text = self.text_with_newlines
        
        match = re.search(pattern, text, re.DOTALL | re.IGNORECASE)
        if match:
            return match.group(1).replace(',', '').strip()
        return None

    def extract_all_data(self):
        """Extract all details using precision patterns."""
        return {
            'card_holder_name': self.extract_card_holder(),
            'card_number_last_4': self.extract_last_four(),
            'statement_date': self.extract_statement_date(),
            'payment_due_date': self.extract_payment_due_date(),
            'total_amount_due': self.extract_total_due(),
            'minimum_amount_due': self.extract_minimum_due(),
            'credit_limit': self.extract_credit_limit(),
            'available_credit': self.extract_available_credit(),
            'billing_period': self.extract_billing_period(),
            'account_number': self.extract_account_number(),
        }

    def extract_card_holder(self):
        return self._search(r'TRANSACTIONS FOR\s+([A-Z\s]{5,}[A-Z])')

    def extract_last_four(self):
        return self._search(r'XXXX\s+XXXX\s+XXXX\s+XX(\d{2})')

    def extract_account_number(self):
        # CORRECTED: Added '.*?' to span newlines between 'No.' and the colon.
        return self._search(r'STMT No\..*?:\s*([A-Z0-9]+)')

    def extract_billing_period(self):
        return self._search(r'for Statement Period:\s*(.*?)\n')

    def extract_total_due(self):
        # This pattern is reliable because it's the first one.
        return self._search(r'\*Total Amount Due.*?\n([\d,]+\.\d{2})')

    def extract_minimum_due(self):
        # CORRECTED: A more specific, non-greedy pattern.
        return self._search(r'\*\*Minimum Amount Due.*?([\d,]+\.\d{2})')

    def extract_credit_limit(self):
        # CORRECTED: This pattern is now more specific to avoid grabbing the wrong value.
        return self._search(r'Credit Limit.*?\( ` \).*?([\d,]+\.\d{2})')

    def extract_available_credit(self):
        # CORRECTED: More specific pattern.
        return self._search(r'Available Credit Limit.*?\( ` \).*?([\d,]+\.\d{2})')

    def extract_statement_date(self):
        # CORRECTED: We take the first date found in the pre-compiled list of all dates.
        return self._all_dates[0] if len(self._all_dates) > 0 else None
        
    def extract_payment_due_date(self):
        # CORRECTED: We take the second date found in the pre-compiled list.
        return self._all_dates[1] if len(self._all_dates) > 1 else None


# ==============================================================================
# === HELPER AND MAIN FUNCTIONS (No changes needed below this line) ===
# ==============================================================================

def extract_text_from_pdf(pdf_path):
    if not os.path.exists(pdf_path):
        print(f"ERROR: File not found at path: {pdf_path}", file=sys.stderr)
        return None
    try:
        doc = fitz.open(pdf_path)
        text = "".join(page.get_text("text") for page in doc)
        doc.close()
        return text
    except Exception as e:
        print(f"ERROR: An exception occurred while reading the PDF: {e}", file=sys.stderr)
        return None

def clean_output(data):
    cleaned = {}
    for key, value in data.items():
        if value:
            cleaned[key] = value
        else:
            cleaned[key] = None
    return cleaned

def main():
    parser = argparse.ArgumentParser(
        description="Universal credit card statement parser with precision patterns."
    )
    parser.add_argument("pdf_path", help="Path to the credit card statement PDF file.")
    parser.add_argument(
        "--dump-text",
        action="store_true",
        help="Extract and save raw text to 'output.txt' for debugging."
    )
    
    args = parser.parse_args()

    statement_text = extract_text_from_pdf(args.pdf_path)
    if not statement_text:
        sys.exit(1)

    if args.dump_text:
        with open("output.txt", "w", encoding="utf-8") as f:
            f.write(statement_text)
        print("Successfully dumped extracted text to 'output.txt'")
        sys.exit(0)

    parser_obj = UniversalCCParser(statement_text)
    extracted_data = parser_obj.extract_all_data()
    final_data = clean_output(extracted_data)
    
    final_data['parsing_method'] = 'universal_precision'
    final_data['extraction_timestamp'] = datetime.now().isoformat()
    
    print(json.dumps(final_data, indent=4, ensure_ascii=False))

if __name__ == "__main__":
    main()