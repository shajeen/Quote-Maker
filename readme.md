# Quote Maker

![Reference (13)](https://user-images.githubusercontent.com/2623563/144739215-6b1cac28-fe6e-4ee0-8355-baa11443b1de.png)

A Python application to generate quote images and share them across various social media platforms.

## Features

-   Generates images with custom or fetched quotes.
-   Supports multiple quote sources: manual input, API, or local file.
-   Modular design for easy extension to new social media platforms.
-   Posts images to Facebook (with placeholders for Twitter and Instagram).
-   Command-line interface for flexible usage.
-   Centralized configuration management.
-   Includes unit tests.
-   Provides a Cython-optimized version for performance.
-   Robust logging for better monitoring.

## Installation

1.  **Clone the repository:**

    ```sh
    git clone https://github.com/your-username/Quote-Maker.git
    cd Quote-Maker
    ```

2.  **Create and activate a conda environment:**

    ```sh
    conda create --name quote-maker-env python=3.10 -y
    conda activate quote-maker-env
    ```

3.  **Install the dependencies:**

    ```sh
    pip install -r requirements.txt
    ```

4.  **Build the Cython module:**

    ```sh
    python setup.py build_ext --inplace
    ```

## Configuration

The application uses a flexible configuration system. Default settings are defined in `config/config.py`. You can override these settings using:

-   **Environment Variables:** For sensitive information like API keys (e.g., `FACEBOOK_ACCESS_TOKEN`).
-   **Configuration File:** Specify a custom JSON configuration file using the `--config` CLI argument.

Key configuration parameters:

-   `FONT_PATH`: Path to the font file.
-   `IMAGE_WIDTH`, `IMAGE_HEIGHT`: Dimensions of the generated image.
-   `FACEBOOK_PAGE_ID`: Your Facebook page ID.
-   `FACEBOOK_ACCESS_TOKEN`: Your Facebook access token (recommended via environment variable).
-   `DEFAULT_QUOTE_SOURCE`: Default source for quotes (`manual`, `api`, or `file`).
-   `QUOTE_API_URL`: URL for fetching quotes from an API.
-   `QUOTE_FILE_PATH`: Path to a local file containing quotes (e.g., JSON, CSV, or TXT).
-   `LOG_LEVEL`: Logging level (e.g., `INFO`, `DEBUG`).
-   `LOG_FILE`: Path to the log file.

## Usage

To run the application, use the following command:

```sh
python -m src.quote_maker.main [OPTIONS]
```

### Command-line Options:

-   `--config PATH`: Path to a custom configuration file.
-   `--quote-source {manual,api,file}`: Specify the source for quotes.
    -   `manual`: Prompts for quote and page name.
    -   `api`: Fetches a random quote from a configured API. Prompts for a page name for the logo.
    -   `file`: Reads a random quote from a local file (JSON, CSV, or TXT). Prompts for a page name for the logo.
-   `--quote-file PATH`: Path to the quotes file (required if `--quote-source` is `file`).
-   `--api-url URL`: API URL for quotes (overrides default if `--quote-source` is `api`).
-   `--no-post`: Generate image only, do not post to social media.
-   `--platform {facebook,all}`: Social media platform to post to (default: `facebook`).
-   `--output PATH`: Custom output path for the generated image.

### Examples:

1.  **Generate an image from manual input and post to Facebook:**

    ```sh
    python -m src.quote_maker.main --quote-source manual --platform facebook
    ```

2.  **Fetch a quote from an API, generate an image, and save locally (do not post):**

    ```sh
    python -m src.quote_maker.main --quote-source api --no-post --output my_quote.png
    ```

3.  **Use a custom quotes file:**

    ```sh
    python -m src.quote_maker.main --quote-source file --quote-file my_quotes.json
    ```

## Running Tests

To run the unit tests, use the following command:

```sh
python -m unittest tests/test_generator.py
```

## Project Structure

```
Quote-Maker/
├── config/
│   └── config.py
├── src/
│   └── quote_maker/
│       ├── __init__.py
│       ├── generator.py
│       ├── generator_cy.pyx
│       ├── facebook.py
│       ├── quote_fetcher.py
│       ├── main.py
│       └── fonts/
│           └── Quote.ttf
├── tests/
│   └── test_generator.py
├── .gitignore
├── LICENSE
├── pyproject.toml
├── readme.md
├── requirements.txt
├── setup.py
└── todo.txt
```