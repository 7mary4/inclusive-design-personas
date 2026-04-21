#!/usr/bin/env python3
"""
Preview server for Inclusive Design Persona Cards.
Mirrors the PHP application logic using Python's http.server.
For preview/development only — deploy the .php files on a PHP host.
"""
import json
import re
import html
from http.server import HTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, parse_qs

BASE_DIR = Path(__file__).parent
DATA_FILE = BASE_DIR / "data" / "cards.json"

with open(DATA_FILE, encoding="utf-8") as f:
    ALL_CARDS = json.load(f)

CATEGORY_ORDER = [
    "Auditory", "Cognitive", "Intersectional", "Mental Health",
    "Neurodiversity", "Physical", "Speech", "Visual"
]

def e(text):
    """HTML-escape a value."""
    return html.escape(str(text) if text is not None else "")

def cat_id(name):
    return re.sub(r"[^a-z0-9]+", "-", name.lower())

def card_by_id(card_id):
    for c in ALL_CARDS:
        if c["id"] == card_id:
            return c
    return None

def related_cards(card):
    return [c for c in ALL_CARDS if c["category"] == card["category"] and c["id"] != card["id"]]

# ── HTML fragments ─────────────────────────────────────────────────────────────

def page_shell(title, description, body_html, *, header_link=False):
    header_content = (
        f'<p><a href="/">Inclusive Design Persona Cards</a></p>'
        if header_link else
        '<h1>Inclusive Design Persona Cards</h1>'
        '<p class="tagline">40 personas. Every kind of user. Better products for everyone.</p>'
    )
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{e(title)}</title>
  <meta name="description" content="{e(description)}">
  <link rel="stylesheet" href="/css/style.css">
</head>
<body>
  <a class="skip-link" href="#main-content">Skip to main content</a>
  <header class="site-header" role="banner">
    <div class="header-inner">{header_content}</div>
  </header>
  <main id="main-content">
{body_html}
  </main>
  <footer class="site-footer" role="contentinfo">
    <p>Inclusive Design Persona Cards &mdash; Helping teams build accessible, human-centered products.</p>
  </footer>
