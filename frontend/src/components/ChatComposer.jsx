
import { ArrowUp02Icon } from "@hugeicons/core-free-icons";
import { HugeiconsIcon } from "@hugeicons/react";
import { useEffect, useRef } from "react";
import "./ChatComposer.css";

const MAX_MESSAGE_LENGTH = 2000;

const TEXT = {
  en: {
    placeholder: "Share what's on your mind...",
    messageLabel: "Your message",
    send: "Send message",
    disclaimer:
      "MindBridge AI supports wellbeing but does not provide medical diagnosis or replace professional care.",
  },
  roman_ur: {
    placeholder: "Aap ke dil mein kya chal raha hai?",
    messageLabel: "Aap ka message",
    send: "Message bhejein",
    disclaimer:
      "MindBridge AI jazbati sehat mein madad karta hai, lekin medical diagnosis ya professional care ka badal nahi hai.",
  },
  ur: {
    placeholder: "آپ کے دل میں کیا چل رہا ہے؟",
    messageLabel: "آپ کا پیغام",
    send: "پیغام بھیجیں",
    disclaimer:
      "مائنڈ برج اے آئی ذہنی اور جذباتی صحت میں معاونت فراہم کرتا ہے، لیکن طبی تشخیص یا پیشہ ورانہ علاج کا متبادل نہیں ہے۔",
  },
    es: {
    placeholder: "Comparte lo que tienes en mente...",
    messageLabel: "Tu mensaje",
    send: "Enviar mensaje",
    disclaimer:
      "MindBridge AI ofrece apoyo para el bienestar emocional, pero no proporciona diagnósticos médicos ni sustituye la atención profesional.",
  },

  de: {
    placeholder: "Teile, was dich beschäftigt...",
    messageLabel: "Deine Nachricht",
    send: "Nachricht senden",
    disclaimer:
      "MindBridge AI unterstützt das psychische Wohlbefinden, stellt jedoch keine medizinischen Diagnosen und ersetzt keine professionelle Behandlung.",
  },
};

export default function ChatComposer({
  value,
  onChange,
  onSend,
  loading = false,
  language = "auto",
}) {
  const textareaRef = useRef(null);

  const currentLanguage =
    language === "auto" ? "en" : language;

  const labels = TEXT[currentLanguage] || TEXT.en;

  const message = String(value ?? "");
  const remaining = MAX_MESSAGE_LENGTH - message.length;

  useEffect(() => {
    const textarea = textareaRef.current;

    if (!textarea) return;

    textarea.style.height = "auto";
    textarea.style.height = `${
      Math.min(textarea.scrollHeight, 160)
    }px`;
  }, [message]);

  function handleSubmit(event) {
    event.preventDefault();

    if (
      !loading &&
      message.trim() &&
      message.length <= MAX_MESSAGE_LENGTH
    ) {
      onSend();
    }
  }

  function handleKeyDown(event) {
    if (
      event.key === "Enter" &&
      !event.shiftKey &&
      !event.nativeEvent.isComposing
    ) {
      event.preventDefault();

      if (
        !loading &&
        message.trim() &&
        message.length <= MAX_MESSAGE_LENGTH
      ) {
        onSend();
      }
    }
  }

  return (
    <div className="mb-composer-area">
      <form
        className="mb-composer"
        onSubmit={handleSubmit}
      >
        <textarea
          ref={textareaRef}
          value={message}
          onChange={(event) =>
            onChange(event.target.value)
          }
          onKeyDown={handleKeyDown}
          placeholder={labels.placeholder}
          aria-label={labels.messageLabel}
          rows={1}
          maxLength={MAX_MESSAGE_LENGTH}
          disabled={loading}
          dir={
            currentLanguage === "ur"
              ? "rtl"
              : "auto"
          }
          lang={
            currentLanguage === "roman_ur"
              ? "ur-Latn"
              : currentLanguage
          }
                  />

        <button
          type="submit"
          className="mb-composer-send"
          disabled={
            loading ||
            !message.trim() ||
            message.length > MAX_MESSAGE_LENGTH
          }
          aria-label={labels.send}
          title={labels.send}
        >
          {loading ? (
            <span className="mb-composer-spinner" />
          ) : (
            <HugeiconsIcon
              icon={ArrowUp02Icon}
              size={21}
            />
          )}
        </button>
      </form>

      <p
        className="mb-composer-disclaimer"
        dir={currentLanguage === "ur" ? "rtl" : "auto"}
      >
        {labels.disclaimer}
      </p>

      <p
        style={{
          textAlign: "right",
          fontSize: "11px",
          opacity: 0.65,
          marginTop: "4px",
        }}
        aria-live="polite"
      >
        {remaining} / {MAX_MESSAGE_LENGTH}
      </p>
    </div>
  );
}
