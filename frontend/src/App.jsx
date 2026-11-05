
import { useEffect, useState } from "react";
import ChatComposer from "./components/ChatComposer";
import ChatWindow from "./components/ChatWindow";
import Header from "./components/Header";
import Sidebar from "./components/Sidebar";
import WelcomeScreen from "./components/WelcomeScreen";
import WellnessPanel from "./components/WellnessPanel";

import "./App.css";

// Backend API configuration
const API_BASE_URL = (
  import.meta.env.VITE_API_BASE_URL ||
  "http://localhost:8000"
).replace(/\/+$/, "");

const API_URL = `${API_BASE_URL}/chat`;

// Multilingual API error messages
const ERROR_MESSAGES = {
  en:
    "MindBridge AI is unable to respond right now. " +
    "Please try again. If you are in immediate danger, " +
    "contact local emergency services or visit the nearest emergency department.",

  roman_ur:
    "MindBridge AI filhaal jawab nahi de pa raha. " +
    "Barah-e-karam dobara koshish karein. " +
    "Agar aap ko foran khatra hai, to local emergency services se rabta karein " +
    "ya qareebi hospital ke emergency department mein jayein.",

  ur:
    "مائنڈ برج اے آئی فی الحال جواب نہیں دے پا رہا۔ " +
    "براہِ کرم دوبارہ کوشش کریں۔ " +
    "اگر آپ کو فوری خطرہ ہے تو مقامی ایمرجنسی سروسز سے رابطہ کریں " +
    "یا قریبی ہسپتال کے شعبۂ ایمرجنسی میں جائیں۔",

  es:
    "MindBridge AI no puede responder en este momento. " +
    "Inténtalo de nuevo. Si estás en peligro inmediato, " +
    "contacta con los servicios de emergencia locales " +
    "o acude al servicio de urgencias más cercano.",

  de:
    "MindBridge AI kann derzeit nicht antworten. " +
    "Bitte versuche es erneut. Wenn du in unmittelbarer Gefahr bist, " +
    "kontaktiere den örtlichen Notdienst oder suche " +
    "die nächste Notaufnahme auf.",
};

