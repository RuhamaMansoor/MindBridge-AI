
import {
  Add01Icon,
  Brain02Icon,
  Cancel01Icon,
  HeartAddIcon,
  Shield01Icon
} from "@hugeicons/core-free-icons";

import { HugeiconsIcon } from "@hugeicons/react";
import { motion } from "motion/react";
import "./Sidebar.css";

const TRANSLATIONS = {
  en: {
    closeNavigation: "Close navigation",
    mainNavigation: "Main navigation",
    closeSidebar: "Close sidebar",
    companion: "YOUR WELLNESS COMPANION",
    newConversation: "New conversation",
    wellnessNavigation: "Wellness navigation",
    yourSpace: "YOUR SPACE",
    currentConversation: "Current conversation",
    everydayWellbeing: "Everyday wellbeing",
    soon: "Soon",
    supportiveSpace: "A supportive space",
    privacy:
      "Conversations are temporary. MindBridge AI does not replace professional care.",
    copyright: "MindBridge AI · Wellness with care",
  },

  roman_ur: {
    closeNavigation: "Navigation band karein",
    mainNavigation: "Main navigation",
    closeSidebar: "Sidebar band karein",
    companion: "AAP KA WELLNESS COMPANION",
    newConversation: "Nayi guftagu",
    wellnessNavigation: "Wellness navigation",
    yourSpace: "AAP KI JAGAH",
    currentConversation: "Mojooda guftagu",
    everydayWellbeing: "Rozana zehni sehat",
    soon: "Jald",
    supportiveSpace: "Ek madadgar jagah",
    privacy:
      "Guftagu aarzi hoti hai. MindBridge AI professional care ka badal nahi hai.",
    copyright: "MindBridge AI · Aap ki sehat ka khayal",
  },

  ur: {
    closeNavigation: "نیویگیشن بند کریں",
    mainNavigation: "مرکزی نیویگیشن",
    closeSidebar: "سائیڈ بار بند کریں",
    companion: "آپ کا فلاح و بہبود کا ساتھی",
    newConversation: "نئی گفتگو",
    wellnessNavigation: "فلاح و بہبود کی نیویگیشن",
    yourSpace: "آپ کی جگہ",
    currentConversation: "موجودہ گفتگو",
    everydayWellbeing: "روزمرہ ذہنی صحت",
    soon: "جلد",
    supportiveSpace: "ایک معاون جگہ",
    privacy:
      "گفتگو عارضی ہوتی ہے۔ مائنڈ برج اے آئی پیشہ ورانہ طبی نگہداشت کا متبادل نہیں ہے۔",
    copyright: "مائنڈ برج اے آئی · آپ کی صحت کا خیال",
  },

  es: {
    closeNavigation: "Cerrar navegación",
    mainNavigation: "Navegación principal",
    closeSidebar: "Cerrar barra lateral",
    companion: "TU COMPAÑERO DE BIENESTAR",
    newConversation: "Nueva conversación",
    wellnessNavigation: "Navegación de bienestar",
    yourSpace: "TU ESPACIO",
    currentConversation: "Conversación actual",
    everydayWellbeing: "Bienestar diario",
    soon: "Próximamente",
    supportiveSpace: "Un espacio de apoyo",
    privacy:
      "Las conversaciones son temporales. MindBridge AI no sustituye la atención profesional.",
    copyright: "MindBridge AI · Bienestar con cuidado",
  },

  de: {
    closeNavigation: "Navigation schließen",
    mainNavigation: "Hauptnavigation",
    closeSidebar: "Seitenleiste schließen",
    companion: "DEIN BEGLEITER FÜR WOHLBEFINDEN",
    newConversation: "Neues Gespräch",
    wellnessNavigation: "Wohlbefinden-Navigation",
    yourSpace: "DEIN RAUM",
    currentConversation: "Aktuelles Gespräch",
    everydayWellbeing: "Wohlbefinden im Alltag",
    soon: "Demnächst",
    supportiveSpace: "Ein unterstützender Raum",
    privacy:
      "Gespräche sind vorübergehend. MindBridge AI ersetzt keine professionelle Betreuung.",
    copyright: "MindBridge AI · Wohlbefinden mit Fürsorge",
  },
};

function Icon({ icon, size = 20 }) {
  return <HugeiconsIcon icon={icon} size={size} />;
}

