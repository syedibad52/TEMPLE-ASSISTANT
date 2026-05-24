"use client";
import { useState, useRef, useEffect, useCallback } from "react";
import { useVoiceRecorder } from "@/hooks/useVoiceRecorder";
import { sendChatMessage, speechToText, textToSpeech } from "@/utils/api";
import { EXAMPLE_QUESTIONS } from "@/data/templeData";

export default function VoiceAssistant() {
  const [messages, setMessages] = useState([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [processingStage, setProcessingStage] = useState("");
  const [selectedLang, setSelectedLang] = useState("auto");
  const [textInput, setTextInput] = useState("");
  const [error, setError] = useState(null);

  const { isRecording, waveformData, duration, startRecording, stopRecording, error: recorderError } = useVoiceRecorder();
  const messagesEndRef = useRef(null);
  const audioRef = useRef(null);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  // Handle recorder errors
  useEffect(() => {
    if (recorderError) setError(recorderError);
  }, [recorderError]);

  /**
   * Full voice flow: record → STT → AI → TTS → play
   */
  const handleVoiceInteraction = useCallback(async () => {
    if (isRecording) {
      // Stop recording and process
      const audioBlob = await stopRecording();
      if (!audioBlob) return;

      setIsProcessing(true);
      setError(null);

      try {
        // Stage 1: Speech-to-Text
        setProcessingStage("🎤 Transcribing your speech...");
        const sttResult = await speechToText(audioBlob);

        if (sttResult.error) {
          setError(sttResult.error);
          setIsProcessing(false);
          return;
        }

        if (!sttResult.text.trim()) {
          setError("Could not understand the audio. Please try again.");
          setIsProcessing(false);
          return;
        }

        const userLang = selectedLang === "auto" ? sttResult.language : selectedLang;

        // Add user message
        const userMessage = {
          role: "user",
          content: sttResult.text,
          language: userLang,
          timestamp: new Date().toISOString(),
        };
        setMessages((prev) => [...prev, userMessage]);

        // Stage 2: AI Response
        setProcessingStage("🤔 Thinking...");
        const chatResult = await sendChatMessage(
          sttResult.text,
          userLang,
          messages.map((m) => ({ role: m.role, content: m.content }))
        );

        // Add AI message
        const aiMessage = {
          role: "assistant",
          content: chatResult.response,
          language: chatResult.language,
          timestamp: new Date().toISOString(),
        };
        setMessages((prev) => [...prev, aiMessage]);

        // Stage 3: Text-to-Speech
        setProcessingStage("🔊 Generating voice...");
        try {
          const audioBlob = await textToSpeech(chatResult.response, chatResult.language);
          const audioUrl = URL.createObjectURL(audioBlob);
          if (audioRef.current) {
            audioRef.current.src = audioUrl;
            audioRef.current.play().catch(() => {});
          }
        } catch (ttsErr) {
          console.warn("TTS unavailable:", ttsErr.message);
          // TTS failure is non-critical — text response is still shown
        }

      } catch (err) {
        setError(err.message || "Something went wrong. Please try again.");
      } finally {
        setIsProcessing(false);
        setProcessingStage("");
      }
    } else {
      // Start recording
      setError(null);
      await startRecording();
    }
  }, [isRecording, stopRecording, startRecording, selectedLang, messages]);

  /**
   * Handle text input submission
   */
  const handleTextSubmit = useCallback(async (e) => {
    e.preventDefault();
    if (!textInput.trim() || isProcessing) return;

    const message = textInput.trim();
    setTextInput("");
    setIsProcessing(true);
    setError(null);

    try {
      const userMessage = {
        role: "user",
        content: message,
        language: selectedLang === "auto" ? "en" : selectedLang,
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, userMessage]);

      setProcessingStage("🤔 Thinking...");
      const chatResult = await sendChatMessage(
        message,
        selectedLang,
        messages.map((m) => ({ role: m.role, content: m.content }))
      );

      const aiMessage = {
        role: "assistant",
        content: chatResult.response,
        language: chatResult.language,
        timestamp: new Date().toISOString(),
      };
      setMessages((prev) => [...prev, aiMessage]);

      // Try TTS
      try {
        setProcessingStage("🔊 Generating voice...");
        const audioBlob = await textToSpeech(chatResult.response, chatResult.language);
        const audioUrl = URL.createObjectURL(audioBlob);
        if (audioRef.current) {
          audioRef.current.src = audioUrl;
          audioRef.current.play().catch(() => {});
        }
      } catch (ttsErr) {
        console.warn("TTS unavailable:", ttsErr.message);
      }

    } catch (err) {
      setError(err.message || "Something went wrong. Please try again.");
    } finally {
      setIsProcessing(false);
      setProcessingStage("");
    }
  }, [textInput, isProcessing, selectedLang, messages]);

  /**
   * Handle example question click
   */
  const handleExampleClick = (question) => {
    setTextInput(selectedLang === "kn" ? question.kn : question.en);
  };

  return (
    <div className="flex flex-col h-full max-h-[800px]" id="voice-assistant">
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-orange-200/30 dark:border-orange-800/20">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-orange-500 to-amber-500 flex items-center justify-center shadow-lg shadow-orange-500/25">
            <span className="text-lg">🙏</span>
          </div>
          <div>
            <h3 className="font-semibold text-gray-900 dark:text-white text-sm">AI Temple Guide</h3>
            <p className="text-xs text-green-600 dark:text-green-400">● Online</p>
          </div>
        </div>

        {/* Language Selector */}
        <div className="flex items-center gap-1 p-1 rounded-xl bg-gray-100 dark:bg-gray-800/50">
          {[
            { value: "auto", label: "Auto" },
            { value: "en", label: "EN" },
            { value: "kn", label: "ಕನ್ನಡ" },
          ].map((lang) => (
            <button
              key={lang.value}
              onClick={() => setSelectedLang(lang.value)}
              className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
                selectedLang === lang.value
                  ? "bg-orange-500 text-white shadow-sm"
                  : "text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200"
              }`}
              id={`lang-${lang.value}`}
            >
              {lang.label}
            </button>
          ))}
        </div>
      </div>

      {/* Messages Area */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 min-h-[300px]">
        {/* Welcome Message */}
        {messages.length === 0 && (
          <div className="text-center py-8">
            <div className="text-5xl mb-4">🛕</div>
            <h3 className="text-lg font-semibold text-gray-900 dark:text-white mb-2">
              Namaskara! ನಮಸ್ಕಾರ! 🙏
            </h3>
            <p className="text-sm text-gray-500 dark:text-gray-400 max-w-sm mx-auto mb-6">
              I am your AI temple guide. Ask me about pooja timings, festivals, darshan, and more in English or Kannada.
            </p>

            {/* Example Questions */}
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-2 max-w-lg mx-auto">
              {EXAMPLE_QUESTIONS.slice(0, 6).map((q, i) => (
                <button
                  key={i}
                  onClick={() => handleExampleClick(q)}
                  className="text-left p-3 rounded-xl bg-orange-50 dark:bg-orange-950/20 border border-orange-200/30 dark:border-orange-800/20 hover:bg-orange-100 dark:hover:bg-orange-950/40 transition-colors text-sm"
                  id={`example-q-${i}`}
                >
                  <span className="text-gray-700 dark:text-gray-300">{q.en}</span>
                  <br />
                  <span className="text-xs text-orange-600 dark:text-orange-400">{q.kn}</span>
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Chat Messages */}
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
          >
            <div
              className={`max-w-[80%] p-4 rounded-2xl ${
                msg.role === "user"
                  ? "bg-gradient-to-br from-orange-500 to-amber-500 text-white rounded-tr-sm"
                  : "bg-gray-100 dark:bg-gray-800/50 text-gray-900 dark:text-white rounded-tl-sm border border-gray-200/50 dark:border-gray-700/30"
              }`}
            >
              {msg.role === "assistant" && (
                <div className="flex items-center gap-1.5 mb-2">
                  <span className="text-sm">🛕</span>
                  <span className="text-xs font-medium text-orange-600 dark:text-orange-400">AI Guide</span>
                  <span className="text-xs text-gray-400 ml-auto">
                    {msg.language === "kn" ? "ಕನ್ನಡ" : "English"}
                  </span>
                </div>
              )}
              <p className="text-sm leading-relaxed whitespace-pre-wrap">{msg.content}</p>
              <p className={`text-[10px] mt-2 ${msg.role === "user" ? "text-white/50" : "text-gray-400"}`}>
                {new Date(msg.timestamp).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}
              </p>
            </div>
          </div>
        ))}

        {/* Processing Indicator */}
        {isProcessing && (
          <div className="flex justify-start">
            <div className="p-4 rounded-2xl rounded-tl-sm bg-gray-100 dark:bg-gray-800/50 border border-gray-200/50 dark:border-gray-700/30">
              <div className="flex items-center gap-2">
                <div className="flex gap-1">
                  <span className="w-2 h-2 bg-orange-500 rounded-full animate-bounce" style={{ animationDelay: "0ms" }} />
                  <span className="w-2 h-2 bg-orange-500 rounded-full animate-bounce" style={{ animationDelay: "150ms" }} />
                  <span className="w-2 h-2 bg-orange-500 rounded-full animate-bounce" style={{ animationDelay: "300ms" }} />
                </div>
                <span className="text-xs text-gray-500 dark:text-gray-400">{processingStage}</span>
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Error Display */}
      {error && (
        <div className="mx-4 mb-2 p-3 rounded-xl bg-red-500/10 border border-red-500/20 text-red-700 dark:text-red-400 text-sm flex items-center gap-2">
          <span>⚠️</span>
          <span className="flex-1">{error}</span>
          <button onClick={() => setError(null)} className="opacity-50 hover:opacity-100">✕</button>
        </div>
      )}

      {/* Waveform Visualization (during recording) */}
      {isRecording && (
        <div className="mx-4 mb-2 p-3 rounded-xl bg-orange-500/10 border border-orange-500/20">
          <div className="flex items-center gap-2 mb-2">
            <span className="w-2 h-2 bg-red-500 rounded-full animate-pulse" />
            <span className="text-xs font-medium text-red-600 dark:text-red-400">Recording... {duration}s</span>
          </div>
          <div className="flex items-end gap-[2px] h-12">
            {waveformData.length > 0
              ? waveformData.map((v, i) => (
                  <div
                    key={i}
                    className="flex-1 bg-gradient-to-t from-orange-500 to-amber-400 rounded-full transition-all duration-75"
                    style={{ height: `${Math.max(4, v * 100)}%` }}
                  />
                ))
              : Array.from({ length: 32 }).map((_, i) => (
                  <div
                    key={i}
                    className="flex-1 bg-orange-300/30 dark:bg-orange-700/30 rounded-full animate-pulse"
                    style={{ height: `${20 + Math.random() * 30}%`, animationDelay: `${i * 50}ms` }}
                  />
                ))}
          </div>
        </div>
      )}

      {/* Input Area */}
      <div className="p-4 border-t border-orange-200/30 dark:border-orange-800/20">
        <div className="flex items-center gap-3">
          {/* Text Input */}
          <form onSubmit={handleTextSubmit} className="flex-1 flex gap-2">
            <input
              type="text"
              value={textInput}
              onChange={(e) => setTextInput(e.target.value)}
              placeholder={selectedLang === "kn" ? "ನಿಮ್ಮ ಪ್ರಶ್ನೆ ಬರೆಯಿರಿ..." : "Type your question..."}
              className="flex-1 px-4 py-3 rounded-xl bg-gray-100 dark:bg-gray-800/50 border border-gray-200/50 dark:border-gray-700/30 text-gray-900 dark:text-white text-sm placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-orange-500/30 focus:border-orange-500/50 transition-all"
              disabled={isProcessing || isRecording}
              id="chat-text-input"
            />
            <button
              type="submit"
              disabled={!textInput.trim() || isProcessing || isRecording}
              className="px-4 py-3 rounded-xl bg-orange-500 text-white font-medium text-sm hover:bg-orange-600 disabled:opacity-40 disabled:cursor-not-allowed transition-colors shadow-lg shadow-orange-500/20"
              id="chat-send-button"
            >
              Send
            </button>
          </form>

          {/* Microphone Button */}
          <button
            onClick={handleVoiceInteraction}
            disabled={isProcessing}
            className={`relative w-14 h-14 rounded-2xl flex items-center justify-center transition-all duration-300 shadow-xl ${
              isRecording
                ? "bg-red-500 shadow-red-500/40 scale-110 animate-pulse"
                : isProcessing
                ? "bg-gray-400 cursor-not-allowed"
                : "bg-gradient-to-br from-orange-500 to-amber-500 shadow-orange-500/30 hover:shadow-orange-500/50 hover:scale-105"
            }`}
            aria-label={isRecording ? "Stop recording" : "Start recording"}
            id="voice-record-button"
          >
            {isRecording ? (
              <svg className="w-6 h-6 text-white" fill="currentColor" viewBox="0 0 24 24">
                <rect x="6" y="6" width="12" height="12" rx="2" />
              </svg>
            ) : (
              <svg className="w-6 h-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"
                />
              </svg>
            )}

            {/* Pulse rings when recording */}
            {isRecording && (
              <>
                <span className="absolute inset-0 rounded-2xl bg-red-500/50 animate-ping" />
                <span className="absolute -inset-2 rounded-3xl border-2 border-red-500/30 animate-pulse" />
              </>
            )}
          </button>
        </div>

        <p className="text-center text-[10px] text-gray-400 mt-2">
          Press mic to speak in English or ಕನ್ನಡ • AI-powered responses
        </p>
      </div>

      {/* Hidden audio element for TTS playback */}
      <audio ref={audioRef} className="hidden" />
    </div>
  );
}
