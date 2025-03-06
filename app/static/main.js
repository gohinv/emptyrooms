const buildingInput = document.getElementById("building");
const buildingsList = document.getElementById("buildingsList");

buildingInput.addEventListener("input", async function() {
  const query = buildingInput.value.trim();
  if (query.length < 1) {
    buildingsList.innerHTML = "";
    return;
  }

  try {
    // Call our /buildings/suggest endpoint
    const resp = await fetch(`/buildings/suggest?query=${encodeURIComponent(query)}`);
    if (!resp.ok) {
      throw new Error(`Server error: ${resp.status}`);
    }
    const suggestions = await resp.json();

    // Clear old suggestions
    buildingsList.innerHTML = "";

    // Add <option> elements for each suggestion
    suggestions.forEach(bldgName => {
      const option = document.createElement("option");
      option.value = bldgName;  // The "value" is what appears if the user selects it
      buildingsList.appendChild(option);
    });
  } catch (error) {
    console.error("Error fetching building suggestions:", error);
  }
});

document.getElementById("queryForm").addEventListener("submit", async function(event) {
    event.preventDefault(); // Prevent form from refreshing the page
    
    const day = document.getElementById("day").value;
    const time = document.getElementById("time").value;
    const building = document.getElementById("building").value;
    
    const url = `/free_rooms?day=${encodeURIComponent(day)}&time=${encodeURIComponent(time)}&building=${encodeURIComponent(building)}`;
    
    try {
        const response = await fetch(url);
        if (!response.ok) {
          throw new Error(`Server error: ${response.status}`);
        }
        const freeRooms = await response.json();
    
        // Clear previous results
        const resultsList = document.getElementById("results");
        resultsList.innerHTML = "";
    
        if (freeRooms.length === 0) {
          const li = document.createElement("li");
          li.textContent = "No free rooms found at that time (and building).";
          resultsList.appendChild(li);
        } else {
          // Display free rooms
          freeRooms.forEach(room => {
            const li = document.createElement("li");
            li.textContent = `${room.building} - Room ${room.room_number}`;
            resultsList.appendChild(li);
          });
        }
    } catch (error) {
        console.error("Error fetching free rooms:", error);
    }
});