export default function Sidebar({
  isOpen,
  onClose,
  onNewConversation,
  isLoading = false,
  language = "auto",
  page = 'chat', chats = [], onOpenChat, onDeleteChat, onNavigate,
}) {
  const currentLanguage =
    language === "auto" ? "en" : language;

  const t =
    TRANSLATIONS[currentLanguage] ||
    TRANSLATIONS.en;

  const isUrdu = currentLanguage === "ur";

  const languageTag =
    currentLanguage === "roman_ur"
      ? "ur-Latn"
      : currentLanguage;

  return (
    <>
      {isOpen && (
        <button
          type="button"
          className="mb-sidebar-overlay"
          aria-label={t.closeNavigation}
          onClick={onClose}
        />
      )}

      <motion.aside
        className={`mb-sidebar ${
          isOpen ? "is-open" : ""
        }`}
        initial={false}
        aria-label={t.mainNavigation}
        lang={languageTag}
        dir={isUrdu ? "rtl" : "ltr"}
      >
        <div className="mb-sidebar-brand">
          <div className="mb-sidebar-logo">
            <Icon icon={Brain02Icon} size={25} />
          </div>

          <div className="mb-sidebar-brand-text">
            <strong>MindBridge AI</strong>
            <span>{t.companion}</span>
          </div>

          <button
            type="button"
            className="mb-sidebar-close"
            onClick={onClose}
            aria-label={t.closeSidebar}
          >
            <Icon icon={Cancel01Icon} size={19} />
          </button>
        </div>

        <button
          type="button"
          className="mb-new-conversation"
          onClick={onNewConversation}
          disabled={isLoading}
        >
          <Icon icon={Add01Icon} size={19} />
          <span>{t.newConversation}</span>
        </button>

        <nav
          className="mb-sidebar-nav"
          aria-label={t.wellnessNavigation}
        >
          <p className="mb-sidebar-label">
            {t.yourSpace}
          </p>

         
        <button
          type="button"
          className={`mb-sidebar-nav-item ${
            page === "chat" ? "is-active" : ""
          }`}
          onClick={() => onNavigate("chat")}
          disabled={isLoading}
        >
          <Icon icon={HeartAddIcon} size={19} />
          <span>{t.currentConversation}</span>
        </button>


          
            <button
              type="button"
              className={`mb-sidebar-nav-item ${
                page === "mood" ? "is-active" : ""
              }`}
              onClick={() => onNavigate("mood")}
              disabled={isLoading}
            >
              <Icon icon={HeartAddIcon} size={19} />
              <span>{t.everydayWellbeing}</span>
            </button>

        </nav>

        <div className="mb-sidebar-extras">
          
          <button className={`mb-side-action ${page==='toolkit'?'is-active':''}`} onClick={()=>onNavigate('toolkit')}>🌿 <span>{({en:'Wellness toolkit',de:'Wellness-Tools',es:'Herramientas de bienestar',ur:'فلاح و بہبود',roman_ur:'Wellness toolkit'})[currentLanguage]||'Wellness toolkit'}</span></button>
          <div className="mb-history-title">{({en:'CHAT HISTORY',de:'CHATVERLAUF',es:'HISTORIAL',ur:'گفتگو کی تاریخ',roman_ur:'CHAT HISTORY'})[currentLanguage]||'CHAT HISTORY'} <small>tab only</small></div>
          <div className="mb-history-list">{chats.length===0?<p className="mb-history-empty">No previous conversations in this tab yet.</p>:chats.map(chat=><div className="mb-history-item" key={chat.id}><button onClick={()=>onOpenChat(chat)} title={chat.title}>{chat.title}</button><button aria-label="Delete chat" title="Delete chat" className="mb-history-delete" onClick={()=>onDeleteChat(chat.id)}>×</button></div>)}</div>
        </div>
        <div className="mb-sidebar-bottom">
          <div className="mb-privacy-card">
            <Icon icon={Shield01Icon} size={20} />
            <div>
              <strong>{t.supportiveSpace}</strong>
              <p>{t.privacy}</p>
            </div>
          </div>

          <p className="mb-sidebar-copyright">
            {t.copyright}
          </p>
        </div>
      </motion.aside>
    </>
  );
}
