# Discord Movie & Book Recommendation Bot

A simple yet powerful Discord bot that provides movie and book recommendations directly in your server. Finished a great movie and want to see something similar? Just read a great book and need a new one? This bot has you covered!

## Features

- **Movie Recommendations:** Get a list of similar movies using the `!movie` command.
- **Book Recommendations:** Discover new books from the same genre using the `!book` command.
- **Clean, Embedded Responses:** Displays information in a nicely formatted and easy-to-read way.

## How to Set Up

Follow these instructions to get your own copy of the bot running.

### Prerequisites

*   Python 3.8+
*   A Discord Bot Token
*   A TMDB API Key

### Installation

1.  **Clone the repository:**
    ```sh
    git clone https://github.com/manjitt2/Movie-bot.git
    cd Movie-bot
    ```

2.  **Install the required libraries:**
    ```sh
    pip install -r requirements.txt
    ```
    *(Note: You will need to create `requirements.txt` first by running `pip freeze > requirements.txt`)*

3.  **Create a `.env` file** in the main folder and add your keys:
    ```
    DISCORD_TOKEN=YourDiscordTokenGoesHere
    TMDB_API_KEY=YourTmdbApiKeyGoesHere
    ```

4.  **Run the bot:**
    ```sh
    python main.py
    ```

## Usage Examples

-   **Get movie recommendations:**
    ```
    !movie The Dark Knight
    ```

-   **Get book recommendations:**
    ```
    !book Dune
    ```

## APIs Used
*   [The Movie Database (TMDB)](https://www.themoviedb.org/)
*   [Open Library](https://openlibrary.org/)
