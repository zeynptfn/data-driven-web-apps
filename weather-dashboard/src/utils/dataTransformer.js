/**
 * Transforms the raw OpenWeatherMap API data into a format suitable for the application.
 *
 * Problem: API returns data with UNIX timestamps and in a list of 3-hour intervals.
 * Solution: Convert timestamps to readable dates and aggregate data by day for charts.
 *
 * @param {Object} rawData - The raw JSON response from the API.
 * @returns {Object} - An object containing statistics and formatted chart data.
 */
export const transformWeatherData = (rawData) => {
  if (!rawData || !rawData.list) {
    return null;
  }

  const dailyDataMap = new Map();
  let totalTemp = 0;
  let minTemp = Infinity;
  let maxTemp = -Infinity;
  const list = rawData.list;

  // Process each 3-hour interval
  list.forEach((item) => {
    const date = new Date(item.dt * 1000);
    // Get local date string (e.g., "Mon", "Tue")
    // Using 'en-US' for consistency with the example, but could be dynamic.
    const dayName = date.toLocaleDateString('en-US', { weekday: 'short' });
    const fullDate = date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });

    const temp = item.main.temp;
    const humidity = item.main.humidity;
    const wind = item.wind.speed;

    // Global stats calculation
    totalTemp += temp;
    if (temp < minTemp) minTemp = temp;
    if (temp > maxTemp) maxTemp = temp;

    // Aggregation by day for charts
    // We use the full date as key to distinguish unique days
    const key = date.toDateString();

    if (!dailyDataMap.has(key)) {
      dailyDataMap.set(key, {
        dayName,
        fullDate,
        temps: [],
        humidities: [],
        winds: [],
      });
    }

    const dayData = dailyDataMap.get(key);
    dayData.temps.push(temp);
    dayData.humidities.push(humidity);
    dayData.winds.push(wind);
  });

  // Calculate averages for each day to create chart data
  const chartData = Array.from(dailyDataMap.values()).map((day) => {
    const avgTemp = day.temps.reduce((sum, val) => sum + val, 0) / day.temps.length;
    const avgHumidity = day.humidities.reduce((sum, val) => sum + val, 0) / day.humidities.length;
    const avgWind = day.winds.reduce((sum, val) => sum + val, 0) / day.winds.length;

    return {
      date: day.dayName, // "Mon"
      fullDate: day.fullDate, // "Jan 1"
      temperature: Number(avgTemp.toFixed(1)),
      humidity: Number(avgHumidity.toFixed(1)),
      wind: Number(avgWind.toFixed(1)),
    };
  });

  // Calculate global averages
  const avgTempGlobal = totalTemp / list.length;

  return {
    stats: {
      maxTemp: Number(maxTemp.toFixed(1)),
      minTemp: Number(minTemp.toFixed(1)),
      avgTemp: Number(avgTempGlobal.toFixed(1)),
      city: rawData.city.name,
      country: rawData.city.country,
    },
    chartData: chartData.slice(0, 5) // Ensure we only show 5 days if more come in
  };
};
