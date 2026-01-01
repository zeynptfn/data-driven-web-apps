const BASE_URL = 'https://api.openweathermap.org/data/2.5';

/**
 * Fetches the 5-day weather forecast for a given city.
 * @param {string} city - The name of the city.
 * @returns {Promise<Object>} - The weather data.
 * @throws {Error} - If the API call fails.
 */
export const fetchWeatherForecast = async (city) => {
  const apiKey = import.meta.env.VITE_OPENWEATHER_API_KEY;

  if (!apiKey) {
    throw new Error('API key is missing. Please check your .env file.');
  }

  try {
    const response = await fetch(
      `${BASE_URL}/forecast?q=${city}&units=metric&appid=${apiKey}`
    );

    if (!response.ok) {
      if (response.status === 404) {
        throw new Error('City not found. Please check the spelling.');
      } else if (response.status === 401) {
        throw new Error('Invalid API key.');
      } else if (response.status === 429) {
        throw new Error('API rate limit exceeded.');
      } else {
        throw new Error('Failed to fetch weather data.');
      }
    }

    const data = await response.json();
    return data;
  } catch (error) {
    throw error;
  }
};
