from urllib.request import urlopen
import re
import sys

# Function that does the actual crawling of the url given and stores the
# links in the provided list, together with their parent link.
def crawl(url, links):
    # Open url and split its words into a list.
    if url.endswith('/'): # remove slash from the end of url
        url = url[:-1]
    # Some of the links, despite being of interest for output, might not be
    # browsable. In those cases, just return the list of links and main() will
    # move on to the next link.
    try:
        data = urlopen(url)
        tokens = str(data.read())
        tokens = re.split(' |<|>', tokens)

        # Remove unwanted tags from the list.
        unwanted_elements = ('<html>', '</html>', '<head>', '</head>', '<body>', '</body>')
        clean_list = [token for token in tokens if token not in unwanted_elements]

        # Fetch links from the list and store them.
        store_link = 0
        for token in clean_list:
            # The tag <a indicates the start of a link, so we look for 'a' since
            # the token was stripped of the '<'.
            if token == 'a':
                # Start looking for a link in the following tokens.
                store_link = 1
            elif store_link == 1:
                if token.startswith('href='):
                    token = token.replace('href="', '')
                    token = token.replace('href=\\', '')
                    # Case where we got a relative path.
                    if token.startswith('/'):
                        # It might instead be a short-hand.
                        if token.startswith('//'):
                            token = 'http:' + token
                        else:
                            token = url + token
                    # It is assumed that links start with a letter.
                    if token and token[0].isalpha():
                        links.append(token[:-1])
                    store_link = 0

        # Get rid of duplicates.
        unique_links = []
        for link in links:
            if link.endswith('/'):
                link = link[:-1]
            if link not in unique_links and link is not url:
                unique_links.append(link)
        return unique_links
    except:
        return links

def main():
    # Create a list to store the links found from the text. Also store the
    # initial url to crawl after dealing with inappropriate input.
    if len(sys.argv) != 2:
        print("Only one argument should be provided: crawler.py \"url to crawl\"")
        sys.exit(1)
    links = [sys.argv[1]]

    # If the amount of unique links is not yet 101 (making up for initial link),
    # crawl the links.
    count = 0
    while count < len(links) and len(links) < 101:
        links = crawl(links[count], links)
        count += 1

    if len(links) > 100:
        links = links[:101]

    # Print the results of the crawl.
    print("Initial URL: ", links[0])
    print("\nURLs discovered:")
    for element in range(1, len(links)):
        print(str(element) + ': ' + links[element])

main()
