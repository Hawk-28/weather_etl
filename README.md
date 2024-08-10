# Weather Data ETL

## Overview

This project contains a Python script that performs an ETL (Extract, Transform, Load) process on weather data obtained from the OpenWeather API. The script fetches weather data based on geographic coordinates, processes it, and stores the output in a desired format.

## Features

- Fetches weather data using latitude and longitude.
- Supports fetching data in metric units (Celsius).
- Processes and transforms the data to meet specific requirements.
- Can be extended for further analysis or storage.

## Getting Started

### Prerequisites

Ensure you have the following installed:

- Python 3.x
- Required Python packages (specified in `requirements.txt` or in the script itself)

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

The script requires an API key from OpenWeather. Set up your environment by adding your API key:

1. **Create a `.env` file** in the project root directory and add your API key:
    ```bash
    OPENWEATHER_API_KEY=your_api_key_here
    ```

2. Alternatively, you can directly insert your API key in the script.

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
    - The processed weather data is displayed or saved in a specified format.

## Project Structure

