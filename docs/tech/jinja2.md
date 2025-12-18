# Jinja2: Static Site Generation

**Why Jinja2?**
SCARF generates **static websites**. We don't want to run a Python backend to serve the final paper. We want a folder of HTML/CSS/JS that can be hosted anywhere (GitHub Pages, Netlify, S3).
Jinja2 is the industry-standard template engine for Python.

## 🎨 How it Works

We define a **Template** (`base.html`, `paper.html`) and pass **Context** (variables) to it.

### The Template (`paper.html`)

```html
{% extends "base.html" %}

{% block content %}
  <h1 class="paper-title">{{ metadata.title }}</h1>
  
  <div class="authors">
    {% for author in metadata.authors %}
      <span class="author">{{ author }}</span>
    {% endfor %}
  </div>

  <div class="sections">
    {% for section in sections %}
      <section id="sec-{{ loop.index }}">
        <h2>{{ section.heading }}</h2>
        <div class="content">
          {{ section.content | safe }}
        </div>
        <div class="ai-summary">
          <strong>TL;DR:</strong> {{ section.summary }}
        </div>
      </section>
    {% endfor %}
  </div>
{% endblock %}
```

### The Rendering Logic

```python
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader('templates'))
template = env.get_template('paper.html')

html_output = template.render(
    metadata=paper_metadata,
    sections=parsed_sections
)

with open('output/index.html', 'w') as f:
    f.write(html_output)
```

## 🧩 Advanced Features Used

### 1. Filters
We use custom filters to format data.
*   `{{ date | date_format }}`
*   `{{ text | markdown_to_html }}`

### 2. Macros
Reusable components (like a "Question Card" or "Citation Tooltip").

```html
{% macro question_card(q, a) %}
<div class="qa-card">
  <p class="q">Q: {{ q }}</p>
  <p class="a">A: {{ a }}</p>
</div>
{% endmacro %}
```

### 3. Inheritance
`base.html` contains the `<html>`, `<head>`, scripts, and navbar. `paper.html` only focuses on the content. This ensures every generated site looks consistent.

## 🌐 Why Static?
*   **Speed**: Pure HTML loads instantly.
*   **Security**: No backend to hack.
*   **Cost**: Free hosting on GitHub Pages.
*   **Portability**: The user can download the zip and read it offline.
