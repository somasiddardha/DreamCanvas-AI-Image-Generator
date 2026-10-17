const promptInput = document.getElementById("prompt");
const charCount = document.getElementById("char-count");
const generateBtn = document.getElementById("generate-btn");
const buttonLabel = document.getElementById("button-label");
const statusLabel = document.getElementById("status");
const emptyState = document.getElementById("empty-state");
const loadingState = document.getElementById("loading-state");
const errorState = document.getElementById("error-state");
const errorMessage = document.getElementById("error-message");
const generatedImage = document.getElementById("generated-image");
const imageActions = document.getElementById("image-actions");
const downloadBtn = document.getElementById("download-btn");

let latestImageUrl = "";

promptInput.addEventListener("input", () => {
  charCount.textContent = `${promptInput.value.length} / 1000`;
});

document.querySelectorAll(".example-chip").forEach((chip) => {
  chip.addEventListener("click", () => {
    promptInput.value = chip.dataset.prompt || "";
    charCount.textContent = `${promptInput.value.length} / 1000`;
    promptInput.focus();
  });
});

function showOnly(state) {
  [emptyState, loadingState, errorState, generatedImage].forEach((el) => el.classList.add("hidden"));
  state.classList.remove("hidden");
}

generateBtn.addEventListener("click", async () => {
  const prompt = promptInput.value.trim();
  if (!prompt) {
    promptInput.focus();
    promptInput.setCustomValidity("Please enter a prompt first.");
    promptInput.reportValidity();
    promptInput.setCustomValidity("");
    return;
  }

  generateBtn.disabled = true;
  buttonLabel.textContent = "Generating…";
  statusLabel.textContent = "CREATING IMAGE";
  imageActions.classList.add("hidden");
  showOnly(loadingState);

  try {
    const response = await fetch("/api/generate", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt }),
    });
    const data = await response.json();

    if (!response.ok) throw new Error(data.error || "Image generation failed.");
    latestImageUrl = data.image;
    generatedImage.src = latestImageUrl;
    generatedImage.alt = `AI-generated image: ${prompt}`;
    showOnly(generatedImage);
    imageActions.classList.remove("hidden");
    statusLabel.textContent = "IMAGE READY";
  } catch (error) {
    errorMessage.textContent = error.message || "Something went wrong. Please try again.";
    showOnly(errorState);
    statusLabel.textContent = "GENERATION FAILED";
  } finally {
    generateBtn.disabled = false;
    buttonLabel.textContent = "Generate image";
  }
});

downloadBtn.addEventListener("click", () => {
  if (!latestImageUrl) return;
  const link = document.createElement("a");
  link.href = latestImageUrl;
  link.download = `dreamcanvas-${new Date().toISOString().replace(/[:.]/g, "-")}.png`;
  document.body.appendChild(link);
  link.click();
  link.remove();
});
