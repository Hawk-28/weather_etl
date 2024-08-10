import pandas as pd
import requests
import numpy as np
import boto3
from io import StringIO
import os
from dotenv import load_dotenv

# loading Access API keys and AWS credentials for .env file
load_dotenv()

API_key= os.getenv('OPENWEATHER_API_KEY')
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
aws_bucket_name = os.getenv('AWS_BUCKET_NAME')

#API key and URL
api_key = API_key 
base_url = 'http://api.openweathermap.org/data/2.5/weather'

##Extracting starts here

# function to fetch data from API 
def fetch_weather(city, lat, lng):
    params = {
        'lat': lat,
        'lon': lng,
        'appid': api_key,
        'units': 'metric'
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        data = response.json()
        if 'main' in data and 'weather' in data or 'sys' in data:
            return {
                'city': city,
                'temperature': data['main']['temp'],
                'weather': data['weather'][0]['description'],
                'lat' : data['coord']['lat'],
                'lng' : data['coord']['lon'],
                'temp_min' : data['main']['temp_min'],
                'temp_max' : data['main']['temp_max'],
                'sea_level' : data['main']['sea_level'],
                'humidity' : data['main']['humidity'],
                'current_time' : data['dt'],
                'sunrise' : data['sys']['sunrise'],
                'sunset' : data['sys']['sunset'],
                'timezone' : data['timezone']
            }
        else:
            print(f"Missing 'main' or 'weather' in response for city: {city}")
            return {'city': city, 'temperature': None, 'weather': None}
    else:
        print(f"Failed to fetch weather data for city: {city}, status code: {response.status_code}")
        return {'city': city, 'temperature': None, 'weather': None}

# only selecting countries having more than 100 cities
def extract():
    df = pd.read_csv('worldcities.csv')
    country_counts = df['country'].value_counts() >= 100
    con = country_counts[country_counts == True].index
    df = df[df['country'].isin(con)]

    # selecting 6 cities from each countries due to restriction of API hits
    df = df.groupby('country').head(2)
    
    # Fetch weather data for each city
    weather_data = []
    for index, row in df.iterrows():
        weather = fetch_weather(row['city'], row['lat'], row['lng'])
        weather_data.append(weather)

    weather_df = pd.DataFrame(weather_data)
    #selecting requires columns and joining cities and weather DFs
    cities_df = df[['city_ascii', 'lat', 'lng', 'admin_name','capital', 'population','country']]
    new = pd.merge(cities_df, weather_df, on = ['lat', 'lng'], how = 'inner')
    return (new)

## Transforming of data

def transform(extracted_data):
    # handling null values and changing column name
    extracted_data.rename(columns = {'city_ascii' : 'city'}, inplace= True)
    extracted_data['admin_name'].fillna('Unknown', inplace = True)
    extracted_data['capital'].fillna('Unknown', inplace = True)

    # changing EPOCH values to datetime
    extracted_data['current_time'] = pd.to_datetime(extracted_data['current_time'], unit = 's')
    extracted_data['sunrise'] = pd.to_datetime(extracted_data['sunrise'], unit = 's')
    extracted_data['sunset'] = pd.to_datetime(extracted_data['sunset'], unit = 's')
    extracted_data['day_length'] = np.ceil((extracted_data['sunset'] - extracted_data['sunrise']).dt.total_seconds() /3600)
    extracted_data['Hot-cities'] = np.where(extracted_data['temperature'] > 30 , 'Y', 'N')

    # adding aggregated metric for Country field
    country_stats = extracted_data.groupby('country').agg({
        'temperature': 'mean',
        'population': 'sum',
        'humidity': 'mean'
    }).reset_index()
    country_stats['Country_AVG_popul_temp_humi'] = (country_stats['population'].astype(int).astype(str)) + ',' +round(country_stats['temperature'],2).astype(str) +','+ round(country_stats['humidity'],2).astype(str)

    # merging the DFs
    country_stats = country_stats[['country','Country_AVG_popul_temp_humi']]
    final_df = pd.merge(extracted_data,country_stats, on='country', how = 'inner')
    return (final_df)

## loading data to S3 bucket

def load(transformed_data):
    os.environ['AWS_ACCESS_KEY_ID'] = aws_access_key_id
    os.environ['AWS_SECRET_ACCESS_KEY'] = aws_secret_access_key
    csv_buffer = StringIO()
    transformed_data.to_csv(csv_buffer, index= False)
    s3 = boto3.client('s3', region_name= 'us-east-1')
    bucket_name = aws_bucket_name
    file_name = 'repo.csv'
    s3.put_object(Bucket=bucket_name, Key=file_name, Body=csv_buffer.getvalue())

new = extract()
final_df = transform(new)
load(final_df)
