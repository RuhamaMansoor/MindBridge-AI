
import {
  ArrowUp02Icon,
  Brain02Icon,
  HeartAddIcon,
  Message01Icon,
  Sun01Icon,
} from "@hugeicons/core-free-icons";

import { HugeiconsIcon } from "@hugeicons/react";
import { motion, useReducedMotion } from "motion/react";
import "./WelcomeScreen.css";

const TRANSLATIONS = {
  en: {
    ariaLabel: "Welcome to MindBridge AI",
    kicker: "A MOMENT FOR YOURSELF",
    heading: "A little space for",
    headingEmphasis: "your mind.",
    introduction:
      "You don't need to have everything figured out. " +
      "Take your time, share what's on your mind, " +
      "and explore your next step.",
    sectionTitle: "Where would you like to begin?",
    sectionDescription:
      "Choose a starting point or write your own message.",
    footer:
      "Your feelings matter. There's no perfect way to begin.",
    prompts: [
      {
        title: "Emotional Support",
        description: "Share what's weighing on you",
        prompt: "I've been feeling overwhelmed lately.",
      },
      {
        title: "Find Your Calm",
        description: "Explore ways to feel grounded",
        prompt: "Can you help me feel calmer right now?",
      },
      {
        title: "Daily Reflection",
        description: "Make sense of your day",
        prompt: "I'd like to reflect on how my day went.",
      },
      {
        title: "Just Talk",
        description: "Start wherever you feel comfortable",
        prompt: "I need someone to talk to.",
      },
    ],
  },

  roman_ur: {
    ariaLabel: "MindBridge AI mein khush aamdeed",
    kicker: "KHUD KE LIYE EK LAMHA",
    heading: "Aap ke zehan ke liye",
    headingEmphasis: "ek pur-sukoon jagah.",
    introduction:
      "Zaroori nahi ke aap ke paas har baat ka jawab ho. " +
      "Apna waqt lein, dil ki baat share karein aur " +
      "apne aglay qadam ke baare mein sochein.",
    sectionTitle: "Aap kahan se shuru karna chahenge?",
    sectionDescription:
      "Koi topic chunein ya apna message likhein.",
    footer:
      "Aap ke jazbaat ahmiyat rakhte hain. " +
      "Baat shuru karne ka koi ek sahi tareeqa nahi.",
    prompts: [
      {
        title: "Jazbati Sahara",
        description: "Jo baat pareshan kar rahi hai, share karein",
        prompt:
          "Main kuch arsay se bohat zyada pressure mehsoos kar raha hoon.",
      },
      {
        title: "Sukoon Talash Karein",
        description: "Khud ko pur-sukoon mehsoos karne ke tareeqay",
        prompt:
          "Kya aap abhi mujhe pur-sukoon hone mein madad kar sakte hain?",
      },
      {
        title: "Rozana Ghor-o-Fikr",
        description: "Apne din ke baare mein sochein",
        prompt:
          "Main aaj ke din ke baare mein baat karna chahta hoon.",
      },
      {
        title: "Bas Baat Karein",
        description: "Jahan se dil chahe, baat shuru karein",
        prompt:
          "Mujhe kisi se baat karni hai.",
      },
    ],
  },

  ur: {
    ariaLabel: "مائنڈ برج اے آئی میں خوش آمدید",
    kicker: "اپنے لیے ایک لمحہ",
    heading: "آپ کے ذہن کے لیے",
    headingEmphasis: "ایک پُرسکون جگہ۔",
    introduction:
      "ضروری نہیں کہ آپ کے پاس ہر بات کا جواب ہو۔ " +
      "اطمینان سے وقت لیں، اپنے دل کی بات بتائیں اور " +
      "اپنے اگلے قدم کے بارے میں سوچیں۔",
    sectionTitle: "آپ کہاں سے شروع کرنا چاہیں گے؟",
    sectionDescription:
      "کوئی موضوع منتخب کریں یا اپنا پیغام لکھیں۔",
    footer:
      "آپ کے جذبات اہم ہیں۔ بات شروع کرنے کا کوئی ایک صحیح طریقہ نہیں۔",
    prompts: [
      {
        title: "جذباتی مدد",
        description: "جو بات پریشان کر رہی ہے، وہ بتائیں",
        prompt:
          "میں کچھ عرصے سے بہت زیادہ دباؤ محسوس کر رہا ہوں۔",
      },
      {
        title: "سکون تلاش کریں",
        description: "خود کو پُرسکون محسوس کرنے کے طریقے",
        prompt:
          "کیا آپ ابھی مجھے پُرسکون ہونے میں مدد کر سکتے ہیں؟",
      },
      {
        title: "روزانہ غور و فکر",
        description: "اپنے دن کے بارے میں سوچیں",
        prompt:
          "میں آج کے دن کے بارے میں بات کرنا چاہتا ہوں۔",
      },
      {
        title: "بس بات کریں",
        description: "جہاں سے چاہیں گفتگو شروع کریں",
        prompt:
          "مجھے کسی سے بات کرنی ہے۔",
      },
    ],
  },
  es: {
  ariaLabel: "Bienvenido a MindBridge AI",
  kicker: "UN MOMENTO PARA TI",
  heading: "Un pequeño espacio para",
  headingEmphasis: "tu mente.",
  introduction:
    "No necesitas tener todas las respuestas. " +
    "Tómate tu tiempo, comparte lo que tienes en mente " +
    "y descubre cuál podría ser tu próximo paso.",
  sectionTitle: "¿Por dónde te gustaría empezar?",
  sectionDescription:
    "Elige un tema o escribe tu propio mensaje.",
  footer:
    "Tus sentimientos importan. No hay una forma perfecta de empezar.",
  prompts: [
    {
      title: "Apoyo emocional",
      description: "Comparte lo que te preocupa",
      prompt: "Últimamente me siento muy abrumado.",
    },
    {
      title: "Encuentra la calma",
      description: "Descubre formas de sentirte más tranquilo",
      prompt: "¿Puedes ayudarme a sentirme más tranquilo ahora?",
    },
    {
      title: "Reflexión diaria",
      description: "Reflexiona sobre tu día",
      prompt: "Me gustaría reflexionar sobre cómo fue mi día.",
    },
    {
      title: "Solo conversar",
      description: "Empieza por donde te sientas cómodo",
      prompt: "Necesito hablar con alguien.",
    },
  ],
},

de: {
  ariaLabel: "Willkommen bei MindBridge AI",
  kicker: "EIN MOMENT FÜR DICH",
  heading: "Ein kleiner Raum für",
  headingEmphasis: "deine Gedanken.",
  introduction:
    "Du musst nicht auf alles eine Antwort haben. " +
    "Nimm dir Zeit, teile deine Gedanken und " +
    "finde heraus, was dein nächster Schritt sein könnte.",
  sectionTitle: "Womit möchtest du beginnen?",
  sectionDescription:
    "Wähle ein Thema oder schreibe deine eigene Nachricht.",
  footer:
    "Deine Gefühle sind wichtig. Es gibt keinen perfekten Anfang.",
  prompts: [
    {
      title: "Emotionale Unterstützung",
      description: "Teile, was dich belastet",
      prompt: "Ich fühle mich in letzter Zeit überfordert.",
    },
    {
      title: "Ruhe finden",
      description: "Entdecke Wege, zur Ruhe zu kommen",
      prompt: "Kannst du mir helfen, mich jetzt zu beruhigen?",
    },
    {
      title: "Tägliche Reflexion",
      description: "Denke über deinen Tag nach",
      prompt: "Ich möchte darüber nachdenken, wie mein Tag war.",
    },
    {
      title: "Einfach reden",
      description: "Beginne dort, wo du dich wohlfühlst",
      prompt: "Ich brauche jemanden zum Reden.",
    },
  ],
},
};

