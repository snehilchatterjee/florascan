document.addEventListener("DOMContentLoaded", function () {
  // Replace this with the actual API URL
  const api = "/api/plant/";

  // Get the plant ID from the URL
  var plantId = window.location.search;
  if (!plantId) {
    plantId = "_";
  }
  console.log(plantId);
  plantId = plantId.replace("?", "");
  const apiUrl = api + plantId;

  // Fetch plant data from the API
  fetch(apiUrl)
    .then((response) => response.json())
    .then((plantData) => {
      if (plantData && !plantData.error) {
        // Update the scientific name, common name, and uses
        document.getElementById("binomial-name").textContent =
          plantData.binomial_name;
        document.getElementById("common-name").textContent =
          plantData.common_name;
        document.getElementById("uses").textContent = plantData.uses;

        // Show the state images based on the plant's distribution
        plantData.states.forEach((state) => {
          const lowercaseState = state.toLowerCase();
          const stateImage = document.getElementById(`state-${lowercaseState}`);
          if (stateImage) {
            stateImage.style.display = "block";
          }
        });
      } else {
        // Handle the case when no plant data is found
        document.getElementById("binomial-name").textContent =
          "Plant not found";
        document.getElementById("common-name").textContent = "N/A";
        document.getElementById("uses").textContent = "N/A";
      }
    })
    .catch((error) => {
      console.error("Error fetching plant information:", error);
    });
});
