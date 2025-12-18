# JavaScript in SCARF

**Philosophy**: Keep it simple.
We are **not** building a Single Page Application (SPA). We don't need React, Vue, or Angular.
The site is static HTML. JavaScript is only used for **progressive enhancement**.

## ⚡ Key Features

### 1. Table of Contents (TOC) Highlighting
As the user scrolls, the active section in the sidebar should light up.

```javascript
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      document.querySelectorAll('.toc-link').forEach(link => link.classList.remove('active'));
      const id = entry.target.getAttribute('id');
      document.querySelector(`.toc-link[href="#${id}"]`).classList.add('active');
    }
  });
});

document.querySelectorAll('section').forEach((section) => {
  observer.observe(section);
});
```

### 2. Dynamic Q&A (The "Chat" Feature)
Even though the site is static, we want users to "ask questions."
How? We use a **Serverless Function** or a simple API call back to our main backend (if running) or a pre-generated Q&A index.

**Approach A: Pre-generated Q&A**
We generate 50 common questions during the build phase and store them in `qa_index.json`.
The JS searches this JSON file. (Zero backend required at runtime!)

**Approach B: Live API**
```javascript
async function askQuestion(query) {
  const response = await fetch('https://api.readify.com/ask', {
    method: 'POST',
    body: JSON.stringify({ q: query })
  });
  const data = await response.json();
  displayAnswer(data.answer);
}
```

### 3. MathJax / KaTeX
Research papers have math. We use **MathJax** to render LaTeX equations in the browser.

```html
<script src="https://polyfill.io/v3/polyfill.min.js?features=es6"></script>
<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
```

## 📦 Bundling?
No. We write vanilla ES6 JavaScript.
*   No Webpack.
*   No Babel.
*   Modern browsers support modules (`<script type="module">`) and ES6 features natively.
This keeps the project lightweight and easy to hack on.
