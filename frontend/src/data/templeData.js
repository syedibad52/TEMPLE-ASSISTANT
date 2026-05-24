/**
 * Client-side temple data and configuration.
 * Used for static content rendering and example questions.
 */

export const TEMPLE_NAME = "Sri Raghavendra Swamy Temple";
export const TEMPLE_NAME_KN = "ಶ್ರೀ ರಾಘವೇಂದ್ರ ಸ್ವಾಮಿ ದೇವಸ್ಥಾನ";

export const NAV_ITEMS = [
  { label: "Home", labelKn: "ಮುಖಪುಟ", href: "/" },
  { label: "About", labelKn: "ಬಗ್ಗೆ", href: "/about" },
  { label: "Pooja Timings", labelKn: "ಪೂಜಾ ಸಮಯ", href: "/pooja" },
  { label: "Festivals", labelKn: "ಹಬ್ಬಗಳು", href: "/festivals" },
  { label: "Donations", labelKn: "ದಾನ", href: "/donations" },
  { label: "Contact", labelKn: "ಸಂಪರ್ಕ", href: "/contact" },
  { label: "AI Assistant", labelKn: "AI ಸಹಾಯಕ", href: "/assistant", highlight: true },
];

export const EXAMPLE_QUESTIONS = [
  {
    en: "What time does the temple open?",
    kn: "ದೇವಸ್ಥಾನ ಯಾವ ಸಮಯಕ್ಕೆ ತೆರೆಯುತ್ತದೆ?",
  },
  {
    en: "What is today's pooja schedule?",
    kn: "ಇವತ್ತು ಪೂಜೆ ಯಾವಾಗ?",
  },
  {
    en: "Is the temple open now?",
    kn: "ದೇವಸ್ಥಾನ ಈಗ ತೆರೆದಿದೆಯೇ?",
  },
  {
    en: "When is prasada time?",
    kn: "ಪ್ರಸಾದ ಸಮಯ ಯಾವಾಗ?",
  },
  {
    en: "Any special pooja today?",
    kn: "ಇಂದು ವಿಶೇಷ ಪೂಜೆ ಇದೆಯೇ?",
  },
  {
    en: "Is parking available?",
    kn: "ಪಾರ್ಕಿಂಗ್ ಲಭ್ಯವಿದೆಯೇ?",
  },
  {
    en: "What are the darshan timings?",
    kn: "ದರ್ಶನ ಸಮಯ ಯಾವಾಗ?",
  },
  {
    en: "Upcoming festivals?",
    kn: "ಮುಂಬರುವ ಹಬ್ಬಗಳು?",
  },
];

export const ABOUT_CONTENT = {
  history: {
    en: "Sri Raghavendra Swamy Temple is one of the most revered temples in South India, dedicated to Sri Guru Raghavendra Swamy. The temple stands as a beacon of spiritual wisdom, attracting millions of devotees from across the world who seek divine blessings and inner peace.",
    kn: "ಶ್ರೀ ರಾಘವೇಂದ್ರ ಸ್ವಾಮಿ ದೇವಸ್ಥಾನವು ದಕ್ಷಿಣ ಭಾರತದ ಅತ್ಯಂತ ಪೂಜ್ಯ ದೇವಸ್ಥಾನಗಳಲ್ಲಿ ಒಂದಾಗಿದೆ, ಶ್ರೀ ಗುರು ರಾಘವೇಂದ್ರ ಸ್ವಾಮಿಗಳಿಗೆ ಸಮರ್ಪಿತವಾಗಿದೆ.",
  },
  significance: {
    en: "The Brindavana (sacred tomb) of Sri Raghavendra Swamy is the main attraction. Devotees believe that the Guru entered the Brindavana alive and continues to bless devotees even today. The temple is known for its divine vibrations and miraculous healing powers.",
    kn: "ಶ್ರೀ ರಾಘವೇಂದ್ರ ಸ್ವಾಮಿಗಳ ಬೃಂದಾವನ (ಪವಿತ್ರ ಸಮಾಧಿ) ಮುಖ್ಯ ಆಕರ್ಷಣೆಯಾಗಿದೆ.",
  },
};

export const FOOTER_DATA = {
  address: "Temple Road, Mantralayam, Kurnool District, Andhra Pradesh 518345",
  phone: "+91 9876543210",
  email: "info@sriraghavendraswamy.org",
  timings: "5:00 AM – 9:00 PM (Break: 12:30 PM – 4:00 PM)",
};

export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
