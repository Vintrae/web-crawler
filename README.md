# web-crawler
A simple web crawler written in Python.

Despite the various amount of links that can be fetched from an HTML file, this crawler only pays attention to those in <a> tags. The
way it works is that the initial link is provided as an argument to the program. For example:
```
C:\> python crawler.py https://www.bbc.co.uk/
```
The crawler will then try to go to the URL and fetch all the links it can from its HTML source code. After that, if 100 links have not
yet been fetched, it will start the crawling process again and if that is not enough it will cycle through the second link instead,
repeating the cycle until at least a hundred links have been seen.

After getting the links it prints the first 100 obtained, together with the entry URL provided.
