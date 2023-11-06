import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, urlunparse


def save_to_file(content, filename="output.txt"):
    with open(filename, 'a', encoding='utf-8') as file:
        file.write(content + '\n\n')


# Normalize URLs to avoid visiting the same page multiple times under different URLs.
# Check if a URL has been visited before making a request.
def normalize_url(base_url, url):
    # Convert relative URLs to absolute
    abs_url = urljoin(base_url, url)

    # Use urlparse to break the URL into components
    parsed = urlparse(abs_url)

    # Remove fragments and normalize trailing slash
    normalized = urlunparse(
        (parsed.scheme, parsed.netloc, parsed.path.rstrip('/'),
         parsed.params, parsed.query, '')
    )
    return normalized


def extract_text_content(soup):
    for script in soup(["script", "style"]):
        script.decompose()  # Remove these tags from the tree

    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text_content = '\n'.join(chunk for chunk in chunks if chunk)
    return text_content


def crawl_website(start_url, depth=1):
    visited = set()

    def crawl(url, depth):
        if depth <= 0 or url in visited:
            return

        try:
            response = requests.get(url)
            response.raise_for_status()  # raise exception if invalid response

            visited.add(url)  # Mark the URL as visited after a successful request

            soup = BeautifulSoup(response.text, 'html.parser')
            print("Crawling URL:", url)

            extracted_content = extract_text_content(soup)
            save_to_file(extracted_content)

            # Crawl all links found on this page (recursive step)
            if depth > 1:
                for a_tag in soup.find_all('a', href=True):
                    link = normalize_url(url, a_tag['href'])
                    if link.startswith("http"):
                        crawl(link, depth - 1)
        except requests.RequestException as e:
            print(f"Failed to fetch {url}. Reason: {e}")

    start_url = normalize_url(start_url, start_url)  # Ensure starting URL is normalized
    crawl(start_url, depth)
