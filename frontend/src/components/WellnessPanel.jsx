
import { useEffect, useState } from "react";
import "./WellnessPanel.css";

const MOODS = ["😄", "🙂", "😐", "😔", "😟"];

const EN = {
  dashboard: "Everyday Wellbeing",
  subtitle: "A gentle space to reflect, check in, and care for yourself.",
  summary: "Today's summary",
  checkins: "Check-ins today",
  selfcareCount: "Self-care completed",
  reflections: "Reflections today",
  moodTitle: "Daily mood check-in",
  moodQuestion: "How are you feeling today?",
  moodNames: ["Great", "Good", "Okay", "Low", "Anxious"],
  moodPlaceholder: "Add an optional note about your day...",
  saveCheckin: "Save check-in",
  trends: "Mood activity trends",
  trendsInfo: "Number of mood check-ins per day",
  noTrends: "No mood check-ins in this period.",
  journal: "Daily reflection journal",
  journalQuestion: "What is one thing on your mind today?",
  journalPlaceholder: "Write your thoughts here...",
  saveReflection: "Save reflection",
  checklist: "Daily self-care checklist",
  checklistInfo: "Small actions can support your everyday wellbeing.",
  tasks: [
    "Drink some water",
    "Take a short break",
    "Move or stretch gently",
    "Connect with someone you trust",
    "Take a moment to relax",
  ],
  recent: "Recent check-ins",
  noEntries: "No check-ins yet.",
  journalNote: "Journal note",
  saved: "Saved for this browser session.",
  privacy:
    "Your check-ins and reflections stay in this open browser tab only. They are not permanently stored or shared.",
  toolkit: "Wellness toolkit",
  toolkitSubtitle: "Simple, interactive exercises for everyday wellbeing.",
  breathing: "Guided breathing",
  breathingInfo:
    "Breathe in gently for 4 seconds and out for 6 seconds. Stop if uncomfortable. Do not force or hold your breath.",
  inhale: "Breathe in",
  exhale: "Breathe out",
  ready: "Ready to begin",
  finished: "Exercise complete",
  start: "Start",
  pause: "Pause",
  resume: "Resume",
  reset: "Reset",
  grounding: "5-4-3-2-1 Grounding",
  groundingSteps: [
    "Notice 5 things you can see.",
    "Notice 4 things you can feel.",
    "Listen for 3 things you can hear.",
    "Notice 2 things you can smell.",
    "Notice 1 thing you can taste.",
  ],
  groundingDone: "Grounding exercise complete.",
  next: "Next step",
  restart: "Start again",
  guidedJournal: "Guided journaling",
  prompts: [
    "What is one small thing you need today?",
    "What are you grateful for today?",
    "What helped you feel calmer recently?",
  ],
  toolkitPlaceholder: "Write your reflection here...",
};

