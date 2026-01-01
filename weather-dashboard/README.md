# Weather Dashboard

A modern Single Page Application (SPA) built with React to analyze and visualize weather data using the OpenWeatherMap API.

## Features

*   **Dynamic Data Analysis**: Calculates Minimum, Maximum, and Average temperatures for the next 5 days.
*   **Interactive Charts**:
    *   Line Chart for daily temperature trends.
    *   Bar Chart for humidity and wind speed analysis.
*   **Clean Architecture**: Separation of concerns with Services, Utils, Context, and Components.
*   **Error Handling**: Graceful handling of invalid cities, API errors, and network issues.
*   **Responsive Design**: Built with Tailwind CSS for a mobile-friendly experience.

## Tech Stack

*   **Frontend**: React.js (Vite)
*   **Styling**: Tailwind CSS
*   **State Management**: Context API
*   **Charts**: Recharts
*   **Icons**: Lucide React
*   **API**: OpenWeatherMap (5 Day / 3 Hour Forecast)

## Getting Started

1.  **Clone the repository**
2.  **Install dependencies**:
    ```bash
    npm install
    ```
3.  **Configure API Key**:
    *   Rename `.env.example` to `.env`.
    *   Add your OpenWeatherMap API key:
        ```
        VITE_OPENWEATHER_API_KEY=your_api_key_here
        ```
4.  **Run the application**:
    ```bash
    npm run dev
    ```

## Technical Case Study: Data Transformation

One of the key challenges was handling the raw data from OpenWeatherMap, which comes in a 3-hour interval list with UNIX timestamps.

**Problem**:
*   Raw data contains ~40 data points (8 per day for 5 days).
*   Timestamps are in UNIX format (seconds).
*   Charts require aggregated data per day (e.g., "Mon", "Tue").

**Solution**:
Implemented a `transformWeatherData` utility function in `src/utils/dataTransformer.js` that:
1.  Iterates through the raw list.
2.  Converts UNIX timestamps to human-readable Weekday/Date strings.
3.  Aggregates temperature, humidity, and wind speed by day.
4.  Calculates daily averages to produce a clean dataset for the charts (e.g., 5 data points instead of 40).
5.  Calculates global Max, Min, and Avg stats for the entire period.

This ensures the UI components receive clean, ready-to-render data, adhering to the principle of separation of concerns.
