
import {
  Globe02Icon,
  Menu01Icon,
  Moon02Icon,
  Sun01Icon,
} from "@hugeicons/core-free-icons";

import { HugeiconsIcon } from "@hugeicons/react";
import "./Header.css";

const LANGUAGES = [
  { code: "en", label: "English", enabled: true },
  { code: "ur", label: "اردو", enabled: true },
  {
    code: "roman_ur",
    label: "Roman Urdu",
    enabled: true,
  },
  {
    code: "es",
    label: "Español (Spanish)",
    enabled: true,
  },
  {
    code: "de",
    label: "Deutsch (German)",
    enabled: true,
  },
];

const TRANSLATIONS = {
  en: {
    personalSpace: "YOUR PERSONAL SPACE",
    conversation: "YOUR CONVERSATION",
    wellnessCompanion: "Wellness Companion",
    conversationTitle: "MindBridge Conversation",
    openNavigation: "Open navigation",
    conversationLanguage: "Conversation language",
    autoDetect: "Auto detect",
    comingSoon: "Coming soon",
    lightMode: "Light mode",
    darkMode: "Dark mode",
    switchToLight: "Switch to light mode",
    switchToDark: "Switch to dark mode",
  },

  roman_ur: {
    personalSpace: "AAP KI PERSONAL SPACE",
    conversation: "AAP KI GUFTAGU",
    wellnessCompanion: "Aap Ka Wellness Companion",
    conversationTitle: "MindBridge Guftagu",
    openNavigation: "Navigation kholein",
    conversationLanguage: "Guftagu ki zubaan",
    autoDetect: "Zubaan khud pehchanein",
    comingSoon: "Jald aa raha hai",
    lightMode: "Light mode",
    darkMode: "Dark mode",
    switchToLight: "Light mode par jayein",
    switchToDark: "Dark mode par jayein",
  },

  ur: {
    personalSpace: "آپ کی ذاتی جگہ",
    conversation: "آپ کی گفتگو",
    wellnessCompanion: "آپ کا فلاح و بہبود کا ساتھی",
    conversationTitle: "مائنڈ برج گفتگو",
    openNavigation: "نیویگیشن کھولیں",
    conversationLanguage: "گفتگو کی زبان",
    autoDetect: "زبان خود پہچانیں",
    comingSoon: "جلد دستیاب ہوگا",
    lightMode: "لائٹ موڈ",
    darkMode: "ڈارک موڈ",
    switchToLight: "لائٹ موڈ پر جائیں",
    switchToDark: "ڈارک موڈ پر جائیں",
  },

  es: {
  personalSpace: "TU ESPACIO PERSONAL",
  conversation: "TU CONVERSACIÓN",
  wellnessCompanion: "Tu compañero de bienestar",
  conversationTitle: "Conversación MindBridge",
  openNavigation: "Abrir navegación",
  conversationLanguage: "Idioma de la conversación",
  autoDetect: "Detectar automáticamente",
  comingSoon: "Próximamente",
  lightMode: "Modo claro",
  darkMode: "Modo oscuro",
  switchToLight: "Cambiar al modo claro",
  switchToDark: "Cambiar al modo oscuro",
},

de: {
  personalSpace: "DEIN PERSÖNLICHER RAUM",
  conversation: "DEIN GESPRÄCH",
  wellnessCompanion: "Dein Begleiter für Wohlbefinden",
  conversationTitle: "MindBridge-Gespräch",
  openNavigation: "Navigation öffnen",
  conversationLanguage: "Gesprächssprache",
  autoDetect: "Automatisch erkennen",
  comingSoon: "Demnächst",
  lightMode: "Heller Modus",
  darkMode: "Dunkler Modus",
  switchToLight: "Zum hellen Modus wechseln",
  switchToDark: "Zum dunklen Modus wechseln",
},

};

function Icon({ icon, size = 20 }) {
  return <HugeiconsIcon icon={icon} size={size} />;
}

export default function Header({
  onOpenSidebar,
  language = "auto",
  onLanguageChange,
  darkMode,
  onToggleTheme,
  isChatActive = false,
}) {
  // Auto mode uses English UI labels.
  // Backend still detects the user's message language.
  const uiLanguage =
    language === "auto" ? "en" : language;

  const t = TRANSLATIONS[uiLanguage] || TRANSLATIONS.en;

  const isUrdu = uiLanguage === "ur";

  return (
    <header className="mb-header">
      <div className="mb-header-left">
        <button
          type="button"
          className="mb-header-icon-button mb-header-menu"
          onClick={onOpenSidebar}
          aria-label={t.openNavigation}
          title={t.openNavigation}
        >
          <Icon icon={Menu01Icon} size={21} />
        </button>

        <div
          className="mb-header-heading"
          dir={isUrdu ? "rtl" : "ltr"}
          lang={
            isUrdu
              ? "ur"
              : uiLanguage === "roman_ur"
                ? "ur-Latn"
                :  uiLanguage
          }
        >
          <span className="mb-header-eyebrow">
            {isChatActive
              ? t.conversation
              : t.personalSpace}
          </span>

          <h1>
            {isChatActive
              ? t.conversationTitle
              : t.wellnessCompanion}
          </h1>
        </div>
      </div>

      <div className="mb-header-actions">
        <label className="mb-header-language">
          <Icon icon={Globe02Icon} size={18} />

          <select
            aria-label={t.conversationLanguage}
            value={language}
            onChange={(event) =>
              onLanguageChange(event.target.value)
            }
          >
            <option value="auto">
              {t.autoDetect}
            </option>

            {LANGUAGES.map((item) => (
              <option
                key={item.code}
                value={item.code}
                disabled={!item.enabled}
              >
                {item.label}
                {!item.enabled
                  ? ` (${t.comingSoon})`
                  : ""}
              </option>
            ))}
          </select>
        </label>

        <button
          type="button"
          className="mb-header-icon-button"
          onClick={onToggleTheme}
          aria-label={
            darkMode
              ? t.switchToLight
              : t.switchToDark
          }
          title={
            darkMode
              ? t.lightMode
              : t.darkMode
          }
        >
          <Icon
            icon={darkMode ? Sun01Icon : Moon02Icon}
            size={20}
          />
        </button>
      </div>
    </header>
  );
}