const TRANSLATIONS = {
  en: {},
  roman_ur: {
    subtitle: "Apne jazbaat samajhne aur apna khayal rakhne ki jagah.",
    summary: "Aaj ki summary",
    checkins: "Aaj ke check-ins",
    selfcareCount: "Self-care completed",
    reflections: "Aaj ki reflections",
    moodTitle: "Daily mood check-in",
    moodQuestion: "Aaj aap kaisa mehsoos kar rahe hain?",
    moodNames: ["Bohat acha", "Acha", "Theek", "Udaas", "Pareshan"],
    moodPlaceholder: "Aaj ke din ke bare mein kuch likhein...",
    saveCheckin: "Check-in save karein",
    trends: "Mood activity trends",
    trendsInfo: "Har din ke mood check-ins",
    noTrends: "Is period mein koi mood check-in nahi.",
    journal: "Daily reflection journal",
    journalQuestion: "Aaj aap ke zehan mein kya chal raha hai?",
    journalPlaceholder: "Apne khayalat yahan likhein...",
    saveReflection: "Reflection save karein",
    checklist: "Daily self-care checklist",
    checklistInfo: "Choti activities wellbeing mein madad kar sakti hain.",
    tasks: [
      "Pani piyein",
      "Thora break lein",
      "Halki stretching karein",
      "Kisi bharosemand shakhs se baat karein",
      "Kuch dair relax karein",
    ],
    recent: "Recent check-ins",
    noEntries: "Abhi koi check-in nahi.",
    journalNote: "Journal note",
    saved: "Is browser session mein save ho gaya.",
    privacy: "Entries sirf is open browser tab mein rehti hain.",
    toolkitSubtitle: "Rozmarra wellbeing ke liye asaan exercises.",
    breathing: "Saans ki mashq",
    breathingInfo:
      "4 seconds aahista saans andar lein aur 6 seconds bahar. Takleef ho to ruk jayein. Saans zabardasti na lein.",
    inhale: "Saans andar",
    exhale: "Saans bahar",
    ready: "Shuru karne ke liye tayyar",
    finished: "Mashq mukammal",
    start: "Shuru karein",
    pause: "Rokein",
    resume: "Jari rakhein",
    reset: "Reset",
    grounding: "5-4-3-2-1 Grounding",
    groundingSteps: [
      "5 cheezein dekhein.",
      "4 cheezein mehsoos karein.",
      "3 awaazein sunein.",
      "2 khushboo mehsoos karein.",
      "1 zaiqa mehsoos karein.",
    ],
    groundingDone: "Grounding exercise mukammal.",
    next: "Agla step",
    restart: "Dobara shuru karein",
    guidedJournal: "Guided journaling",
    prompts: [
      "Aaj aap ko kis choti cheez ki zaroorat hai?",
      "Aaj aap kis cheez ke liye shukar guzar hain?",
      "Haal hi mein kis cheez se sukoon mila?",
    ],
    toolkitPlaceholder: "Apne khayalat yahan likhein...",
  },
  ur: {
    dashboard: "روزمرہ فلاح و بہبود",
    subtitle: "اپنے احساسات سمجھنے اور اپنا خیال رکھنے کی جگہ۔",
    summary: "آج کا خلاصہ",
    checkins: "آج کے چیک اِن",
    selfcareCount: "مکمل سرگرمیاں",
    reflections: "آج کی تحریریں",
    moodTitle: "روزانہ موڈ چیک اِن",
    moodQuestion: "آج آپ کیسا محسوس کر رہے ہیں؟",
    moodNames: ["بہت اچھا", "اچھا", "ٹھیک", "اداس", "پریشان"],
    moodPlaceholder: "آج کے دن کے بارے میں لکھیں...",
    saveCheckin: "چیک اِن محفوظ کریں",
    trends: "موڈ کی سرگرمی",
    trendsInfo: "ہر دن کے موڈ چیک اِن کی تعداد",
    noTrends: "اس مدت میں کوئی چیک اِن نہیں۔",
    journal: "روزانہ خیالات کی ڈائری",
    journalQuestion: "آج آپ کے ذہن میں کیا چل رہا ہے؟",
    journalPlaceholder: "اپنے خیالات لکھیں...",
    saveReflection: "خیالات محفوظ کریں",
    checklist: "روزانہ خود کی دیکھ بھال",
    checklistInfo: "چھوٹی سرگرمیاں آپ کی فلاح میں مدد کر سکتی ہیں۔",
    tasks: [
      "پانی پئیں",
      "تھوڑا وقفہ لیں",
      "ہلکی ورزش کریں",
      "کسی قابل اعتماد شخص سے بات کریں",
      "کچھ دیر آرام کریں",
    ],
    recent: "حالیہ چیک اِن",
    noEntries: "ابھی کوئی چیک اِن نہیں۔",
    journalNote: "ڈائری نوٹ",
    saved: "اس براؤزر سیشن میں محفوظ ہو گیا۔",
    privacy: "آپ کی تحریریں صرف اس کھلے براؤزر ٹیب میں رہتی ہیں۔",
    toolkit: "فلاح و بہبود کے طریقے",
    toolkitSubtitle: "روزمرہ سکون کے لیے آسان مشقیں۔",
    breathing: "سانس کی مشق",
    breathingInfo:
      "چار سیکنڈ آہستہ سانس اندر لیں اور چھ سیکنڈ باہر نکالیں۔ تکلیف ہو تو رک جائیں۔",
    inhale: "سانس اندر",
    exhale: "سانس باہر",
    ready: "شروع کرنے کے لیے تیار",
    finished: "مشق مکمل",
    start: "شروع کریں",
    pause: "روکیں",
    resume: "جاری رکھیں",
    reset: "دوبارہ شروع",
    grounding: "۵-۴-۳-۲-۱ گراؤنڈنگ",
    groundingSteps: [
      "پانچ چیزیں دیکھیں۔",
      "چار چیزیں محسوس کریں۔",
      "تین آوازیں سنیں۔",
      "دو خوشبوئیں محسوس کریں۔",
      "ایک ذائقہ محسوس کریں۔",
    ],
    groundingDone: "مشق مکمل ہو گئی۔",
    next: "اگلا مرحلہ",
    restart: "دوبارہ شروع کریں",
    guidedJournal: "رہنمائی کے ساتھ ڈائری",
    prompts: [
      "آج آپ کو کس چھوٹی چیز کی ضرورت ہے؟",
      "آج آپ کس چیز کے لیے شکر گزار ہیں؟",
      "حال ہی میں کس چیز سے سکون ملا؟",
    ],
    toolkitPlaceholder: "اپنے خیالات لکھیں...",
  },
  es: {
    dashboard: "Bienestar diario",
    subtitle: "Un espacio tranquilo para reflexionar y cuidarte.",
    summary: "Resumen de hoy",
    checkins: "Registros de hoy",
    selfcareCount: "Autocuidado completado",
    reflections: "Reflexiones de hoy",
    moodTitle: "Registro diario de ánimo",
    moodQuestion: "¿Cómo te sientes hoy?",
    moodNames: ["Genial", "Bien", "Normal", "Triste", "Ansioso"],
    moodPlaceholder: "Añade una nota opcional...",
    saveCheckin: "Guardar registro",
    trends: "Actividad del estado de ánimo",
    trendsInfo: "Registros de ánimo por día",
    noTrends: "No hay registros en este período.",
    journal: "Diario de reflexión",
    journalQuestion: "¿Qué tienes en mente hoy?",
    journalPlaceholder: "Escribe tus pensamientos...",
    saveReflection: "Guardar reflexión",
    checklist: "Lista diaria de autocuidado",
    checklistInfo: "Las pequeñas acciones pueden apoyar tu bienestar.",
    tasks: [
      "Beber agua",
      "Tomar un descanso",
      "Estirarte suavemente",
      "Hablar con alguien de confianza",
      "Tomar un momento para relajarte",
    ],
    recent: "Registros recientes",
    noEntries: "Todavía no hay registros.",
    journalNote: "Nota del diario",
    saved: "Guardado durante esta sesión.",
    privacy: "Tus registros permanecen solo en esta pestaña abierta.",
    toolkit: "Herramientas de bienestar",
    toolkitSubtitle: "Ejercicios sencillos para tu bienestar diario.",
    breathing: "Respiración guiada",
    breathingInfo:
      "Inhala suavemente durante 4 segundos y exhala durante 6. Detente si te incomoda.",
    inhale: "Inhala",
    exhale: "Exhala",
    ready: "Listo para empezar",
    finished: "Ejercicio completado",
    start: "Iniciar",
    pause: "Pausar",
    resume: "Continuar",
    reset: "Reiniciar",
    grounding: "Conexión 5-4-3-2-1",
    groundingSteps: [
      "Nombra 5 cosas que ves.",
      "Nota 4 cosas que sientes.",
      "Escucha 3 sonidos.",
      "Identifica 2 olores.",
      "Nota 1 sabor.",
    ],
    groundingDone: "Ejercicio completado.",
    next: "Siguiente paso",
    restart: "Empezar de nuevo",
    guidedJournal: "Diario guiado",
    prompts: [
      "¿Qué pequeña cosa necesitas hoy?",
      "¿Por qué estás agradecido hoy?",
      "¿Qué te ayudó a sentir calma recientemente?",
    ],
    toolkitPlaceholder: "Escribe tu reflexión...",
  },
  de: {
    dashboard: "Tägliches Wohlbefinden",
    subtitle: "Ein ruhiger Ort für Reflexion und Selbstfürsorge.",
    summary: "Heutige Übersicht",
    checkins: "Heutige Einträge",
    selfcareCount: "Selbstfürsorge erledigt",
    reflections: "Heutige Reflexionen",
    moodTitle: "Täglicher Stimmungscheck",
    moodQuestion: "Wie fühlst du dich heute?",
    moodNames: ["Sehr gut", "Gut", "Okay", "Traurig", "Ängstlich"],
    moodPlaceholder: "Optionale Notiz hinzufügen...",
    saveCheckin: "Eintrag speichern",
    trends: "Stimmungsaktivität",
    trendsInfo: "Stimmungseinträge pro Tag",
    noTrends: "Keine Einträge in diesem Zeitraum.",
    journal: "Tägliche Reflexion",
    journalQuestion: "Was beschäftigt dich heute?",
    journalPlaceholder: "Schreibe deine Gedanken auf...",
    saveReflection: "Reflexion speichern",
    checklist: "Tägliche Selbstfürsorge",
    checklistInfo: "Kleine Schritte können dein Wohlbefinden unterstützen.",
    tasks: [
      "Wasser trinken",
      "Eine kurze Pause machen",
      "Sanft bewegen oder dehnen",
      "Mit einer vertrauten Person sprechen",
      "Einen Moment entspannen",
    ],
    recent: "Letzte Einträge",
    noEntries: "Noch keine Einträge.",
    journalNote: "Tagebuchnotiz",
    saved: "Für diese Sitzung gespeichert.",
    privacy: "Deine Einträge bleiben nur in diesem geöffneten Tab.",
    toolkit: "Wellness-Tools",
    toolkitSubtitle: "Einfache Übungen für dein Wohlbefinden.",
    breathing: "Geführte Atmung",
    breathingInfo:
      "Atme sanft 4 Sekunden ein und 6 Sekunden aus. Stoppe bei Unwohlsein.",
    inhale: "Einatmen",
    exhale: "Ausatmen",
    ready: "Bereit zum Start",
    finished: "Übung abgeschlossen",
    start: "Starten",
    pause: "Pause",
    resume: "Fortsetzen",
    reset: "Zurücksetzen",
    grounding: "5-4-3-2-1 Achtsamkeit",
    groundingSteps: [
      "Nenne 5 Dinge, die du siehst.",
      "Spüre 4 Dinge.",
      "Höre 3 Geräusche.",
      "Bemerke 2 Gerüche.",
      "Nimm 1 Geschmack wahr.",
    ],
    groundingDone: "Übung abgeschlossen.",
    next: "Nächster Schritt",
    restart: "Neu beginnen",
    guidedJournal: "Geführtes Tagebuch",
    prompts: [
      "Was brauchst du gerade?",
      "Wofür bist du heute dankbar?",
      "Was hat dir kürzlich Ruhe gegeben?",
    ],
    toolkitPlaceholder: "Schreibe deine Reflexion...",
  },
};

