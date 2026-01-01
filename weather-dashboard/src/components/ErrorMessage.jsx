import React, { useEffect } from 'react';
import { useWeather } from '../context/WeatherContext';
import { AlertCircle, X } from 'lucide-react';

const ErrorMessage = () => {
  const { error, clearError } = useWeather();

  // Auto-dismiss after 5 seconds
  useEffect(() => {
    if (error) {
      const timer = setTimeout(() => {
        clearError();
      }, 5000);
      return () => clearTimeout(timer);
    }
  }, [error, clearError]);

  if (!error) return null;

  return (
    <div className="fixed bottom-4 right-4 bg-red-100 border-l-4 border-red-500 text-red-700 p-4 rounded shadow-lg z-50 flex items-center gap-3 animate-fade-in-up">
      <AlertCircle size={24} />
      <div>
        <p className="font-bold">Error</p>
        <p>{error}</p>
      </div>
      <button
        onClick={clearError}
        className="ml-auto text-red-700 hover:text-red-900"
      >
        <X size={20} />
      </button>
    </div>
  );
};

export default ErrorMessage;