const PROMPT_ICONS = [
  HeartAddIcon,
  Sun01Icon,
  Brain02Icon,
  Message01Icon,
];

function Icon({ icon, size = 22 }) {
  return <HugeiconsIcon icon={icon} size={size} />;
}

export default function WelcomeScreen({
  onStartConversation,
  disabled = false,
  language = "auto",
}) {
  const reducedMotion = useReducedMotion();

  // Auto detection is handled by the backend.
  // English is the default interface language.
  const uiLanguage =
    language === "auto" ? "en" : language;

  const t = TRANSLATIONS[uiLanguage] || TRANSLATIONS.en;

  const isUrdu = uiLanguage === "ur";

  const languageTag = isUrdu
    ? "ur"
    : uiLanguage === "roman_ur"
      ? "ur-Latn"
      :  uiLanguage;

  return (
    <motion.section
      className="mb-welcome"
      aria-label={t.ariaLabel}
      lang={languageTag}
      dir={isUrdu ? "rtl" : "ltr"}
      initial={
        reducedMotion
          ? false
          : { opacity: 0, y: 14 }
      }
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
    >
      <div className="mb-welcome-intro">
        <span className="mb-welcome-kicker">
          <Icon icon={Sun01Icon} size={17} />
          {t.kicker}
        </span>

        <h2>
          {t.heading} <em>{t.headingEmphasis}</em>
        </h2>

        <p>{t.introduction}</p>
      </div>

      <div className="mb-welcome-section-title">
        <div>
          <h3>{t.sectionTitle}</h3>
          <p>{t.sectionDescription}</p>
        </div>
      </div>

      <div className="mb-welcome-grid">
        {t.prompts.map((item, index) => (
          <motion.button
            key={index}
            type="button"
            className="mb-welcome-card"
            disabled={disabled}
            onClick={() =>
              onStartConversation(item.prompt)
            }
            initial={
              reducedMotion
                ? false
                : { opacity: 0, y: 12 }
            }
            animate={{ opacity: 1, y: 0 }}
            transition={{
              duration: 0.35,
              delay: reducedMotion
                ? 0
                : index * 0.06,
            }}
            whileHover={
              reducedMotion
                ? undefined
                : { y: -3 }
            }
          >
            <span className="mb-welcome-card-icon">
              <Icon
                icon={PROMPT_ICONS[index]}
                size={23}
              />
            </span>

            <span className="mb-welcome-card-content">
              <strong>{item.title}</strong>
              <small>{item.description}</small>
            </span>

            <span className="mb-welcome-card-arrow">
              <Icon
                icon={ArrowUp02Icon}
                size={17}
              />
            </span>
          </motion.button>
        ))}
      </div>

      <p className="mb-welcome-footer">
        {t.footer}
      </p>
    </motion.section>
  );
}
