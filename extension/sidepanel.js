let formSnapshot = null;
const $ = id => document.getElementById(id);
async function loadSettings() { const s = await chrome.storage.local.get(["apiUrl", "apiKey"]); $("apiUrl").value = s.apiUrl || "http://127.0.0.1:8000"; $("apiKey").value = s.apiKey || ""; }
async function getSettings() { return { apiUrl: $("apiUrl").value.trim().replace(/\/$/, ""), apiKey: $("apiKey").value.trim() }; }
$("saveSettings").addEventListener("click", async () => { await chrome.storage.local.set(await getSettings()); $("status").textContent = "Saved locally."; });
$("scanForm").addEventListener("click", async () => {
  const [tab] = await chrome.tabs.query({ active: true, currentWindow: true });
  try { formSnapshot = await chrome.tabs.sendMessage(tab.id, { type: "EXTRACT_FORM" }); $("fields").textContent = JSON.stringify(formSnapshot, null, 2); $("status").textContent = `Found ${formSnapshot.fields.length} visible fields.`; }
  catch { $("status").textContent = "Could not inspect this page (Chrome internal pages are unsupported)."; }
});
$("getSuggestions").addEventListener("click", async () => {
  if (!formSnapshot) { $("status").textContent = "Inspect the form first."; return; }
  const s = await getSettings(); if (!s.apiKey) { $("status").textContent = "Set API key first."; return; }
  $("status").textContent = "Requesting Gemini suggestions…";
  try {
    const r = await fetch(`${s.apiUrl}/v1/agent/form-assist`, { method: "POST", headers: { "Content-Type": "application/json", Authorization: `Bearer ${s.apiKey}` }, body: JSON.stringify({ page_url: formSnapshot.page_url, page_title: formSnapshot.page_title, fields: formSnapshot.fields, user_instruction: $("instruction").value }) });
    const data = await r.json(); if (!r.ok) throw Error(data.detail || `HTTP ${r.status}`);
    $("response").textContent = data.suggestions || JSON.stringify(data, null, 2); $("status").textContent = "Suggestions ready. Review and manually fill in this MVP.";
  } catch (e) { $("status").textContent = `Request failed: ${e.message}`; }
});
loadSettings();
