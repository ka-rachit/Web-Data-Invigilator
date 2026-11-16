function extractVisibleForm() {
  const nodes = Array.from(document.querySelectorAll("input, textarea, select"));
  const fields = nodes.filter(el => {
    const type = (el.getAttribute("type") || "").toLowerCase();
    return !["password", "hidden", "file", "submit", "button", "reset"].includes(type)
      && !el.disabled && el.getClientRects().length > 0;
  }).slice(0, 100).map((el, index) => {
    const label = el.labels?.[0]?.innerText?.trim() || el.getAttribute("aria-label") || el.placeholder || el.name || el.id || `Field ${index + 1}`;
    return { index, tag: el.tagName.toLowerCase(), type: el.type || "text", label: label.slice(0, 250), name: (el.name || "").slice(0, 250), id: (el.id || "").slice(0, 250), required: !!el.required,
      options: el.tagName === "SELECT" ? Array.from(el.options).slice(0, 25).map(o => o.text.slice(0, 120)) : undefined };
  });
  return { page_url: location.href, page_title: document.title, fields };
}
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg?.type === "EXTRACT_FORM") sendResponse(extractVisibleForm());
});
