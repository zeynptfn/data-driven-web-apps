import React from 'react';
import { useWeather } from '../context/WeatherContext';
import { Thermometer, ArrowDown, ArrowUp } from 'lucide-react';

const WeatherStats = () => {
  const { weatherData } = useWeather();

  if (!weatherData) return null;

  const { stats } = weatherData;

  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
      <div className="bg-white p-6 rounded-lg shadow-md flex items-center justify-between">
        <div>
          <p className="text-gray-500 text-sm">Average Temp</p>
          <p className="text-3xl font-bold text-gray-800">{stats.avgTemp}°C</p>
        </div>
        <div className="p-3 bg-blue-100 rounded-full text-blue-500">
          <Thermometer size={24} />
        </div>
      </div>

      <div className="bg-white p-6 rounded-lg shadow-md flex items-center justify-between">
        <div>
          <p className="text-gray-500 text-sm">Max Temp</p>
          <p className="text-3xl font-bold text-gray-800">{stats.maxTemp}°C</p>
        </div>
        <div className="p-3 bg-red-100 rounded-full text-red-500">
          <ArrowUp size={24} />
        </div>
      </div>

      <div className="bg-white p-6 rounded-lg shadow-md flex items-center justify-between">
        <div>
          <p className="text-gray-500 text-sm">Min Temp</p>
          <p className="text-3xl font-bold text-gray-800">{stats.minTemp}°C</p>
        </div>
        <div className="p-3 bg-cyan-100 rounded-full text-cyan-500">
          <ArrowDown size={24} />
        </div>
      </div>
    </div>
  );
};

export default WeatherStats;
