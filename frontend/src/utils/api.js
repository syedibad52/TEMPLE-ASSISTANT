/**
 * API utility functions for communicating with the FastAPI backend.
 */
import { API_BASE_URL } from "@/data/templeData";

/**
 * Generic fetch wrapper with error handling.
 */
async function apiFetch(endpoint, options = {}) {
  const url = `${API_BASE_URL}${endpoint}`;
  try {
    const response = await fetch(url, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        ...options.headers,
      },
    });

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      throw new Error(errorData.detail || `API error: ${response.status}`);
    }

    return response;
  } catch (error) {
    if (error.name === "TypeError" && error.message.includes("fetch")) {
      throw new Error("Cannot connect to the server. Please make sure the backend is running.");
    }
    throw error;
  }
}

/**
 * Send a chat message and get AI response.
 */
export async function sendChatMessage(message, language = "auto", conversationHistory = []) {
  const response = await apiFetch("/api/chat", {
    method: "POST",
    body: JSON.stringify({
      message,
      language,
      conversation_history: conversationHistory,
    }),
  });
  return response.json();
}

/**
 * Send audio blob for speech-to-text transcription.
 */
export async function speechToText(audioBlob) {
  const formData = new FormData();
  formData.append("audio", audioBlob, "recording.webm");

  const url = `${API_BASE_URL}/api/speech-to-text`;
  const response = await fetch(url, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || "Speech recognition failed");
  }

  return response.json();
}

/**
 * Convert text to speech and return audio blob.
 */
export async function textToSpeech(text, language = "en") {
  const url = `${API_BASE_URL}/api/text-to-speech`;
  const response = await fetch(url, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text, language }),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new Error(errorData.detail || "Speech generation failed");
  }

  return response.blob();
}

/**
 * Get current temple status.
 */
export async function getTempleStatus() {
  const response = await apiFetch("/api/temple-status");
  return response.json();
}

/**
 * Get pooja timings.
 */
export async function getPoojaTimings() {
  const response = await apiFetch("/api/pooja-timings");
  return response.json();
}

/**
 * Get festivals.
 */
export async function getFestivals() {
  const response = await apiFetch("/api/festivals");
  return response.json();
}

/**
 * Get announcements.
 */
export async function getAnnouncements() {
  const response = await apiFetch("/api/announcements");
  return response.json();
}

/**
 * Get API health status.
 */
export async function getApiHealth() {
  const response = await apiFetch("/api/health");
  return response.json();
}
