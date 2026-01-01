import React, { createContext, useState, useContext, useCallback } from 'react';
import { fetchWeatherForecast } from '../services/weatherService';
import { transformWeatherData } from '../utils/dataTransformer';

const WeatherContext = createContext();

export const WeatherProvider = ({ children }) => {
  const [weatherData, setWeatherData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchWeather = useCallback(async (city) => {
    setLoading(true);
    setError(null);
    try {
      // In a real scenario, we would call the API.
      // For testing without a real key, we might need a mock mode,
      // but here we follow the standard path.
      const data = await fetchWeatherForecast(city);
      const transformedData = transformWeatherData(data);
      setWeatherData(transformedData);
    } catch (err) {
      setError(err.message);
      setWeatherData(null);
    } finally {
      setLoading(false);
    }
  }, []);

  const clearError = () => setError(null);

  return (
    <WeatherContext.Provider value={{ weatherData, loading, error, fetchWeather, clearError }}>
      {children}
    </WeatherContext.Provider>
  );
};

export const useWeather = () => useContext(WeatherContext);
