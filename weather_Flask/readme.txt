To use this application:

Install requirements:

bash
Copy
pip install flask requests python-dotenv
Create a .env file with your API keys:

env
Copy
OPENWEATHER_API_KEY=your_api_key_here
WEATHERAPI_API_KEY=your_api_key_here
Run the application:

bash
Copy
python app.py
To add new weather providers:

Add a new entry to the WEATHER_PROVIDERS dictionary

Implement the URL constructor

Add a parser function for the provider's response format

Add the corresponding API key to the environment variables

The application will automatically show new providers in the UI once they're added to the configuration.