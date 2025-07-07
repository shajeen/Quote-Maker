# Quote Maker

![Reference (13)](https://user-images.githubusercontent.com/2623563/144739215-6b1cac28-fe6e-4ee0-8355-baa11443b1de.png)

A Python script to create quoted images and publish them to a Facebook page.

## Features

-   Generates images with custom quotes.
-   Posts images to a Facebook page.
-   Uses a professional project structure.
-   Includes unit tests.
-   Provides a Cython-optimized version for performance.

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

Before running the application, you need to configure your Facebook API settings in `config/config.py`:

-   `FACEBOOK_PAGE_ID`: Your Facebook page ID.
-   `FACEBOOK_ACCESS_TOKEN`: Your Facebook access token.

## Usage

To run the application, use the following command:

```sh
python -m src.quote_maker.main
```

The script will prompt you to enter a quote, and then it will generate an image and post it to your Facebook page.

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