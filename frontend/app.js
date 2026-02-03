const API_BASE = "http://127.0.0.1:8000";
let currentTheme = localStorage.getItem("theme") || "dark";
let currentUserId = null;

// ============= TOAST NOTIFICATIONS =============

function createToast(message, type = "info", duration = 3000) {
  const toast = document.createElement("div");
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `
    <div class="toast-content">
      <span>${message}</span>
      <button onclick="this.parentElement.parentElement.remove()" class="toast-close">✕</button>
    </div>
  `;
  document.body.appendChild(toast);

  setTimeout(() => {
    toast.classList.add("toast-show");
  }, 10);

  setTimeout(() => {
    toast.classList.remove("toast-show");
    setTimeout(() => toast.remove(), 300);
  }, duration);
}

// ============= BACKGROUND EFFECT =============

class BackgroundEffect {
  constructor() {
    this.mouseX = window.innerWidth / 2;
    this.mouseY = window.innerHeight / 2;
    this.createBackground();
    this.init();
  }

  createBackground() {
    const bg = document.createElement("div");
    bg.className = "animated-bg";
    bg.innerHTML = `
      <div class="bg-blob blob1"></div>
      <div class="bg-blob blob2"></div>
      <div class="bg-blob blob3"></div>
      <div class="bg-light"></div>
    `;
    document.body.insertBefore(bg, document.body.firstChild);
  }

  init() {
    document.addEventListener("mousemove", (e) => {
      this.mouseX = e.clientX;
      this.mouseY = e.clientY;
      this.updateBackgroundLight();
    });
  }

  updateBackgroundLight() {
    const light = document.querySelector(".bg-light");
    if (light) {
      light.style.left = this.mouseX + "px";
      light.style.top = this.mouseY + "px";
    }
  }
}

// Initialize background effect when page loads
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", () => new BackgroundEffect());
} else {
  new BackgroundEffect();
}

// ============= UTILITY FUNCTIONS =============

function showError(message) {
  createToast(message, "error", 4000);
}

function showSuccess(message) {
  createToast(message, "success", 3000);
}

function showInfo(message) {
  createToast(message, "info", 3000);
}


function checkAuth() {
  const token = localStorage.getItem("token");
  if (!token) {
    location.href = "index.html";
  }
  return token;
}

// ============= REGISTER FLOW =============

async function registerStep1() {
  const name = document.getElementById("name")?.value.trim();
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value.trim();

  if (!name || !email || !password) {
    showError("All fields are required");
    return;
  }

  if (password.length < 6) {
    showError("Password must be at least 6 characters");
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/auth/register?name=${encodeURIComponent(name)}&email=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" }
    });

    const data = await res.json();
    if (!res.ok) {
      showError(data.detail || "Registration failed");
      return;
    }

    localStorage.setItem("reg_email", email);
    localStorage.setItem("reg_password", password);
    showSuccess("OTP sent to your email");
    setTimeout(() => location.href = "register-verify.html", 1500);
  } catch (error) {
    showError(error.message);
  }
}

async function registerStep2() {
  const email = localStorage.getItem("reg_email");
  const otp = document.getElementById("otp").value.trim();

  if (!otp) {
    showError("Please enter OTP");
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/auth/register/verify-otp?email=${encodeURIComponent(email)}&otp=${encodeURIComponent(otp)}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" }
    });

    const data = await res.json();
    if (!res.ok) {
      showError(data.detail || "Invalid OTP");
      return;
    }

    showSuccess("Registration successful! Redirecting to login...");
    localStorage.removeItem("reg_email");
    localStorage.removeItem("reg_password");
    setTimeout(() => location.href = "index.html", 1500);
  } catch (error) {
    showError(error.message);
  }
}

// ============= LOGIN FLOW =============

async function loginStep1() {
  const email = document.getElementById("email").value.trim();
  const password = document.getElementById("password").value.trim();

  if (!email || !password) {
    showError("Email and password are required");
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/auth/login?email=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" }
    });

    const data = await res.json();
    if (!res.ok) {
      showError(data.detail || "Login failed");
      return;
    }

    localStorage.setItem("login_email", email);
    showSuccess("OTP sent to your email");
    setTimeout(() => location.href = "login-verify.html", 1500);
  } catch (error) {
    showError(error.message);
  }
}

