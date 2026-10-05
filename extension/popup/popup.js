(function () {
  "use strict";

  const $ = (id) => document.getElementById(id);
  const captureButton = $("capture");
  const copyButton = $("copy");
  const downloadButton = $("download");
  const preview = $("preview");
  const status = $("status");
  const platform = $("platform");
  const stats = $("stats");
  const messageCount = $("messageCount");
  const charCount = $("charCount");

  let lastJSON = "";

  function setStatus(message) { status.textContent = message; }

  function buildPortableJSON(data) {
    return {
      inbox_ai: {
        version: "1.0",
        exported_at: new Date().toISOString()
      },
      source: {
        platform: data.platform,
        url: data.url,
        title: data.title,
        captured_at: data.captured_at,
        capture_mode: data.capture_mode,
        warnings: data.warnings
      },
      conversation: {
        message_count: data.message_count,
        messages: data.messages
      }
    };
  }

  async function getActiveTab() {
    const tabs = await chrome.tabs.query({ active: true, currentWindow: true });
    return tabs[0];
  }

  async function capture() {
    captureButton.disabled = true;
    setStatus("Capturing...");

    try {
      const tab = await getActiveTab();
      if (!tab?.id || !/^https:\/\/(chatgpt\.com|chat\.openai\.com|gemini\.google\.com|claude\.ai)\//.test(tab.url || "")) {
        throw new Error("Open a ChatGPT, Gemini, or Claude conversation first.");
      }

      const response = await chrome.tabs.sendMessage(tab.id, { type: "INBOX_AI_CAPTURE" });
      if (!response?.ok) throw new Error(response?.error || "Capture failed.");

      const portable = buildPortableJSON(response.data);
      lastJSON = JSON.stringify(portable, null, 2);
      preview.value = lastJSON;
      platform.textContent = response.data.platform;
      messageCount.textContent = response.data.message_count;
      charCount.textContent = response.data.messages.reduce((sum, m) => sum + m.content.length, 0).toLocaleString();
      stats.classList.remove("hidden");
      copyButton.disabled = false;
      downloadButton.disabled = false;

      setStatus(response.data.message_count
        ? `Captured ${response.data.message_count} messages.`
        : "No rendered messages were found. Try opening the conversation fully first.");
    } catch (error) {
      setStatus(error.message || "Capture failed.");
    } finally {
      captureButton.disabled = false;
    }
  }

  async function copyJSON() {
    if (!lastJSON) return;
    await navigator.clipboard.writeText(lastJSON);
    setStatus("JSON copied to clipboard.");
  }

  function downloadJSON() {
    if (!lastJSON) return;
    const blob = new Blob([lastJSON], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `inbox-ai-${new Date().toISOString().replace(/[:.]/g, "-")}.json`;
    a.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
    setStatus("JSON downloaded.");
  }

  captureButton.addEventListener("click", capture);
  copyButton.addEventListener("click", copyJSON);
  downloadButton.addEventListener("click", downloadJSON);
})();
