import requests
from bs4 import BeautifulSoup
from collections import deque
import urllib.parse

def normalize_url(url):
    # Parse the URL
    parsed_url = urllib.parse.urlparse(url)
    # Normalize: Convert domain to lowercase, remove www, sort query parameters, strip trailing slash
    normalized = parsed_url.scheme + "://" + parsed_url.netloc.replace("www.", "").lower() + parsed_url.path.rstrip('/')
    if parsed_url.query:
        # Sort query parameters
        query = urllib.parse.parse_qs(parsed_url.query)
        sorted_query = sorted(query.items())
        normalized_query = urllib.parse.urlencode(sorted_query, doseq=True)
        normalized += '?' + normalized_query
    return normalized

def crawl_starting_from(url):
    # Use a set to keep track of visited URLs
    visited = set()
    # Use a queue for the breadth-first search approach
    queue = deque([url])
    # Counter for number of links processed
    count = 0

    # Open a file to write links and titles
    with open("links_nbc.txt", "w") as file:
        while queue and count < 500:
            current_url = queue.popleft()
            normalized_url = normalize_url(current_url)
            if normalized_url not in visited:
                visited.add(normalized_url)
                try:
                    # Fetch the content of the URL
                    response = requests.get(current_url, timeout=10)
                    if response.status_code == 200:
                        # Parse the content
                        soup = BeautifulSoup(response.content, "html.parser")
                        # Get the canonical URL if available, otherwise use the normalized URL
                        canonical_link = soup.find('link', rel='canonical')
                        if canonical_link and canonical_link['href']:
                            current_url = normalize_url(canonical_link['href'])
                        # Write the current URL and the title to the file
                        title = soup.find('title').text if soup.find('title') else 'No title'
                        if current_url != "https://facebook.com/login" and "nbc" in current_url:
                            file.write(f"{current_url} {title}\n")
                            # Increment the counter
                            count += 1
                        # Find all links on the current page
                        for link in soup.find_all('a', href=True):
                            href = link.get('href')
                            new_url = normalize_url(urllib.parse.urljoin(current_url, href))
                            if new_url not in visited:
                                queue.append(new_url)
                except requests.RequestException as e:
                    print(f"Failed to retrieve {current_url}: {e}")
        print(f"Finished crawling. {count} links collected.")

# Start crawling from NBC
crawl_starting_from("https://www.nbcnews.com/")
