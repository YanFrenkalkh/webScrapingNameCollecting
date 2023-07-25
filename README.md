# webScrapingNameCollecting

This project uses Python to scrape data from Wikipedia to collect the first and last names of people. 
The project is divided into the following steps:

    1.Install the necessary Python libraries.
    2.Create a list of Wikipedia pages to scrape.
    3.Scrape the Wikipedia pages for the first and last names of people.
    4.Save the names to a file.

# The project uses the following Python libraries:
    1.requests for making HTTP requests to Wikipedia.
    2.BeautifulSoup for parsing the HTML content of Wikipedia pages.
    3.json used to parse JSON data.
    4.tqdm library is used to display a progress bar.
    5.pandas library used to work with dataframes.

To run the project, you will need to have Python installed on your computer. 
# You can then install the necessary libraries by running the following command in your terminal:

pip install requests beautifulsoup4 pandas tqdm

# Once you have installed the libraries, you can run the project by running the following command in your terminal:

python names_data_collection.py

This will scrape the Wikipedia pages and save the names to the data_sets.csv file.

The CSV file contains the contents of a Wikipedia pages. 
# The file contains the following columns:

    Name (Label): This column stores the name from the Wikipedia website. This refers to the given name or surname we are looking for.
    WikiData ID: This column stores the ID you found.
    English Description: This column stores the general description in English for the given name.
    Language: This column stores the language in which the name is written (English, Arabic).
    Lang Short Wiki: This column stores the language abbreviations as they appear on the page, e.g., en for English, ar for Arabic, etc.
    Entry: This is intended to store the name in the specific language.