function dayKey(value) {
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return "";

  return [
    date.getFullYear(),
    String(date.getMonth() + 1).padStart(2, "0"),
    String(date.getDate()).padStart(2, "0"),
  ].join("-");
}

function isMoodEntry(entry) {
  return (
    Number.isInteger(entry?.mood) &&
    entry.mood >= 0 &&
    entry.mood < MOODS.length
  );
}

export default function WellnessPanel({
  mode = "mood",
  language = "auto",
  entries = [],
  onSave,
}) {
  const lang = TRANSLATIONS[language] ? language : "en";
  const t = { ...EN, ...TRANSLATIONS[lang] };
  const safeEntries = Array.isArray(entries) ? entries : [];

  const [mood, setMood] = useState(null);
  const [note, setNote] = useState("");
  const [reflection, setReflection] = useState("");
  const [period, setPeriod] = useState(7);
  const [notice, setNotice] = useState("");

  const [care, setCare] = useState({
    date: dayKey(new Date()),
    completed: [],
  });

  const [seconds, setSeconds] = useState(60);
  const [running, setRunning] = useState(false);
  const [groundingStep, setGroundingStep] = useState(0);
  const [promptIndex, setPromptIndex] = useState(0);
  const [toolkitNote, setToolkitNote] = useState("");

  // Breathing timer: six cycles of 4s inhale + 6s exhale.
  useEffect(() => {
    if (!running) return;

    const timer = window.setInterval(() => {
      setSeconds((previous) => Math.max(0, previous - 1));
    }, 1000);

    return () => window.clearInterval(timer);
  }, [running]);

  useEffect(() => {
    if (seconds === 0) setRunning(false);
  }, [seconds]);

  const today = dayKey(new Date());
  const completed = care.date === today ? care.completed : [];

  const todayEntries = safeEntries.filter(
    (entry) => dayKey(entry?.date) === today
  );

  const moodCount = todayEntries.filter(isMoodEntry).length;

  const reflectionCount = todayEntries.filter(
    (entry) => typeof entry?.note === "string" && entry.note.trim()
  ).length;

  function saveEntry(selectedMood, text) {
    if (typeof onSave !== "function") return;

    const cleanText = text.trim();
    if (selectedMood === null && !cleanText) return;

    onSave({
      mood: selectedMood,
      note: cleanText,
      date: new Date().toISOString(),
    });

    setNotice(t.saved);
  }

  function saveMood() {
    if (mood === null && !note.trim()) return;
    saveEntry(mood, note);
    setMood(null);
    setNote("");
  }

  function saveJournal() {
    if (!reflection.trim()) return;
    saveEntry(null, reflection);
    setReflection("");
  }

  function saveToolkitJournal() {
    if (!toolkitNote.trim()) return;
    saveEntry(null, toolkitNote);
    setToolkitNote("");
  }

  function toggleCare(index) {
    setCare((previous) => {
      const current =
        previous.date === today ? previous.completed : [];

      return {
        date: today,
        completed: current.includes(index)
          ? current.filter((value) => value !== index)
          : [...current, index],
      };
    });
  }

  const trendData = Array.from({ length: period }, (_, index) => {
    const date = new Date();
    date.setHours(12, 0, 0, 0);
    date.setDate(date.getDate() - (period - 1 - index));

    const key = dayKey(date);

    return {
      key,
      label: date.toLocaleDateString(
        lang === "roman_ur" ? "en-PK" : lang,
        { month: "short", day: "numeric" }
      ),
      count: safeEntries.filter(
        (entry) => dayKey(entry?.date) === key && isMoodEntry(entry)
      ).length,
    };
  });

  const maxCount = Math.max(1, ...trendData.map((item) => item.count));
  const hasTrendData = trendData.some((item) => item.count > 0);

  // 60 seconds = six 10-second breathing cycles.
  const elapsed = 60 - seconds;
  const phaseSeconds = elapsed % 10;
  const inhaling = phaseSeconds < 4;
  const phaseLabel = inhaling ? t.inhale : t.exhale;

  function resetBreathing() {
    setRunning(false);
    setSeconds(60);
  }

  function renderToolkit() {
    return (
      <div className="toolkit-grid">
        <section className="wellness-section">
          <h2>🌿 {t.breathing}</h2>
          <p>{t.breathingInfo}</p>

          <div
            className={`breathing-circle ${
              running ? "breathing-active" : ""
            }`}
            style={{
              transform:
                running && inhaling ? "scale(1.06)" : "scale(0.94)",
            }}
            aria-live="off"
          >
            <span>
              {seconds === 0
                ? t.finished
                : running
                ? phaseLabel
                : t.ready}
            </span>
          </div>

          <div className="breathing-time">{seconds}s</div>

          <div className="toolkit-actions">
            <button
              type="button"
              className="wellness-save"
              disabled={seconds === 0}
              onClick={() => setRunning((previous) => !previous)}
            >
              {running
                ? t.pause
                : seconds < 60
                ? t.resume
                : t.start}
            </button>

            <button
              type="button"
              className="toolkit-secondary"
              onClick={resetBreathing}
            >
              {t.reset}
            </button>
          </div>
        </section>

        <section className="wellness-section">
          <h2>🪴 {t.grounding}</h2>

          <div className="grounding-progress">
            {t.groundingSteps.map((_, index) => (
              <span
                key={index}
                className={index < groundingStep ? "active" : ""}
              />
            ))}
          </div>

          {groundingStep < 5 ? (
            <>
              <div className="grounding-step">
                <strong>{groundingStep + 1}/5</strong>
                <p>{t.groundingSteps[groundingStep]}</p>
              </div>

              <button
                type="button"
                className="wellness-save"
                onClick={() =>
                  setGroundingStep((previous) =>
                    Math.min(5, previous + 1)
                  )
                }
              >
                {t.next}
              </button>
            </>
          ) : (
            <>
              <p>{t.groundingDone}</p>
              <button
                type="button"
                className="wellness-save"
                onClick={() => setGroundingStep(0)}
              >
                {t.restart}
              </button>
            </>
          )}
        </section>

        <section className="wellness-section toolkit-journal">
          <h2>📓 {t.guidedJournal}</h2>

          <div className="journal-prompts">
            {t.prompts.map((prompt, index) => (
              <button
                type="button"
                key={index}
                className={promptIndex === index ? "active" : ""}
                aria-pressed={promptIndex === index}
                onClick={() => setPromptIndex(index)}
              >
                {prompt}
              </button>
            ))}
          </div>

          <p>{t.prompts[promptIndex]}</p>

          <textarea
            className="mood-note"
            value={toolkitNote}
            maxLength={1000}
            placeholder={t.toolkitPlaceholder}
            aria-label={t.toolkitPlaceholder}
            onChange={(event) => {
              setToolkitNote(event.target.value);
              setNotice("");
            }}
          />

          <button
            type="button"
            className="wellness-save"
            disabled={!toolkitNote.trim() || typeof onSave !== "function"}
            onClick={saveToolkitJournal}
          >
            {t.saveReflection}
          </button>

          {notice && <p role="status">{notice}</p>}
        </section>
      </div>
    );
  }

  function renderDashboard() {
    return (
      <>
        <section className="wellness-section">
          <h2>{t.summary}</h2>

          <div className="wellness-summary-grid">
            {[
              ["💚", moodCount, t.checkins],
              ["🌿", `${completed.length}/5`, t.selfcareCount],
              ["📝", reflectionCount, t.reflections],
            ].map(([icon, value, label]) => (
              <div className="wellness-summary-card" key={label}>
                <div className="wellness-summary-icon">{icon}</div>
                <div className="wellness-summary-value">{value}</div>
                <div className="wellness-summary-label">{label}</div>
              </div>
            ))}
          </div>
        </section>

        <section className="wellness-section">
          <h2>{t.moodTitle}</h2>
          <p>{t.moodQuestion}</p>

          <div className="mood-options">
            {MOODS.map((emoji, index) => (
              <button
                type="button"
                key={index}
                className={mood === index ? "selected" : ""}
                aria-pressed={mood === index}
                onClick={() => {
                  setMood(index);
                  setNotice("");
                }}
              >
                <span className="mood-face">{emoji}</span>
                <span className="mood-label">{t.moodNames[index]}</span>
              </button>
            ))}
          </div>

          <textarea
            className="mood-note"
            value={note}
            maxLength={500}
            placeholder={t.moodPlaceholder}
            aria-label={t.moodPlaceholder}
            onChange={(event) => {
              setNote(event.target.value);
              setNotice("");
            }}
          />

          <button
            type="button"
            className="wellness-save"
            disabled={
              (mood === null && !note.trim()) ||
              typeof onSave !== "function"
            }
            onClick={saveMood}
          >
            {t.saveCheckin}
          </button>
        </section>

        <section className="wellness-section wellness-trends-section">
          <div className="wellness-section-heading">
            <div>
              <h2>{t.trends}</h2>
              <p>{t.trendsInfo}</p>
            </div>

            <div className="wellness-periods">
              {[7, 30].map((value) => (
                <button
                  type="button"
                  key={value}
                  className={period === value ? "active" : ""}
                  aria-pressed={period === value}
                  onClick={() => setPeriod(value)}
                >
                  {value} {lang === "de" ? "Tage" : lang === "es" ? "días" : "days"}
                </button>
              ))}
            </div>
          </div>

          {!hasTrendData ? (
            <p className="wellness-empty">{t.noTrends}</p>
          ) : (
            <div
              className={`wellness-chart ${
                period === 30 ? "wellness-chart-30" : ""
              }`}
              role="img"
              aria-label={t.trendsInfo}
            >
              {trendData.map((item, index) => (
                <div
                  className="wellness-chart-column"
                  key={item.key}
                  title={`${item.label}: ${item.count}`}
                >
                  <span className="wellness-chart-value">
                    {item.count || ""}
                  </span>

                  <div className="wellness-chart-track">
                    <div
                      className="wellness-chart-bar"
                      style={{
                        height: `${
                          (item.count / maxCount) * 100
                        }%`,
                      }}
                    />
                  </div>

                  <span className="wellness-chart-date">
                    {period === 7 ||
                    index % 5 === 0 ||
                    index === period - 1
                      ? item.label
                      : ""}
                  </span>
                </div>
              ))}
            </div>
          )}
        </section>

        <div className="wellness-two-columns">
          <section className="wellness-section">
            <h2>{t.journal}</h2>
            <p>{t.journalQuestion}</p>

            <textarea
              className="mood-note wellness-journal-input"
              value={reflection}
              maxLength={1000}
              placeholder={t.journalPlaceholder}
              aria-label={t.journalPlaceholder}
              onChange={(event) => {
                setReflection(event.target.value);
                setNotice("");
              }}
            />

            <button
              type="button"
              className="wellness-save"
              disabled={
                !reflection.trim() ||
                typeof onSave !== "function"
              }
              onClick={saveJournal}
            >
              {t.saveReflection}
            </button>
          </section>

          <section className="wellness-section">
            <h2>{t.checklist}</h2>
            <p>{t.checklistInfo}</p>

            <div className="wellness-checklist">
              {t.tasks.map((task, index) => (
                <label
                  key={index}
                  className={`wellness-check-item ${
                    completed.includes(index) ? "completed" : ""
                  }`}
                >
                  <input
                    type="checkbox"
                    checked={completed.includes(index)}
                    onChange={() => toggleCare(index)}
                  />
                  <span>{task}</span>
                </label>
              ))}
            </div>
          </section>
        </div>

        <section className="wellness-section">
          <h2>{t.recent}</h2>

          <div className="mood-log">
            {safeEntries.length === 0 ? (
              <p className="wellness-empty">{t.noEntries}</p>
            ) : (
              safeEntries.map((entry, index) => {
                const validMood = isMoodEntry(entry);
                const date = new Date(entry?.date);

                return (
                  <div className="wellness-log-entry" key={index}>
                    <div className="wellness-log-header">
                      <strong>
                        {validMood
                          ? `${MOODS[entry.mood]} ${
                              t.moodNames[entry.mood]
                            }`
                          : t.journalNote}
                      </strong>

                      {!Number.isNaN(date.getTime()) && (
                        <small>
                          {date.toLocaleString(
                            lang === "roman_ur" ? "en-PK" : lang
                          )}
                        </small>
                      )}
                    </div>

                    {entry?.note && <p>{entry.note}</p>}
                  </div>
                );
              })
            )}
          </div>
        </section>

        {notice && <p role="status">{notice}</p>}
      </>
    );
  }

  return (
    <div className="wellness-scroll">
      <div
        className="wellness-wrap"
        dir={lang === "ur" ? "rtl" : "ltr"}
      >
        <div className="wellness-kicker">
          MINDBRIDGE AI · WELLNESS
        </div>

        <h1>{mode === "toolkit" ? t.toolkit : t.dashboard}</h1>

        <p className="wellness-subtitle">
          {mode === "toolkit" ? t.toolkitSubtitle : t.subtitle}
        </p>

        {mode === "toolkit" ? renderToolkit() : renderDashboard()}

        <p className="wellness-note">{t.privacy}</p>
      </div>
    </div>
  );
}
