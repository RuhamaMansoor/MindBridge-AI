
import {
  Alert02Icon,
  Brain02Icon,
  CheckmarkCircle02Icon,
  Copy01Icon,
} from "@hugeicons/core-free-icons";

import { HugeiconsIcon } from "@hugeicons/react";
import { motion, useReducedMotion } from "motion/react";
import { useEffect, useRef, useState } from "react";
import "./ChatWindow.css";

const TRANSLATIONS = {
  en: {
    you: "You",
    system: "System",
    copied: "Copied",
    copyAI: "Copy AI response",
    copyResponse: "Copy response",
    responding: "MindBridge is responding...",
    conversationMessages: "Conversation messages",
  },

  roman_ur: {
    you: "Aap",
    system: "System",
    copied: "Copy ho gaya",
    copyAI: "AI ka jawab copy karein",
    copyResponse: "Jawab copy karein",
    responding: "MindBridge jawab de raha hai...",
    conversationMessages: "Guftagu ke paighamaat",
  },

  ur: {
    you: "آپ",
    system: "سسٹم",
    copied: "کاپی ہو گیا",
    copyAI: "اے آئی کا جواب کاپی کریں",
    copyResponse: "جواب کاپی کریں",
    responding: "مائنڈ برج جواب دے رہا ہے...",
    conversationMessages: "گفتگو کے پیغامات",
  },

  es: {
    you: "Tú",
    system: "Sistema",
    copied: "Copiado",
    copyAI: "Copiar respuesta de IA",
    copyResponse: "Copiar respuesta",
    responding: "MindBridge está respondiendo...",
    conversationMessages: "Mensajes de la conversación",
  },

  de: {
    you: "Du",
    system: "System",
    copied: "Kopiert",
    copyAI: "KI-Antwort kopieren",
    copyResponse: "Antwort kopieren",
    responding: "MindBridge antwortet...",
    conversationMessages: "Gesprächsnachrichten",
  },
};

function Icon({ icon, size = 19 }) {
  return <HugeiconsIcon icon={icon} size={size} />;
}

function isUrdu(text = "") {
  return /[\u0600-\u06FF]/.test(text);
}

function MessageBubble({
  message,
  reducedMotion,
  labels,
  language,
}) {
  const [copied, setCopied] = useState(false);

  const isUser = message.role === "user";
  const isError = message.role === "system";

  async function copyMessage() {
    try {
      await navigator.clipboard.writeText(message.content);
      setCopied(true);
      window.setTimeout(() => setCopied(false), 1800);
    } catch {
      setCopied(false);
    }
  }

  return (
    <motion.article
      className={`mb-chat-message ${
        isUser
          ? "is-user"
          : isError
            ? "is-error"
            : "is-assistant"
      }`}
      initial={
        reducedMotion
          ? false
          : { opacity: 0, y: 10 }
      }
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.25 }}
    >
      {!isUser && (
        <div
          className="mb-chat-avatar"
          aria-hidden="true"
        >
          <Icon
            icon={
              isError
                ? Alert02Icon
                : Brain02Icon
            }
          />
        </div>
      )}

      <div className="mb-chat-message-body">
        <div
          className={`mb-chat-bubble ${
            isUrdu(message.content)
              ? "is-urdu"
              : ""
          }`}
          dir="auto"
        >
          {message.content}
        </div>

        <div className="mb-chat-message-meta">
          <span>
            {isUser
              ? labels.you
              : isError
                ? labels.system
                : "MindBridge AI"}
          </span>

          {message.timestamp && (
            <time dateTime={message.timestamp}>
              {new Date(
                message.timestamp
              ).toLocaleTimeString(
                language === "auto"
                  ? undefined
                  : language === "roman_ur"
                    ? "ur-Latn"
                    : language,
                {
                  hour: "2-digit",
                  minute: "2-digit",
                }
              )}
            </time>
          )}

          {!isUser && !isError && (
            <button
              type="button"
              className="mb-chat-copy"
              onClick={copyMessage}
              aria-label={
                copied
                  ? labels.copied
                  : labels.copyAI
              }
              title={
                copied
                  ? labels.copied
                  : labels.copyResponse
              }
            >
              <Icon
                icon={
                  copied
                    ? CheckmarkCircle02Icon
                    : Copy01Icon
                }
                size={15}
              />
            </button>
          )}
        </div>
      </div>
    </motion.article>
  );
}

export default function ChatWindow({
  messages = [],
  loading = false,
  language = "auto",
}) {
  const bottomRef = useRef(null);
  const reducedMotion = useReducedMotion();

  const currentLanguage =
    language === "auto"
      ? "en"
      : language;

  const labels =
    TRANSLATIONS[currentLanguage] ||
    TRANSLATIONS.en;

  const languageTag =
    currentLanguage === "roman_ur"
      ? "ur-Latn"
      : currentLanguage;

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: reducedMotion
        ? "auto"
        : "smooth",
      block: "end",
    });
  }, [messages, loading, reducedMotion]);

  return (
    <section
      className="mb-chat-window"
      aria-label={labels.conversationMessages}
      lang={languageTag}
    >
      <div className="mb-chat-list">
        {messages.map((message, index) => (
          <MessageBubble
            key={message.id ?? index}
            message={message}
            reducedMotion={reducedMotion}
            labels={labels}
            language={language}
          />
        ))}

        {loading && (
          <div className="mb-chat-message is-assistant">
            <div
              className="mb-chat-avatar"
              aria-hidden="true"
            >
              <Icon icon={Brain02Icon} />
            </div>

            <div
              className="mb-chat-typing"
              role="status"
            >
              <span className="mb-typing-dot" />
              <span className="mb-typing-dot" />
              <span className="mb-typing-dot" />

              <span className="mb-typing-label">
                {labels.responding}
              </span>
            </div>
          </div>
        )}

        <div ref={bottomRef} />
      </div>
    </section>
  );
}
