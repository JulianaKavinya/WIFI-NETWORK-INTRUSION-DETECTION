document.addEventListener("DOMContentLoaded", () => {
    // Placeholder data
    const weatherData = {
        location: "London",
        temperature: "25°C",
        condition: "Sunny"
    };

    // Populate the weather widget
    document.getElementById("location").textContent = weatherData.location;
    document.getElementById("temperature").textContent = weatherData.temperature;
    document.getElementById("condition").textContent = weatherData.condition;
});
