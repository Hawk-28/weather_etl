# Weather Data ETL

## Overview

This project contains a Python script that performs an ETL (Extract, Transform, Load) process on weather data obtained from the OpenWeather API. The script fetches weather data based on geographic coordinates, processes it, and stores the output in an AWS S3 bucket.

## Features

- Fetches weather data using latitude and longitude.
- Supports fetching data in metric units (Celsius).
- Handles AWS S3 storage for processed data.
- Can be extended for further analysis or storage.

## Getting Started

### Prerequisites

Ensure you have the following installed:

- Python 3.x
- Required Python packages (listed in `requirements.txt`)

### Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/yourusername/weather-data-etl.git
    cd weather-data-etl
    ```

2. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

### Configuration

The script requires an API key from OpenWeather and AWS credentials for accessing S3. Set up your environment by adding your API key and AWS credentials:

1. **Create a `.env` file** in the project root directory and add your API key and AWS credentials:
    ```bash
    OPENWEATHER_API_KEY=your_api_key_here
    AWS_ACCESS_KEY_ID=your_aws_access_key_id_here
    AWS_SECRET_ACCESS_KEY=your_aws_secret_access_key_here
    AWS_BUCKET_NAME=your_s3_bucket_name_here
    ```

2. Alternatively, you can directly insert your API key and AWS credentials in the script.

### Usage

1. **Run the script**:
    ```bash
    python weather_report.py
    ```

2. **Parameters**:
    - `lat`: Latitude of the location.
    - `lon`: Longitude of the location.
    - `units`: Units for temperature (e.g., `metric` for Celsius).

    Example:
    ```python
    params = {
        'lat': 40.7128,
        'lon': -74.0060,
        'appid': 'your_api_key',
        'units': 'metric'
    }
    ```

3. **Output**:
    - The processed weather data is displayed or saved in an S3 bucket.

### API Hit Limitation

Due to API hit limitations, the script reduces the number of rows in the DataFrame. If you have a higher API request limit, you can adjust the script to fetch and process more data.

## Project Structure

