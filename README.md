# Inclusive Design Persona Cards

A printable, accessible web application featuring 40 research-backed persona cards for inclusive design practice.

---

## About

Inclusive Design Persona Cards help product teams move beyond abstract accessibility guidelines by putting real human experiences at the center of design decisions. Each card profiles a person living with a disability, chronic condition, cognitive difference, or situational impairment — covering their digital challenges, the assistive technologies they rely on, and concrete design recommendations.

Use the cards during design critiques, sprint planning, usability reviews, or AI-assisted accessibility audits to build empathy and identify barriers before they reach production.

---

## Features

- **40 persona cards** across 8 disability and impairment categories
- **WCAG 2.2 AA compliant** — semantic HTML, proper landmark regions, skip navigation, keyboard accessible, minimum contrast ratios of 11:1
- **Printable double-sided cards** — fold-over layout sized for a half sheet of letter paper
- **Built-in AI audit prompts** — each card includes a pre-written prompt mapped to WCAG 2.2 criteria for use with AI development tools
- **No frameworks** — pure PHP, CSS, and JSON; no build tools, no npm, no React
- **Responsive layout** — horizontal card grid on desktop, vertical stack on mobile

---

## Card Categories

| Category | Cards | Covers |
|---|---|---|
| Auditory | 3 | Deafness, hard of hearing, noisy environments |
| Cognitive | 4 | Memory, attention, processing, literacy |
| Intersectional | 11 | Multiple overlapping conditions and identities |
| Mental Health | 5 | Anxiety, depression, PTSD, and related conditions |
| Neurodiversity | 3 | ADHD, autism, dyslexia |
| Physical | 5 | Motor impairments, tremors, limited dexterity |
| Speech | 2 | Nonverbal communication, speech differences |
| Visual | 7 | Blindness, low vision, color vision deficiency |

---

## Getting Started

### Requirements

- **PHP 8.0+** (recommended for production or local use), or
- **Python 3** (included preview server for development without PHP)

### Run with PHP

```bash
git clone <your-repo-url>
cd "Inclusive Design Persona Cards"
php -S localhost:8000
```

Open [http://localhost:8000](http://localhost:8000) in your browser.

### Run with the Python preview server

A Python server is included that mirrors the PHP application logic — useful if PHP is not installed locally.

```bash
python3 server.py
```

Open [http://localhost:8765](http://localhost:8765) in your browser.

---

## File Structure

```
Inclusive Design Persona Cards/
├── index.php          # Home page — all 40 cards grouped by category
├── card.php           # Individual card detail page (?id=N)
├── 404.php            # 404 error page
├── server.py          # Python development preview server
├── css/
│   └── style.css      # All styles, including print media query
└── data/
    └── cards.json     # Source data — 40 persona cards
```

---

## Data Schema

Each entry in `data/cards.json` contains the following fields:

| Field | Type | Description |
|---|---|---|
| `id` | integer | Unique card identifier, used in URL (`card.php?id=N`) |
| `title` | string | Condition or impairment name (e.g. "Deaf", "Low Vision") |
| `name` | string | Persona first name |
| `backstory` | string | Brief biographical description of the persona |
| `category` | string | One of 8 categories (e.g. "Auditory", "Visual") |
| `conditionDescription` | string | Plain-language explanation of the condition |
| `digitalChallenges` | string | Specific barriers this persona encounters in digital products |
| `assistiveTechnologies` | array | Technologies the persona uses (e.g. screen readers, captions) |
| `designConsiderations` | string | Actionable guidance for designers and developers |
| `aiPrompt` | string | Pre-written prompt for AI-assisted accessibility audits |
| `clinicalExamples` | string | Related clinical or diagnostic examples |
| `aiPromptUrl` | string | External URL to the full hosted prompt |

### Example entry

```json
{
  "id": 11,
  "title": "Deaf",
  "name": "Angela",
  "backstory": "Angela, 34, Black, rents an apartment with her partner. Works remotely as a UX researcher and uses ASL as her primary language.",
  "category": "Auditory",
  "conditionDescription": "Deaf users rely on sign-language interpreters, captions, transcripts, and visual alerts...",
  "digitalChallenges": "Videos without captions, audio alerts without visual equivalents...",
  "assistiveTechnologies": ["Captions and subtitles", "sign language interpretation tools", "visual alert systems"],
  "designConsiderations": "Never rely on audio alone. Every alert, confirmation, and notification needs a persistent visual equivalent...",
  "aiPrompt": "You are designing and building a digital product for Deaf users...",
  "clinicalExamples": "Congenital deafness, acquired deafness, Deaf community identity",
  "aiPromptUrl": "https://fyvr.net/prompts.html#deaf"
}
```

---

## Print Layout

Each card page includes a **print-ready foldable layout** optimized for letter paper (8.5" × 11", portrait):

- **Front panel** — category, title, persona name, backstory, condition description, and related cards
- **Back panel** — digital challenges, assistive technologies, design considerations, and the AI prompt URL

To print: open any card page, click **Print this card**, and print at 100% scale with default margins. Fold the right panel behind the left to create a double-sided card.

---

## Accessibility

This application is built to meet **WCAG 2.2 Level AA**. Key implementation details:

- Skip navigation link to `#main-content`
- `lang="en"` declared on all pages
- Semantic landmark regions: `<header>`, `<main>`, `<nav>`, `<article>`, `<aside>`, `<footer>`
- Logical heading hierarchy (`h1` → `h2` → `h3`) on every page
- All sections have `aria-labelledby` pointing to a visible heading
- Minimum color contrast ratio of 11:1 (WCAG requires 4.5:1)
- All interactive elements meet the 24×24px minimum touch target size (WCAG 2.5.8)
- External links include `rel="noopener noreferrer"` and an `aria-label` noting they open in a new tab
- No mouse-only event handlers; all interactions are keyboard accessible

---

## License

<!-- Add your license here -->