async function loginStep2() {
  const email = localStorage.getItem("login_email");
  const otp = document.getElementById("otp").value.trim();

  if (!otp) {
    showError("Please enter OTP");
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/auth/login/verify?email=${encodeURIComponent(email)}&otp=${encodeURIComponent(otp)}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" }
    });

    const data = await res.json();
    if (!res.ok) {
      showError(data.detail || "Invalid OTP");
      return;
    }

    localStorage.setItem("token", data.token);
    localStorage.removeItem("login_email");
    showSuccess("Login successful! Redirecting...");
    setTimeout(() => location.href = "chat.html", 1500);
  } catch (error) {
    showError(error.message);
  }
}

// ============= FORGOT PASSWORD FLOW =============

async function forgotPasswordStep1() {
  const email = document.getElementById("email").value.trim();

  if (!email) {
    showError("Please enter your email");
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/auth/forgot-password?email=${encodeURIComponent(email)}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" }
    });

    const data = await res.json();
    if (!res.ok) {
      showError(data.detail || "Email not found");
      return;
    }

    localStorage.setItem("reset_email", email);
    showSuccess("OTP sent to your email");
    setTimeout(() => location.href = "reset.html", 1500);
  } catch (error) {
    showError(error.message);
  }
}

async function resetPassword() {
  const email = localStorage.getItem("reset_email");
  const otp = document.getElementById("otp").value.trim();
  const newPassword = document.getElementById("password").value.trim();

  if (!otp || !newPassword) {
    showError("Please enter OTP and new password");
    return;
  }

  if (newPassword.length < 6) {
    showError("Password must be at least 6 characters");
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/auth/reset-password?email=${encodeURIComponent(email)}&otp=${encodeURIComponent(otp)}&new_password=${encodeURIComponent(newPassword)}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" }
    });

    const data = await res.json();
    if (!res.ok) {
      showError(data.detail || "Reset failed");
      return;
    }

    showSuccess("Password reset successful! Redirecting to login...");
    localStorage.removeItem("reset_email");
    setTimeout(() => location.href = "index.html", 1500);
  } catch (error) {
    showError(error.message);
  }
}

// ============= CHAT FLOW =============

let selectedDocumentId = null;
let selectedDocumentName = null;

function selectDocument(event) {
  const file = event.target.files[0];
  if (!file) return;

  const docDiv = document.getElementById("selectedDocument");
  selectedDocumentName = file.name;
  docDiv.innerHTML = `✅ Document selected: <strong>${file.name}</strong> <button onclick="clearDocument()" style="margin-left: 10px; padding: 2px 8px; background: #ff6b6b; border: none; border-radius: 4px; color: white; cursor: pointer; font-size: 12px;">Remove</button>`;
  docDiv.classList.add("show");
  
  // In a real scenario, you'd upload the document here
  // For now, just show it's selected
  console.log("Document selected:", file.name);
}

function clearDocument() {
  selectedDocumentId = null;
  selectedDocumentName = null;
  document.getElementById("docSelect").value = "";
  const docDiv = document.getElementById("selectedDocument");
  docDiv.classList.remove("show");
  docDiv.innerHTML = "";
}

