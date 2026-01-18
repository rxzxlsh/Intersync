function showSection(id) {
  document.querySelectorAll(".section").forEach(section => {
    section.classList.remove("active");
  });
  document.getElementById(id).classList.add("active");
}

function generateProjects() {
  const interests = document.getElementById("interestInput").value.trim();
  const container = document.getElementById("projectResults");

  container.innerHTML = "";

  if (!interests) {
    container.innerHTML = `<p>Please enter at least one interest.</p>`;
    return;
  }

  container.innerHTML = `
    <div class="ai-loader">
      <div class="pulse-ring"></div>
      <p>Analyzing interests…</p>
      <span>Connecting to neural intelligence layer</span>
    </div>
  `;
}
