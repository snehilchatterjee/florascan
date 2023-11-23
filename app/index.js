const apiUrl = "/api/predict/";

// Get references to the <div>, <img>, and file input elements
const imageDiv = document.getElementById("image-div");
const myImage = document.getElementById("input-image");
const imageInput = document.getElementById("image-input");
const inputLabel = document.getElementById("input-label");
const scanButton = document.getElementById("scan");

// Add a click event listener to the <div>
imageDiv.addEventListener("click", () => {
  // Trigger the file input dialog when the div is clicked
  imageInput.click();
});

// Add an event listener to the file input to handle image selection
imageInput.addEventListener("change", (event) => {
  const selectedFile = event.target.files[0];

  if (selectedFile) {
    // Read the selected image as a base64 encoded string
    const reader = new FileReader();

    reader.onload = function () {
      // Set the base64 string as the src of the image element
      myImage.src = reader.result;
      myImage.alt = "Selected Image";
      inputLabel.style.display = "none";
      myImage.style.display = "block";
    };

    reader.readAsDataURL(selectedFile);
  }
});

scanButton.addEventListener("click", () => {
  const selectedFile = imageInput.files[0];

  if (selectedFile) {
    console.log(selectedFile);
    const reader = new FileReader();
    document.getElementById("info").textContent = "Scanning...";
    reader.onload = function () {
      const base64Image = reader.result.split(",")[1]; // Get the base64 image data
      // Create a JSON object with the base64 image
      const imageData = { image: base64Image };
      // Send the image data as a JSON POST request to the server
      fetch(apiUrl, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(imageData),
      })
        .then((response) => response.json())
        .then((data) => {
          // Handle the response from the server
          console.log(data);
          window.location.href = `./plant.html?${data.prediction}`;
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    };

    reader.readAsDataURL(selectedFile);
  } else {
    document.getElementById("info").textContent = "Please select an image.";
  }
});