async function sendMessage() {
  const token = checkAuth();
  const message = document.getElementById("message").value.trim();

  if (!message) {
    showError("Please type a message");
    return;
  }

  const chatBox = document.getElementById("chat");
  const timestamp = new Date().toLocaleTimeString();
  chatBox.innerHTML += `<div class="msg user"><span class="msg-time">${timestamp}</span>You: ${message}</div>`;
  document.getElementById("message").value = "";

  // Show loading indicator
  const loadingId = "loading-" + Date.now();
  chatBox.innerHTML += `<div class="msg ai" id="${loadingId}"><span class="loading-dots">⏳ AI is thinking<span class="dot">.</span><span class="dot">.</span><span class="dot">.</span></span></div>`;
  chatBox.scrollTop = chatBox.scrollHeight;

  try {
    const res = await fetch(`${API_BASE}/chat?message=${encodeURIComponent(message)}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      }
    });

    const data = await res.json();
    if (!res.ok) {
      document.getElementById(loadingId)?.remove();
      showError(data.detail || "Chat failed");
      return;
    }

    // Remove loading indicator and add response
    document.getElementById(loadingId)?.remove();
    const responseTimestamp = new Date().toLocaleTimeString();
    chatBox.innerHTML += `<div class="msg ai"><span class="msg-time">${responseTimestamp}</span>AI: ${data.reply}</div>`;
    chatBox.scrollTop = chatBox.scrollHeight;
  } catch (error) {
    document.getElementById(loadingId)?.remove();
    showError(error.message);
  }
}

async function loadChatHistory() {
  const token = checkAuth();

  try {
    const res = await fetch(`${API_BASE}/chat/history`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      }
    });

    const messages = await res.json();
    if (!res.ok) {
      showError("Failed to load history");
      return;
    }

    const historyDiv = document.getElementById("history");
    if (messages.length === 0) {
      historyDiv.innerHTML = "<p>No chat history yet</p>";
      return;
    }

    historyDiv.innerHTML = messages.map(msg => {
      const time = new Date(msg.timestamp).toLocaleString();
      return `<div class="msg-with-actions">
        <div class="msg ${msg.role}">
          <span class="msg-time">${time}</span>
          ${msg.role === 'user' ? 'You' : 'AI'}: ${msg.content}
        </div>
        <div class="msg-actions">
          <button class="msg-action-btn" title="Copy" onclick="copyToClipboard('${msg.content.replace(/'/g, "\\'")}')">📋</button>
          <button class="msg-action-btn" title="Delete" onclick="deleteMessage(this)">🗑️</button>
        </div>
      </div>`;
    }).join("");
  } catch (error) {
    showError(error.message);
  }
}

function copyToClipboard(text) {
  navigator.clipboard.writeText(text).then(() => {
    showSuccess("Copied to clipboard!");
  }).catch(err => {
    showError("Failed to copy");
  });
}

function deleteMessage(btn) {
  btn.parentElement.parentElement.remove();
  showInfo("Message removed from view");
}

async function searchHistory() {
  const token = checkAuth();
  const query = prompt("Search chat history:");
  if (!query) return;

  try {
    const res = await fetch(`${API_BASE}/chat/history`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      }
    });

    const messages = await res.json();
    const filtered = messages.filter(msg => 
      msg.content.toLowerCase().includes(query.toLowerCase())
    );

    const historyDiv = document.getElementById("history");
    if (filtered.length === 0) {
      historyDiv.innerHTML = "<p>No results found for: " + query + "</p>";
      return;
    }

    historyDiv.innerHTML = filtered.map(msg => {
      const time = new Date(msg.timestamp).toLocaleString();
      return `<div class="msg-with-actions">
        <div class="msg ${msg.role}">
          <span class="msg-time">${time}</span>
          ${msg.role === 'user' ? 'You' : 'AI'}: ${msg.content}
        </div>
        <div class="msg-actions">
          <button class="msg-action-btn" title="Copy" onclick="copyToClipboard('${msg.content.replace(/'/g, "\\'")}')">📋</button>
        </div>
      </div>`;
    }).join("");
  } catch (error) {
    showError(error.message);
  }
}

async function exportChatHistory() {
  const token = checkAuth();

  try {
    const res = await fetch(`${API_BASE}/chat/history`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      }
    });

    const messages = await res.json();
    if (messages.length === 0) {
      showError("No chat history to export");
      return;
    }

    let content = "=== AI CHATBOT HISTORY ===\n\n";
    messages.forEach(msg => {
      const time = new Date(msg.timestamp).toLocaleString();
      content += `[${time}] ${msg.role === 'user' ? 'You' : 'AI'}:\n${msg.content}\n\n`;
    });

    const blob = new Blob([content], { type: "text/plain" });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = `chat-history-${Date.now()}.txt`;
    a.click();
    window.URL.revokeObjectURL(url);
    showSuccess("Chat history exported!");
  } catch (error) {
    showError(error.message);
  }
}

async function deleteHistory() {
  const token = checkAuth();

  if (!confirm("Are you sure you want to delete all chat history? This action cannot be undone.")) {
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/chat/history`, {
      method: "DELETE",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      }
    });

    const data = await res.json();
    if (!res.ok) {
      showError(data.detail || "Failed to delete history");
      return;
    }

    showSuccess("Chat history deleted successfully");
    setTimeout(() => location.reload(), 1500);
  } catch (error) {
    showError(error.message);
  }
}

