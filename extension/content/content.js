(function () {
  "use strict";

  if (window.__inboxAIInstalled) return;
  window.__inboxAIInstalled = true;

  function getPlatform() {
    const host = location.hostname;
    if (host === "chatgpt.com" || host === "chat.openai.com") return "ChatGPT";
    if (host === "gemini.google.com") return "Gemini";
    if (host === "claude.ai") return "Claude";
    return "Unknown";
  }

  function extract() {
    const platform = getPlatform();
    let messages = [];

    if (platform === "ChatGPT") messages = window.InboxAIAdapters.chatGPT();
    else if (platform === "Gemini") messages = window.InboxAIAdapters.gemini();
    else if (platform === "Claude") messages = window.InboxAIAdapters.claude();
    else messages = window.InboxAIAdapters.generic();

    return {
      platform,
      url: location.href,
      title: document.title,
      captured_at: new Date().toISOString(),
      capture_mode: "dom",
      warnings: [
        "Inbox AI v1 captures messages currently rendered in the page DOM. Virtualized or unloaded older messages may not be included."
      ],
      message_count: messages.length,
      messages: messages.map((message, index) => ({
        id: index + 1,
        role: message.role,
        content: message.content
      }))
    };
  }

  chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request?.type !== "INBOX_AI_CAPTURE") return;
    try {
      sendResponse({ ok: true, data: extract() });
    } catch (error) {
      sendResponse({ ok: false, error: error.message || "Capture failed." });
    }
    return true;
  });
})();