</body>
</html>"""

def render_index():
    categories = {}
    for card in ALL_CARDS:
        categories.setdefault(card["category"], []).append(card)

    sections = []
    for cat_name in CATEGORY_ORDER:
        if cat_name not in categories:
            continue
        cid = cat_id(cat_name)
        card_items = []
        for card in categories[cat_name]:
            card_url = f"/card?id={card['id']}"
            card_items.append(f"""
              <li>
                <article class="card-preview" aria-labelledby="card-title-{card['id']}">
                  <header class="card-preview__header">
                    <span class="card-preview__category" aria-label="Category: {e(cat_name)}">{e(cat_name)}</span>
                    <h3 id="card-title-{card['id']}">{e(card['title'])}</h3>
                    <p class="card-preview__name">{e(card['name'])}</p>
                  </header>
                  <div class="card-preview__body">
                    <p class="card-preview__backstory">{e(card['backstory'])}</p>
                  </div>
                  <footer class="card-preview__footer">
                    <a class="card-link" href="{e(card_url)}">
                      View {e(card['title'])} card
                      <span class="visually-hidden">for {e(card['name'])}</span>
                    </a>
                  </footer>
                </article>
              </li>""")

        sections.append(f"""
    <section class="category-section" aria-labelledby="cat-{cid}">
      <h2 id="cat-{cid}">{e(cat_name)}</h2>
      <ul class="cards-grid" role="list">{''.join(card_items)}
      </ul>
    </section>""")

    body = """    <section class="page-intro" aria-labelledby="intro-heading">
      <h2 id="intro-heading" class="visually-hidden">About These Cards</h2>
      <p>
        Great products are built for everyone&mdash;not just the majority. These persona cards represent
        real experiences of people with disabilities, chronic conditions, situational impairments, and
        cognitive differences. By designing with these personas in mind from the start, your team can
        uncover barriers early, build empathy across disciplines, and ship products that work for the
        full spectrum of human diversity. Use them in design critiques, sprint planning, accessibility
        audits, and AI development to keep diverse users at the center of every decision.
      </p>
    </section>""" + "".join(sections)

    return page_shell(
        "Inclusive Design Persona Cards",
        "A collection of 40 inclusive design persona cards representing diverse users.",
        body,
        header_link=False
    )

def render_card(card_id):
    card = card_by_id(card_id)
    if card is None:
        return None

    rel = related_cards(card)
    cid = cat_id(card["category"])
    techs = card["assistiveTechnologies"]

    # No whitespace between <li> elements — prevents spaces before CSS-generated commas
    tech_items = "".join(f"<li>{e(t.strip())}</li>" for t in techs)

    # Related cards section (inside card article)
    related_section = ""
    if rel:
        links = "".join(
            f'<li><a href="/card?id={r["id"]}">{e(r["title"])}'
            f'<span class="visually-hidden"> &mdash; {e(r["name"])}</span></a></li>'
            for r in rel
        )
        related_section = f"""
      <section class="card-section related-cards-section" aria-labelledby="related-heading">
        <h2 id="related-heading">Related {e(card['category'])} Cards</h2>
        <ul class="related-cards-list" role="list">{links}</ul>
      </section>"""

    # Print front: related card titles as plain text
    print_related = ""
    if rel:
        titles = ", ".join(e(r["title"]) for r in rel)
        print_related = f'<div class="print-related"><strong>Related:</strong> {titles}</div>'

    # AI prompt aside (screen only)
    ai_section = ""
    if card.get("aiPromptUrl"):
        copy_svg = '<svg aria-hidden="true" focusable="false" width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"></rect><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"></path></svg>'
        prompt_block = ""
        if card.get("aiPrompt"):
            prompt_block = f"""
      <div class="ai-prompt-wrapper">
        <div class="ai-prompt-toolbar">
          <span class="ai-prompt-label">Prompt</span>
          <button class="copy-prompt-btn" type="button" onclick="copyPrompt(this)" aria-label="Copy AI prompt text to clipboard">
            {copy_svg} Copy prompt
          </button>
        </div>
        <pre class="ai-prompt-code"><code>{e(card['aiPrompt'])}</code></pre>
      </div>"""
        ai_section = f"""
    <aside class="ai-prompt-section no-print" aria-labelledby="ai-prompt-heading">
      <h2 id="ai-prompt-heading">AI Development Prompt</h2>
      <p>Incorporate {e(card['title'])} into your AI development with this prompt.</p>{prompt_block}
      <a class="ai-prompt-link"
         href="{e(card['aiPromptUrl'])}"
         target="_blank"
         rel="noopener noreferrer"
         aria-label="Open AI prompt for {e(card['title'])} (opens in new tab)">
        Use the {e(card['title'])} AI Prompt &rarr;
      </a>
    </aside>"""

    clinical = ""
    if card.get("clinicalExamples"):
        clinical = f"""
      <section class="card-section" aria-labelledby="section-clinical">
        <h2 id="section-clinical">Clinical Examples</h2>
        <p class="clinical-examples">{e(card['clinicalExamples'])}</p>
      </section>"""

    # Print-only card (front + back)
    print_tech_items = "\n".join(f"              <li>{e(t.strip())}</li>" for t in techs)
    print_ai = ""
    if card.get("aiPromptUrl"):
        print_ai = f"""
          <h3>AI Development Prompt</h3>
          <p>Incorporate {e(card['title'])} into your AI development with this prompt:</p>
          <p class="print-ai-url">{e(card['aiPromptUrl'])}</p>"""

    body = f"""
    <nav class="breadcrumb" aria-label="Breadcrumb">
      <ol>
        <li><a href="/">All Cards</a></li>
        <li><a href="/#cat-{cid}">{e(card['category'])}</a></li>
        <li><span aria-current="page">{e(card['title'])}</span></li>
      </ol>
    </nav>

    <button class="print-btn no-print" onclick="window.print()" type="button">
      <svg aria-hidden="true" focusable="false" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <polyline points="6 9 6 2 18 2 18 9"></polyline>
        <path d="M6 18H4a2 2 0 0 1-2-2v-5a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v5a2 2 0 0 1-2 2h-2"></path>
        <rect x="6" y="14" width="12" height="8"></rect>
      </svg>
      Print this card
    </button>

    <article class="card-detail no-print" aria-labelledby="card-heading">
      <header class="card-detail__header">
        <span class="card-detail__category">{e(card['category'])}</span>
        <h1 id="card-heading">{e(card['title'])}</h1>
        <p class="card-detail__persona-name">Persona: {e(card['name'])}</p>
        <p class="card-detail__backstory">{e(card['backstory'])}</p>
      </header>

      <section class="card-section" aria-labelledby="section-condition">
        <h2 id="section-condition">About This Condition</h2>
        <p>{e(card['conditionDescription'])}</p>
      </section>

      <section class="card-section" aria-labelledby="section-challenges">
        <h2 id="section-challenges">Digital Challenges</h2>
        <p>{e(card['digitalChallenges'])}</p>
      </section>

      <section class="card-section" aria-labelledby="section-assistive">
        <h2 id="section-assistive">Assistive Technologies</h2>
        <ul class="assistive-tech-list">{tech_items}</ul>
      </section>

      <section class="card-section" aria-labelledby="section-design">
        <h2 id="section-design">Design Considerations</h2>
        <p>{e(card['designConsiderations'])}</p>
      </section>
{clinical}
{related_section}
    </article>
{ai_section}

    <div class="print-only" role="presentation">
      <div class="print-card-wrapper">
        <div class="print-card-front">
          <span class="print-category">{e(card['category'])}</span>
          <h1>{e(card['title'])}</h1>
          <p class="print-name">{e(card['name'])}</p>
          <p class="print-backstory">{e(card['backstory'])}</p>
          <p class="print-condition">{e(card['conditionDescription'])}</p>
          {print_related}
        </div>
        <div class="print-card-back">
          <h3>Digital Challenges</h3>
          <p>{e(card['digitalChallenges'])}</p>
          <h3>Assistive Technologies</h3>
          <ul>
{print_tech_items}
          </ul>
          <h3>Design Considerations</h3>
          <p>{e(card['designConsiderations'])}</p>
{print_ai}
        </div>
      </div>
      <p class="print-fold-guide">&#9986; Fold right panel behind left panel to create a double-sided card</p>
    </div>
