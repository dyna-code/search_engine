# **Political Search Engine**

**Datasets:**

For our project the `webcrawler` and `downloader` folders go over our data collection and datasets. We already have the HTMLs downloaded. Crawling the websites and redownloading all the HTMLs will be time consuming. Crawling and Downloading the pages needs to be done individually for each website.

**Components:**

* Webcrawler: We are targeting 10 sites across 5 politcal leanings. Each of these sites has their own webcrawler to extract relevant links and their titles.
* Downloader: The output of the webcrawler is then run through the downloader which downloads and stores all the links as HTML files.
* JSON Compiler: This compiles all the metadata for each website into one large file.
* Inverted Index: Building an inverted index from all of the HTMLs from the 10 websites
* flask_app: It is the Flask server which hosts the search engine.

*(**IMPORTANT**: skip steps 3, 4, 5, 6 as these are data collection steps and are time consuming. We have submitted to project with all the data already there)*

**Setup:**

1. run `pip3 install -r requirements.txt` in the parent directory (`eecs486finalproject`)
2. This should install Flask v3.0.3 and BeautifulSoup4 v4.12.3
3. To scrape the latest links for any webcrawler, `cd` into the relevant `webcrawler/<website>` folder, and in that folder run `python3 main.py`
4. This should output a file in the format of `links_<website>`.txt
5. You can download the links by moving to the downloader folder and running `python3 downloader.py`
6. This should prompt a website name in the terminal. Enter a website name and it will add the HTMLs for that website to the `files` folder. Copy this folder to `flask_app` and rename it to `static`
7. Move to the `inverted_index` folder and run `inv_index.py` , which should build an inverted index from the files in `downloader/files`
8. Move to the `json_compiler` folder and run `main.py` to build the master metadata json from all the websites we have downloaded HTMLs for
9. Now move to `flask_app` and run `python3 main.py`
10. Open `127.0.0.1:5000` on your browser and you should have a search engine ready to use!

Additional Documentation:

`webcrawler`

There are 10 webcrawlers - one for each website that we are using in this project. To run the webcrawler for a given website, `cd` into the directory and ensure that the  `links_<website>.txt` only has the base link for the website in it (the first one in the file). Execute the command `python3 crawler_<website>.py` . Running the webcrawler for a given website will only generate the links for the said website in the text file.

`downloader`

To work with the downloader you will first need to `cd` into the `downloader` folder and run `python3 downloader.py` . This should prompt you with a website name. Ensure that you have crawled the links for this website before downloading the HTML pages. Also ensure that pages from this website are not already in the `downloader/files` folder. If there pages, from the `downloader/files` folder in the terminal, 

run `rm -rf <website>_*` to delete any HTML pages. The code should output roughly 500 HTML files and a json containing file names and the folder. Progress can be monitored by the HTML file download number displayed in the terminal. (out of ~500)

`json_compiler`

After crawling and downloading all website, compile all the jsons produced by the downloader into one file - `output.json` by running `python3 main.py`

`inverted_index`

Build an inverted index by running `python3 inv_index.py` . The code will take sometime to run - progress can be monitored by terminal output indicating number of files processed (out of ~5000)

`flask_app`

After running `downloader`, `json_compiler`, and `inverted_index`, delete the `static` folder and then copy the `downloader/files` folder to `flask_app` and rename it to `static` . Then run `python3 main.py` and it should host a serve at `127.0.0.1:5000` from where the search engine can be accessed.
