document.getElementById("queryForm").addEventListener("submit", async function(event) {
    event.preventDefault(); // Prevent form from refreshing the page
    
    const day = document.getElementById("day").value;
    const time = document.getElementById("time").value;
    
    const url = `/free_rooms?day=${encodeURIComponent(day)}&time=${encodeURIComponent(time)}`;
    
    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error(`Server error: ${response.status}`);
      }
      const freeRooms = await response.json();
      
      // Group results by building
      const groupedRooms = {};
      freeRooms.forEach(room => {
        const building = room.building;
        const roomNumber = room.room_number;
        if (!groupedRooms[building]) {
          groupedRooms[building] = [];
        }
        groupedRooms[building].push(roomNumber);
      });
      
      // Sort building names alphabetically
      const sortedBuildings = Object.keys(groupedRooms).sort();
      
      // Prepare the results list
      const resultsList = document.getElementById("results");
      resultsList.innerHTML = ""; // Clear previous results
      
      if (sortedBuildings.length === 0) {
        const li = document.createElement("li");
        li.textContent = "No free rooms found at that time.";
        resultsList.appendChild(li);
      } else {
        // For each building, sort room numbers numerically and display them
        sortedBuildings.forEach(building => {
          const buildingLi = document.createElement("li");
          buildingLi.textContent = building; // Building name header
          const roomList = document.createElement("ul");
          
          // Sort room numbers numerically (assuming they can be parsed as integers)
          const sortedRoomNumbers = groupedRooms[building].sort((a, b) => parseInt(a, 10) - parseInt(b, 10));
          
          sortedRoomNumbers.forEach(roomNumber => {
            const roomLi = document.createElement("li");
            roomLi.textContent = `Room ${roomNumber}`;
            roomList.appendChild(roomLi);
          });
          
          buildingLi.appendChild(roomList);
          resultsList.appendChild(buildingLi);
        });
      }
    } catch (error) {
      console.error("Error fetching free rooms:", error);
    }
  });