"""

    footer_html = f"""  <footer class="site-footer no-print" role="contentinfo">
    <p>
      <a href="/">← Back to all persona cards</a>
      &nbsp;&mdash;&nbsp;
      Inclusive Design Persona Cards
    </p>
  </footer>"""

    title = f"{card['title']} — Inclusive Design Persona Cards"
    desc = f"Inclusive design persona for {card['title']} ({card['category']}). Digital challenges, assistive technologies, and design considerations."

    copy_script = """  <script>
  function copyPrompt(btn) {
    var code = btn.closest('.ai-prompt-wrapper').querySelector('code');
    var original = btn.innerHTML;
    navigator.clipboard.writeText(code.textContent).then(function () {
      btn.textContent = 'Copied!';
      btn.setAttribute('aria-label', 'Copied to clipboard');
      setTimeout(function () {
        btn.innerHTML = original;
        btn.setAttribute('aria-label', 'Copy AI prompt text to clipboard');
      }, 2000);
    }, function () {
      btn.textContent = 'Copy failed';
      setTimeout(function () { btn.innerHTML = original; }, 2000);
    });
  }
  </script>"""

    page = page_shell(title, desc, body, header_link=True)
    # Inject custom footer and copy script
    page = page.replace(
        "  <footer",
        "  " + footer_html + "\n" + copy_script + "\n  <footer",
        1
    ).replace(
        "  <footer class=\"site-footer\" role=\"contentinfo\">\n    <p>Inclusive Design Persona Cards &mdash; Helping teams build accessible, human-centered products.</p>\n  </footer>",
        ""
    )
    return page


class Handler(BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        print(f"  {self.address_string()} → {format % args}")

    def send_html(self, content, status=200):
        encoded = content.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)

    def send_file(self, path, content_type):
        try:
            with open(path, "rb") as f:
                data = f.read()
            self.send_response(200)
            self.send_header("Content-Type", content_type)
            self.send_header("Content-Length", str(len(data)))
            self.end_headers()
            self.wfile.write(data)
        except FileNotFoundError:
            self.send_html("<h1>404</h1>", 404)

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path.rstrip("/") or "/"
        qs = parse_qs(parsed.query)

        if path in ("/", "/index.php"):
            self.send_html(render_index())

        elif path in ("/card", "/card.php"):
            card_id = int(qs.get("id", [0])[0])
            html_content = render_card(card_id)
            if html_content is None:
                self.send_html("<html><body><h1>Card Not Found</h1><p><a href='/'>Back to all cards</a></p></body></html>", 404)
            else:
                self.send_html(html_content)

        elif path.startswith("/css/"):
            css_path = BASE_DIR / path.lstrip("/")
            self.send_file(css_path, "text/css; charset=utf-8")

        elif path.startswith("/data/"):
            data_path = BASE_DIR / path.lstrip("/")
            self.send_file(data_path, "application/json; charset=utf-8")

        else:
            self.send_html("<html><body><h1>Not Found</h1><p><a href='/'>Home</a></p></body></html>", 404)


if __name__ == "__main__":
    port = 8765
    server = HTTPServer(("127.0.0.1", port), Handler)
    print(f"Preview server running at http://127.0.0.1:{port}/")
    print("Press Ctrl+C to stop.")
    server.serve_forever()
