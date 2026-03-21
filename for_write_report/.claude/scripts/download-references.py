#!/usr/bin/env python3
"""
Reference Paper Downloader for Research Reports
Automatically downloads PDFs of cited papers from various sources
Also converts web pages to PDFs
"""

import os
import re
import sys
import json
import time
import argparse
import subprocess
import shutil
from pathlib import Path
from urllib.parse import quote, urljoin, urlparse
from urllib.request import urlopen, Request
from urllib.error import HTTPError, URLError

class ReferenceDownloader:
    def __init__(self, output_dir="references/papers", verbose=True, convert_webpages=True):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.verbose = verbose
        self.convert_webpages = convert_webpages
        self.downloaded = []
        self.failed = []
        self.webpages = []  # Track web page URLs

        # User agent to avoid blocking
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36'
        }

        # Check for wkhtmltopdf
        self.has_wkhtmltopdf = shutil.which('wkhtmltopdf') is not None
        if self.convert_webpages and not self.has_wkhtmltopdf:
            self.log("wkhtmltopdf not found. Web page conversion disabled.", "WARNING")
            self.log("Install with: sudo apt-get install wkhtmltopdf", "INFO")
            self.convert_webpages = False

    def log(self, message, level="INFO"):
        """Print log message if verbose"""
        if self.verbose:
            prefix = {
                "INFO": "ℹ️",
                "SUCCESS": "✅",
                "ERROR": "❌",
                "WARNING": "⚠️"
            }.get(level, "•")
            print(f"{prefix} {message}")

    def extract_doi_from_text(self, text):
        """Extract DOI from text"""
        # DOI pattern: 10.xxxx/xxxxx
        doi_pattern = r'10\.\d{4,9}/[-._;()/:A-Z0-9]+'
        matches = re.findall(doi_pattern, text, re.IGNORECASE)
        return list(set(matches))  # Remove duplicates

    def extract_arxiv_id(self, text):
        """Extract arXiv ID from text"""
        # arXiv patterns: arXiv:1234.5678, arXiv:1234.5678v2
        arxiv_pattern = r'arXiv:(\d{4}\.\d{4,5})(v\d+)?'
        matches = re.findall(arxiv_pattern, text, re.IGNORECASE)
        return [f"{m[0]}{m[1]}" for m in matches]

    def extract_pubmed_id(self, text):
        """Extract PubMed ID from text"""
        # PMID pattern
        pmid_pattern = r'PMID:?\s*(\d{6,8})'
        matches = re.findall(pmid_pattern, text, re.IGNORECASE)
        return matches

    def parse_bibtex(self, bibtex_file):
        """Parse BibTeX file and extract identifiers"""
        self.log(f"Parsing BibTeX file: {bibtex_file}")

        identifiers = {
            'doi': [],
            'arxiv': [],
            'pmid': [],
            'url': []
        }

        try:
            with open(bibtex_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract DOIs
            identifiers['doi'] = self.extract_doi_from_text(content)

            # Extract arXiv IDs
            identifiers['arxiv'] = self.extract_arxiv_id(content)

            # Extract PMIDs
            identifiers['pmid'] = self.extract_pubmed_id(content)

            # Extract URLs from url={...} fields
            url_pattern = r'url\s*=\s*[{"]([^}"]+)[}"]'
            identifiers['url'] = re.findall(url_pattern, content, re.IGNORECASE)

            self.log(f"Found {len(identifiers['doi'])} DOIs, "
                    f"{len(identifiers['arxiv'])} arXiv IDs, "
                    f"{len(identifiers['pmid'])} PMIDs")

            return identifiers

        except Exception as e:
            self.log(f"Error parsing BibTeX: {e}", "ERROR")
            return identifiers

    def parse_tex_references(self, tex_file):
        """Parse LaTeX file and extract identifiers from references"""
        self.log(f"Parsing LaTeX file: {tex_file}")

        identifiers = {
            'doi': [],
            'arxiv': [],
            'pmid': [],
            'url': []
        }

        try:
            with open(tex_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Look for references section
            # Pattern: \begin{thebibliography} ... \end{thebibliography}
            ref_pattern = r'\\begin{thebibliography}(.*?)\\end{thebibliography}'
            ref_match = re.search(ref_pattern, content, re.DOTALL | re.IGNORECASE)

            if ref_match:
                ref_content = ref_match.group(1)

                # Extract identifiers from references
                identifiers['doi'] = self.extract_doi_from_text(ref_content)
                identifiers['arxiv'] = self.extract_arxiv_id(ref_content)
                identifiers['pmid'] = self.extract_pubmed_id(ref_content)

                # Extract URLs from \url{...} or \href{...}
                url_pattern = r'\\(?:url|href)\{([^}]+)\}'
                identifiers['url'] = re.findall(url_pattern, ref_content)

                self.log(f"Found {len(identifiers['doi'])} DOIs, "
                        f"{len(identifiers['arxiv'])} arXiv IDs, "
                        f"{len(identifiers['pmid'])} PMIDs")
            else:
                self.log("No bibliography section found", "WARNING")

            return identifiers

        except Exception as e:
            self.log(f"Error parsing LaTeX: {e}", "ERROR")
            return identifiers

    def download_from_doi(self, doi):
        """Download paper using DOI via Sci-Hub or Unpaywall"""
        self.log(f"Attempting to download DOI: {doi}")

        # Try Unpaywall API first (legal, open access)
        try:
            unpaywall_url = f"https://api.unpaywall.org/v2/{doi}?email=researcher@example.com"
            req = Request(unpaywall_url, headers=self.headers)
            response = urlopen(req, timeout=10)
            data = json.loads(response.read().decode())

            if data.get('is_oa') and data.get('best_oa_location'):
                pdf_url = data['best_oa_location'].get('url_for_pdf')
                if pdf_url:
                    return self.download_pdf(pdf_url, f"doi_{doi.replace('/', '_')}.pdf")

        except Exception as e:
            self.log(f"Unpaywall failed: {e}", "WARNING")

        # Note: Sci-Hub usage may violate copyright laws in some jurisdictions
        # Users should ensure compliance with local laws
        self.log(f"Could not find open access version for DOI: {doi}", "WARNING")
        return None

    def download_from_arxiv(self, arxiv_id):
        """Download paper from arXiv"""
        self.log(f"Downloading from arXiv: {arxiv_id}")

        # Clean version number if present
        arxiv_id_clean = arxiv_id.split('v')[0]

        # arXiv PDF URL
        pdf_url = f"https://arxiv.org/pdf/{arxiv_id_clean}.pdf"

        return self.download_pdf(pdf_url, f"arxiv_{arxiv_id_clean}.pdf")

    def download_from_pmid(self, pmid):
        """Download paper using PubMed ID"""
        self.log(f"Attempting to download PMID: {pmid}")

        # Try to get PMC ID and download from PMC
        try:
            # Get article info from PubMed
            url = f"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&id={pmid}&retmode=json"
            req = Request(url, headers=self.headers)
            response = urlopen(req, timeout=10)
            data = json.loads(response.read().decode())

            # Check if there's a PMC ID
            article_ids = data.get('result', {}).get(pmid, {}).get('articleids', [])
            pmc_id = None

            for aid in article_ids:
                if aid.get('idtype') == 'pmc':
                    pmc_id = aid.get('value')
                    break

            if pmc_id:
                # Try to download from PMC
                pmc_pdf_url = f"https://www.ncbi.nlm.nih.gov/pmc/articles/{pmc_id}/pdf/"
                return self.download_pdf(pmc_pdf_url, f"pmid_{pmid}.pdf")
            else:
                self.log(f"No PMC version available for PMID: {pmid}", "WARNING")

        except Exception as e:
            self.log(f"PubMed download failed: {e}", "WARNING")

        return None

    def convert_webpage_to_pdf(self, url, filename):
        """Convert web page to PDF using wkhtmltopdf"""
        if not self.has_wkhtmltopdf:
            self.log(f"Cannot convert webpage (wkhtmltopdf not available): {url}", "WARNING")
            return None

        output_path = self.output_dir / filename

        # Skip if already exists
        if output_path.exists():
            self.log(f"File already exists: {filename}", "WARNING")
            return str(output_path)

        try:
            self.log(f"Converting webpage to PDF: {url}")

            # Run wkhtmltopdf
            result = subprocess.run(
                [
                    'wkhtmltopdf',
                    '--quiet',
                    '--enable-local-file-access',
                    '--no-stop-slow-scripts',
                    '--javascript-delay', '2000',
                    '--load-error-handling', 'ignore',
                    url,
                    str(output_path)
                ],
                capture_output=True,
                timeout=60
            )

            if result.returncode == 0 and output_path.exists():
                self.log(f"Converted: {filename}", "SUCCESS")
                return str(output_path)
            else:
                self.log(f"Conversion failed: {url}", "ERROR")
                if output_path.exists():
                    output_path.unlink()  # Remove incomplete file
                return None

        except subprocess.TimeoutExpired:
            self.log(f"Conversion timeout: {url}", "ERROR")
            return None
        except Exception as e:
            self.log(f"Conversion error: {e}", "ERROR")
            return None

    def is_webpage_url(self, url):
        """Check if URL is a web page (not a direct PDF link)"""
        # Skip if it's clearly a PDF URL
        if url.lower().endswith('.pdf'):
            return False

        # Skip academic paper repositories (handled separately)
        parsed = urlparse(url.lower())
        if any(domain in parsed.netloc for domain in [
            'arxiv.org', 'doi.org', 'pubmed', 'ncbi.nlm.nih.gov'
        ]):
            return False

        # Likely a web page
        return True

    def download_pdf(self, url, filename):
        """Download PDF from URL"""
        output_path = self.output_dir / filename

        # Skip if already exists
        if output_path.exists():
            self.log(f"File already exists: {filename}", "WARNING")
            return str(output_path)

        try:
            self.log(f"Downloading: {url}")
            req = Request(url, headers=self.headers)
            response = urlopen(req, timeout=30)

            # Check if content is PDF
            content_type = response.headers.get('Content-Type', '')
            if 'pdf' not in content_type.lower():
                self.log(f"Not a PDF: {content_type}", "WARNING")
                return None

            # Download
            with open(output_path, 'wb') as f:
                f.write(response.read())

            self.log(f"Downloaded: {filename}", "SUCCESS")
            return str(output_path)

        except HTTPError as e:
            self.log(f"HTTP Error {e.code}: {url}", "ERROR")
            return None
        except URLError as e:
            self.log(f"URL Error: {e.reason}", "ERROR")
            return None
        except Exception as e:
            self.log(f"Download failed: {e}", "ERROR")
            return None

    def download_all(self, identifiers, delay=2):
        """Download all papers from identifiers"""
        # Separate web page URLs from identifiers
        webpage_urls = []
        if self.convert_webpages:
            webpage_urls = [url for url in identifiers.get('url', [])
                          if self.is_webpage_url(url)]

        total = (len(identifiers['doi']) +
                len(identifiers['arxiv']) +
                len(identifiers['pmid']) +
                len(webpage_urls))

        self.log(f"\nStarting download of {total} references...")
        self.log("="*60)

        # Download from arXiv (usually most reliable)
        for arxiv_id in identifiers['arxiv']:
            result = self.download_from_arxiv(arxiv_id)
            if result:
                self.downloaded.append(result)
            else:
                self.failed.append(('arxiv', arxiv_id))
            time.sleep(delay)

        # Download from DOI
        for doi in identifiers['doi']:
            result = self.download_from_doi(doi)
            if result:
                self.downloaded.append(result)
            else:
                self.failed.append(('doi', doi))
            time.sleep(delay)

        # Download from PubMed
        for pmid in identifiers['pmid']:
            result = self.download_from_pmid(pmid)
            if result:
                self.downloaded.append(result)
            else:
                self.failed.append(('pmid', pmid))
            time.sleep(delay)

        # Convert web pages to PDF
        if self.convert_webpages and webpage_urls:
            self.log(f"\nConverting {len(webpage_urls)} web pages to PDF...")
            for url in webpage_urls:
                # Generate filename from URL
                parsed = urlparse(url)
                safe_name = re.sub(r'[^\w\-]', '_', parsed.netloc + parsed.path)
                safe_name = safe_name[:100]  # Limit length
                filename = f"webpage_{safe_name}.pdf"

                result = self.convert_webpage_to_pdf(url, filename)
                if result:
                    self.downloaded.append(result)
                    self.webpages.append(url)
                else:
                    self.failed.append(('webpage', url))
                time.sleep(delay)

        # Print summary
        self.print_summary()

    def print_summary(self):
        """Print download summary"""
        print("\n" + "="*60)
        print("Download Summary")
        print("="*60)
        print(f"✅ Successfully downloaded/converted: {len(self.downloaded)} files")
        print(f"   - Papers (PDF): {len(self.downloaded) - len(self.webpages)}")
        print(f"   - Web pages (PDF): {len(self.webpages)}")
        print(f"❌ Failed to download/convert: {len(self.failed)} files")
        print(f"📁 Output directory: {self.output_dir}")

        if self.downloaded:
            print("\nSuccessfully processed:")
            for path in self.downloaded:
                print(f"  • {Path(path).name}")

        if self.failed:
            print("\nFailed to process:")
            for id_type, identifier in self.failed:
                if id_type == 'webpage':
                    print(f"  • webpage: {identifier[:80]}...")
                else:
                    print(f"  • {id_type}: {identifier}")
            print("\nNote: Some papers may not be available as open access.")
            print("You may need to download them manually from your institution.")
            print("Some web pages may not convert properly to PDF.")

def main():
    parser = argparse.ArgumentParser(
        description="Download reference papers from BibTeX or LaTeX files"
    )
    parser.add_argument(
        'input',
        nargs='?',
        help='Input file (.bib or .tex)'
    )
    parser.add_argument(
        '-o', '--output',
        default='references/papers',
        help='Output directory (default: references/papers)'
    )
    parser.add_argument(
        '-d', '--delay',
        type=int,
        default=2,
        help='Delay between downloads in seconds (default: 2)'
    )
    parser.add_argument(
        '--quiet',
        action='store_true',
        help='Suppress verbose output'
    )
    parser.add_argument(
        '--no-webpages',
        action='store_true',
        help='Skip web page to PDF conversion'
    )

    args = parser.parse_args()

    # Find input file if not specified
    if not args.input:
        # Look for .bib or .tex files in report directory
        report_dir = Path('report')
        if report_dir.exists():
            bib_files = list(report_dir.glob('*.bib'))
            tex_files = list(report_dir.glob('*.tex'))

            if bib_files:
                args.input = str(bib_files[0])
                print(f"Auto-detected BibTeX file: {args.input}")
            elif tex_files:
                args.input = str(tex_files[0])
                print(f"Auto-detected LaTeX file: {args.input}")
            else:
                print("Error: No .bib or .tex files found in report/ directory")
                print("Please specify an input file")
                sys.exit(1)
        else:
            print("Error: No report/ directory found")
            print("Please specify an input file")
            sys.exit(1)

    input_file = Path(args.input)

    if not input_file.exists():
        print(f"Error: File not found: {input_file}")
        sys.exit(1)

    # Create downloader
    downloader = ReferenceDownloader(
        output_dir=args.output,
        verbose=not args.quiet,
        convert_webpages=not args.no_webpages
    )

    # Parse input file
    if input_file.suffix == '.bib':
        identifiers = downloader.parse_bibtex(input_file)
    elif input_file.suffix == '.tex':
        identifiers = downloader.parse_tex_references(input_file)
    else:
        print(f"Error: Unsupported file type: {input_file.suffix}")
        print("Supported types: .bib, .tex")
        sys.exit(1)

    # Download papers
    downloader.download_all(identifiers, delay=args.delay)

if __name__ == '__main__':
    main()