// ============= DOCUMENT FLOW =============

async function uploadDocument() {
  const token = checkAuth();
  const fileInput = document.getElementById("file");
  const file = fileInput.files[0];

  if (!file) {
    showError("Please select a file");
    return;
  }

  const formData = new FormData();
  formData.append("file", file);

  try {
    const res = await fetch(`${API_BASE}/upload`, {
      method: "POST",
      headers: {
        "Authorization": `Bearer ${token}`
      },
      body: formData
    });

    const data = await res.json();
    if (!res.ok) {
      showError(data.detail || "Upload failed");
      return;
    }

    showSuccess("File uploaded successfully!");
    setTimeout(() => location.href = "documents.html", 1500);
  } catch (error) {
    showError(error.message);
  }
}

async function loadDocuments() {
  const token = checkAuth();

  try {
    const res = await fetch(`${API_BASE}/documents`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      }
    });

    const docs = await res.json();
    if (!res.ok) {
      showError("Failed to load documents");
      return;
    }

    const docsDiv = document.getElementById("documents");
    if (docs.length === 0) {
      docsDiv.innerHTML = "<p>No documents uploaded yet</p>";
      return;
    }

    docsDiv.innerHTML = docs.map(doc => 
      `<div class="doc-item" onclick="chatWithDocument(${doc.id})">${doc.filename}</div>`
    ).join("");
  } catch (error) {
    showError(error.message);
  }
}

async function chatWithDocument(docId) {
  const token = checkAuth();
  const question = document.getElementById("message").value.trim();

  if (!question) {
    showError("Please enter a question");
    return;
  }

  const chatBox = document.getElementById("chat");
  chatBox.innerHTML += `<div class="msg user">You: ${question}</div>`;
  document.getElementById("message").value = "";

  try {
    const res = await fetch(`${API_BASE}/document/chat?document_id=${docId}&question=${encodeURIComponent(question)}`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${token}`
      }
    });

    const data = await res.json();
    if (!res.ok) {
      showError(data.detail || "Chat failed");
      return;
    }

    chatBox.innerHTML += `<div class="msg ai">AI: ${data.answer}</div>`;
    chatBox.scrollTop = chatBox.scrollHeight;
  } catch (error) {
    showError(error.message);
  }
}

// ============= PAGE INITIALIZATION =============

function logout() {
  localStorage.removeItem("token");
  localStorage.removeItem("login_email");
  location.href = "index.html";
}
// ============= THEME TOGGLE =============

function toggleTheme() {
  currentTheme = currentTheme === "dark" ? "light" : "dark";
  localStorage.setItem("theme", currentTheme);
  document.body.setAttribute("data-theme", currentTheme);
  showInfo(`Switched to ${currentTheme} mode`);
}

function initTheme() {
  document.body.setAttribute("data-theme", currentTheme);
}

// Initialize theme on page load
if (document.readyState === "loading") {
  document.addEventListener("DOMContentLoaded", initTheme);
} else {
  initTheme();
}

// ============= KEYBOARD SHORTCUTS =============

document.addEventListener("keydown", (e) => {
  // Cmd/Ctrl + K for quick search
  if ((e.ctrlKey || e.metaKey) && e.key === "k") {
    e.preventDefault();
    if (typeof searchHistory === "function") {
      searchHistory();
    }
  }
  // Cmd/Ctrl + E for export
  if ((e.ctrlKey || e.metaKey) && e.key === "e") {
    e.preventDefault();
    if (typeof exportChatHistory === "function") {
      exportChatHistory();
    }
  }
  // Cmd/Ctrl + T for theme toggle
  if ((e.ctrlKey || e.metaKey) && e.key === "t") {
    e.preventDefault();
    toggleTheme();
  }
});