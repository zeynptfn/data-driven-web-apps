import React, { useState } from 'react';
import { useWeather } from '../context/WeatherContext';
import { Search } from 'lucide-react';

const SearchBar = () => {
  const [city, setCity] = useState('');
  const { fetchWeather, loading } = useWeather();

  const handleSubmit = (e) => {
    e.preventDefault();
    if (city.trim()) {
      fetchWeather(city);
    }
  };

  return (
    <div className="w-full max-w-md mx-auto p-4">
      <form onSubmit={handleSubmit} className="relative flex items-center">
        <input
          type="text"
          value={city}
          onChange={(e) => setCity(e.target.value)}
          placeholder="Enter city name..."
          className="w-full px-4 py-2 pr-10 text-gray-700 bg-white border rounded-lg focus:outline-none focus:border-blue-500 shadow-sm"
        />
        <button
          type="submit"
          disabled={loading}
          className="absolute right-0 top-0 mt-2 mr-3 text-gray-500 hover:text-blue-500 disabled:opacity-50"
        >
          {loading ? (
            <span className="animate-spin h-5 w-5 border-2 border-blue-500 rounded-full border-t-transparent block"></span>
          ) : (
            <Search size={20} />
          )}
        </button>
      </form>
    </div>
  );
};

export default SearchBar;
