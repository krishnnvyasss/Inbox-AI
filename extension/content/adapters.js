(function () {
  "use strict";

  const clean = (value) => String(value || "")
    .replace(/\u00a0/g, " ")
    .replace(/\r/g, "")
    .replace(/[ \t]+\n/g, "\n")
    .replace(/\n{3,}/g, "\n\n")
    .trim();

  const unique = (messages) => {
    const result = [];
    const seen = new Set();
    for (const message of messages) {
      const content = clean(message.content);
      if (!content) continue;
      const key = `${message.role}|${content}`;
      if (seen.has(key)) continue;
      seen.add(key);
      result.push({ role: message.role, content });
    }
    return result;
  };

  const textFrom = (node) => clean(node?.innerText || node?.textContent || "");

  function chatGPT() {
    const nodes = [...document.querySelectorAll("[data-message-author-role]")];
    const messages = nodes.map((node) => ({
      role: node.getAttribute("data-message-author-role") === "user" ? "user" : "assistant",
      content: textFrom(node)
    }));
    return unique(messages);
  }

  function gemini() {
    const nodes = [...document.querySelectorAll("user-query, model-response")];
    const messages = nodes.map((node) => ({
      role: node.tagName.toLowerCase() === "user-query" ? "user" : "assistant",
      content: textFrom(node)
    }));
    return unique(messages);
  }

  function claude() {
    const nodes = [...document.querySelectorAll(
      '[data-testid*="user-message"], [data-testid*="assistant-message"]'
    )];
    const messages = nodes.map((node) => {
      const id = (node.getAttribute("data-testid") || "").toLowerCase();
      return {
        role: id.includes("user") ? "user" : "assistant",
        content: textFrom(node)
      };
    });
    return unique(messages);
  }

  function generic() {
    const candidates = [...document.querySelectorAll("main article")];
    const messages = [];
    for (const node of candidates) {
      const text = textFrom(node);
      if (!text) continue;
      const buttons = [...node.querySelectorAll("button")].map(textFrom).join(" ").toLowerCase();
      const label = `${node.getAttribute("aria-label") || ""} ${buttons}`.toLowerCase();
      let role = null;
      if (label.includes("user")) role = "user";
      if (label.includes("assistant") || label.includes("ai")) role = "assistant";
      if (role) messages.push({ role, content: text });
    }
    return unique(messages);
  }

  window.InboxAIAdapters = { chatGPT, gemini, claude, generic };
})();