export default function App() {
  // Application state
  const [messages, setMessages] = useState([]);
 const [sessionId, setSessionId] = useState(
  () => sessionStorage.getItem("mindbridge_active_session")
);

useEffect(() => {
  if (sessionId) {
    sessionStorage.setItem(
      "mindbridge_active_session",
      sessionId
    );
  } else {
    sessionStorage.removeItem(
      "mindbridge_active_session"
    );
  }
}, [sessionId]);
  const [input, setInput] = useState("");
  const [language, setLanguage] = useState("auto");
  const [loading, setLoading] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [darkMode, setDarkMode] = useState(false);

  const [page, setPage] = useState('chat');
  const [moodEntries, setMoodEntries] = useState([]);
  const [chatArchive, setChatArchive] = useState([]);
  const [archiveId, setArchiveId] = useState(null);
  const isChatActive = messages.length > 0;
  
  // Restore chat history after browser refresh
  useEffect(() => {
    const savedSessionId = sessionStorage.getItem(
      "mindbridge_active_session"
    );

    if (!savedSessionId) return;

    const controller = new AbortController();

    async function restoreChat() {
      try {
        const response = await fetch(
          `${API_URL}/history/${encodeURIComponent(savedSessionId)}`,
          {
            method: "GET",
            credentials: "include",
            signal: controller.signal,
          }
        );

        if (!response.ok) {
          if (response.status === 403 || response.status === 404) {
            sessionStorage.removeItem(
              "mindbridge_active_session"
            );
            setSessionId(null);
          }
          return;
        }

        const data = await response.json();

        if (
          data.session_id === savedSessionId &&
          Array.isArray(data.messages)
        ) {
          setMessages(data.messages);
        }
      } catch (error) {
        if (error.name !== "AbortError") {
          console.error("Chat restoration failed:", error);
        }
      }
    }

    restoreChat();

    return () => controller.abort();
  }, []);

 
  // Send message to backend
  async function sendMessage(value = input) {
    const text = String(value ?? "").trim();

    if (!text || loading) {
      return;
    }

    setInput("");
    setSidebarOpen(false);
    setPage("chat");

    // Add user message
    setMessages((previous) => [
      ...previous,
      {
        role: "user",
        content: text,
        timestamp: new Date().toISOString(),
      },
    ]);

    setLoading(true);

    try {
      // Build multilingual request payload
      const payload = {
        message: text,
        language_mode:
          language === "auto" ? "auto" : "manual",
      };

      if (language !== "auto") {
        payload.preferred_language = language;
      }

      if (sessionId) {
        payload.session_id = sessionId;
      }

      // Send request
      const response = await fetch(API_URL, {
        method: "POST",
        credentials: "include",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        throw new Error(
          `API request failed: ${response.status}`
        );
      }

      const data = await response.json();

      // Validate API response
      if (
        typeof data?.response !== "string" ||
        !data.response.trim() ||
        typeof data?.session_id !== "string" ||
        !data.session_id.trim()
      ) {
        throw new Error("Invalid API response");
      }

      // Save session ID
      setSessionId(data.session_id);

      // Add AI response
      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content: data.response,
          timestamp: new Date().toISOString(),
        },
      ]);
    } catch (error) {
      console.error("MindBridge API error:", error);

      // Display error in selected language
      setMessages((previous) => [
        ...previous,
        {
          role: "system",
          content:
            ERROR_MESSAGES[language] ||
            ERROR_MESSAGES.en,
          timestamp: new Date().toISOString(),
        },
      ]);
    } finally {
      setLoading(false);
    }
  }

  // Start a new conversation
  function newConversation() {
    if (loading) {
      return;
    }

    if (messages.length) {
      setChatArchive(prev => [{id:crypto.randomUUID(),title:(messages.find(m=>m.role==='user')?.content||'Conversation').slice(0,52),messages:[...messages],date:new Date().toISOString()},...prev]);
    }
    setMessages([]);
    setSessionId(null);
    setArchiveId(null);
    setPage('chat');
    setInput('');
    setSidebarOpen(false);
  }
  function openArchived(chat){
    if(loading)return;
    setArchiveId(chat.id);
    setPage('archive');
    setSidebarOpen(false);
  }
  function deleteArchived(id){setChatArchive(prev=>prev.filter(c=>c.id!==id));if(archiveId===id){setArchiveId(null);setPage('chat')}}
  function openPage(next){if(loading)return;setPage(next);setSidebarOpen(false)}

  return (
    <div
      className={`app-shell ${darkMode ? "dark" : ""}`}
    >
      <Sidebar
        isOpen={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
        onNewConversation={newConversation}
        isLoading={loading}
        language={language}
        page={page}
        chats={chatArchive}
        onOpenChat={openArchived}
        onDeleteChat={deleteArchived}
        onNavigate={openPage}
      />

      <main className="mb-main">
        <Header
          onOpenSidebar={() => setSidebarOpen(true)}
          language={language}
          onLanguageChange={setLanguage}
          darkMode={darkMode}
          onToggleTheme={() =>
            setDarkMode((previous) => !previous)
          }
          isChatActive={isChatActive}
        />

        <div className="mb-content">
          {page === 'mood' || page === 'toolkit' ? (
            <WellnessPanel mode={page} language={language} entries={moodEntries} onSave={entry=>setMoodEntries(prev=>[entry,...prev])}/>
          ) : page === 'archive' ? (
            <div className="mb-archive-view"><div className="mb-archive-header"><h2>{chatArchive.find(c=>c.id===archiveId)?.title}</h2><p>Read-only chat history · Current browser tab only</p></div><ChatWindow messages={chatArchive.find(c=>c.id===archiveId)?.messages||[]} loading={false} language={language}/></div>
          ) : isChatActive ? (
            <ChatWindow
              messages={messages}
              loading={loading}
              language={language}
            />
          ) : (
            <div className="mb-welcome-scroll">
              <WelcomeScreen
                onStartConversation={sendMessage}
                disabled={loading}
                language={language}
              />
            </div>
          )}

          {page === 'chat' && <ChatComposer
            value={input}
            onChange={setInput}
            onSend={() => sendMessage()}
            loading={loading}
            language={language}
          />}
        </div>
      </main>
    </div>
  );
}
