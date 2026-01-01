import React from 'react';
import { WeatherProvider } from './context/WeatherContext';
import SearchBar from './components/SearchBar';
import WeatherStats from './components/WeatherStats';
import Charts from './components/Charts';
import ErrorMessage from './components/ErrorMessage';
import { CloudSun } from 'lucide-react';

function App() {
  return (
    <WeatherProvider>
      <div className="min-h-screen bg-gray-100 py-10 px-4 sm:px-6 lg:px-8">
        <div className="max-w-5xl mx-auto">

          <header className="mb-10 text-center">
            <div className="flex items-center justify-center mb-4 text-blue-600">
              <CloudSun size={48} />
            </div>
            <h1 className="text-4xl font-extrabold text-gray-900 tracking-tight">
              Weather Dashboard
            </h1>
            <p className="mt-2 text-lg text-gray-600">
              Analyze weather trends with interactive charts
            </p>
          </header>

          <main className="space-y-8">
            <SearchBar />
            <ErrorMessage />

            <div className="transition-all duration-500 ease-in-out">
              <WeatherStats />
              <Charts />
            </div>
          </main>

          <footer className="mt-16 text-center text-gray-500 text-sm">
            <p>Powered by OpenWeatherMap API & React</p>
          </footer>
        </div>
      </div>
    </WeatherProvider>
  );
}

export default App;
