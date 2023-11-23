document.addEventListener("DOMContentLoaded", function () {
  const plantTable = document.getElementById("plantTable");

  fetch("/api/all_plants")
    .then((response) => response.json())
    .then((data) => {
      data.plants.forEach((plant) => {
        const row = plantTable.insertRow();
        const nameCell = row.insertCell(0);
        const usesCell = row.insertCell(1);
        nameCell.innerHTML = `<a href="./plant.html?${plant.name}">${plant.name}</a>`;
        usesCell.innerHTML = plant.uses;
      });
    })
    .catch((error) => console.error("Error fetching data:", error));
});

const searchInput = document.getElementById("searchInput");
const table = document.getElementById("plantTable");
const rows = table.getElementsByTagName("tr");

searchInput.addEventListener("keyup", function () {
  const filter = searchInput.value.toLowerCase();

  for (let i = 0; i < rows.length; i++) {
    const row = rows[i];
    const nameColumn = row.getElementsByTagName("td")[0];
    const usesColumn = row.getElementsByTagName("td")[1];

    if (nameColumn) {
      const name = nameColumn.textContent.toLowerCase();
      const uses = usesColumn.textContent.toLowerCase();

      if (name.includes(filter) || uses.includes(filter)) {
        row.style.display = "";
        row.classList.remove("invisible");
      } else {
        row.style.display = "none";
        row.classList.add("invisible");
      }
    }
  }
});
