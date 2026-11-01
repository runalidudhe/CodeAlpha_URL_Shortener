
const urlInput = document.getElementById("urlInput");
const shortenBtn = document.getElementById("shortenBtn");
const resultBox = document.getElementById("resultBox");
const shortUrl = document.getElementById("shortUrl");
const errorMessage = document.getElementById("errorMessage");
const copyMessage = document.getElementById("copyMessage");

async function shortenURL() {
    const url = urlInput.value.trim();

    errorMessage.textContent = "";
    copyMessage.textContent = "";
    resultBox.classList.add("hidden");

    if (!url) {
        errorMessage.textContent = "Please enter a URL first.";
        return;
    }

    shortenBtn.disabled = true;
    shortenBtn.textContent = "Processing...";

    try {
        const response = await fetch("/shorten", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ url: url })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message || "Something went wrong.");
        }

        shortUrl.textContent = data.short_url;
        shortUrl.href = data.short_url;

        resultBox.classList.remove("hidden");

        await loadHistory();

    } catch (error) {
        errorMessage.textContent = error.message;

    } finally {
        shortenBtn.disabled = false;
        shortenBtn.textContent = "Shorten URL";
    }
}

async function copyURL() {
    try {
        await navigator.clipboard.writeText(shortUrl.href);
        copyMessage.textContent = "Link copied successfully!";
    } catch {
        copyMessage.textContent = "Unable to copy. Please copy the link manually.";
    }
}

async function loadHistory() {
    const historyList = document.getElementById("historyList");

    try {
        const response = await fetch("/api/urls");
        const data = await response.json();

        historyList.innerHTML = "";

        if (!data.urls || data.urls.length === 0) {
            historyList.innerHTML =
                '<p class="empty-history">No links generated yet.</p>';
            return;
        }

        data.urls.forEach(item => {
            const row = document.createElement("div");
            row.className = "history-row";

            const original = document.createElement("span");
            original.textContent = item.original_url;

            const short = document.createElement("a");
            short.href = item.short_url;
            short.textContent = item.short_code;
            short.target = "_blank";
            short.rel = "noopener noreferrer";

            const clicks = document.createElement("span");
            clicks.textContent = item.clicks;

            row.append(original, short, clicks);
            historyList.appendChild(row);
        });

    } catch {
        historyList.innerHTML =
            '<p class="empty-history">Unable to load URL history.</p>';
    }
}

document.addEventListener("DOMContentLoaded", loadHistory);

urlInput.addEventListener("keydown", event => {
    if (event.key === "Enter") {
        shortenURL();
    }
});
