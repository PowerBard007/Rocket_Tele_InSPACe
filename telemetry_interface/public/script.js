// Replace with your actual Flask API URL
const API_URL = "http://localhost:5000/api/telemetry";

async function fetchTelemetryData() {
    try {
        const response = await fetch(API_URL);
        const data = await response.json();

        document.getElementById('altitude').innerText = data.altitude;
        document.getElementById('pressure').innerText = data.pressure;
        document.getElementById('temperature').innerText = data.temperature;
    } catch (error) {
        console.error("Error fetching telemetry data:", error);
    }
}

// Fetch data every 5 seconds
setInterval(fetchTelemetryData, 5000);
