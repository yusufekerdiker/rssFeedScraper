# rssFeedScraper

```
# Tech News Scraper

Welcome to the Tech News Scraper project repository! This is a tool that collects and organizes technology news articles from various websites, providing you with an easy way to stay updated on the latest happenings in the tech world.

## Features

- Scrapes technology news articles from popular websites.
- Cleans the scraped data for consistency and quality.
- Uses machine learning (RAKE*) to classify articles into categories.
- Stores the data in a database for easy access.
- Provides a web API to access the collected data programmatically.
- Includes a user-friendly web application to browse and search for articles.

*RAKE is a domain independent keyword extraction algorithm which tries to determine key phrases in a body of text by analyzing the frequency of word appearance and its co-occurance with other words in the text.

## Technologies Used

- Python
- Beautiful Soup
- Flask
- MongoDB
- Angular

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/tech-news-aggregator.git
```

2. Install the required dependencies for the web scraping and API components:

```bash
pip install -r requirements.txt
```

3. Install the required dependencies for the web application:

```bash
cd Frontend
npm install
```

## Usage

1. Run the web scraping component to gather the latest technology news articles:

```bash
python scraper.py
```

2. Start the API server to provide access to the collected data:

```bash
python api.py
```

3. Launch the web application to browse and search for articles:

```bash
cd Frontend
npm start
```

4. Open your web browser and navigate to `http://localhost:4200` to access the Tech News Scraper web application.

## Contributing

Contributions are welcome! If you find any issues or have ideas for improvements, please open an issue or submit a pull request.

## License

This project is licensed under the [I HAVE NO IDEA].
```
