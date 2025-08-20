---

marp: true
title: "Product Documentation — Acme Cloud SDK"
author: "Technical Writer"
theme: fintech-docs
paginate: true
footer: "Page \$current / \$total — Acme Cloud SDK"
math: mathjax
size: 16:9
----------

<!--
Custom theme: Define once, reuse in version control. The slides below use this theme via `theme: fintech-docs`.
-->

<style>
/* @theme fintech-docs */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&display=swap');
:root {
  --color-primary: #0B5FFF;
  --color-accent: #07B39B;
  --bg-top: #0b1020;
  --bg-bottom: #111833;
  --fg: #E8EEFC;
}
section {
  font-family: 'Inter', system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, 'Helvetica Neue', Arial, sans-serif;
  color: var(--fg);
  background: linear-gradient(180deg, var(--bg-top) 0%, var(--bg-bottom) 100%);
}
section h1, section h2, section h3 { color: var(--color-primary); }
section a { color: var(--color-accent); text-decoration: none; border-bottom: 1px dotted var(--color-accent); }
section a:hover { opacity: .85; }
section.lead h1 { font-size: 64px; letter-spacing: .5px; }
section.lead p { font-size: 28px; }
pre, code { font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, "Liberation Mono", monospace; font-size: .95em; }
code { background: rgba(255,255,255,.06); padding: .15em .35em; border-radius: .4rem; }
footer { color: rgba(232,238,252,.75); }
/* Slide-level utility classes used via Marp directives */
section.compact { font-size: 26px; line-height: 1.35; }
section.callout { border-left: .5rem solid var(--color-accent); padding-left: 1rem; }
section.invert { filter: invert(0); }
</style>

<!-- _class: lead -->

# Acme Cloud SDK — Product Documentation

**Purpose:** Developer-focused overview, install, config, and API usage.

**Contact:** [23f2004422@ds.study.iitm.ac.in](mailto:23f2004422@ds.study.iitm.ac.in)

---

<!-- _class: compact -->

## Agenda

1. Overview & versioning workflow
2. Install & configure
3. API usage patterns
4. Error handling & observability
5. Performance & complexity notes (with math)
6. Packaging docs for PDF/HTML/Slides

---

## Maintainability in Version Control

* **Single source of truth:** Keep `docs/` with Marp Markdown (`.md`) next to source.
* **Build matrix:** Generate **HTML**, **PDF**, and **slides** via Marp CLI.
* **PR previews:** Use CI (e.g., GitHub Actions) to render and publish on push.

```bash
# Local authoring & preview
yarn global add @marp-team/marp-cli  # or: npm i -g @marp-team/marp-cli
marp docs/product.md --html --allow-local-files --watch

# Export for distribution
marp docs/product.md --pdf
marp docs/product.md --pptx
```

---

## Installation

```bash
# Node 18+
npm install @acme/cloud-sdk

# or with Yarn
yarn add @acme/cloud-sdk
```

**Initialize:**

```js
import { Acme } from '@acme/cloud-sdk';

const client = new Acme({
  apiKey: process.env.ACME_API_KEY,
  region: 'ap-south-1',
  timeoutMs: 10000,
});
```

---

## Configuration

Use environment variables for secrets; provide sane defaults.

```bash
export ACME_API_KEY="..."
export ACME_REGION="ap-south-1"
export ACME_LOG_LEVEL="info"
```

```ts
// config.ts
export const cfg = {
  apiKey: process.env.ACME_API_KEY ?? '',
  region: process.env.ACME_REGION ?? 'us-east-1',
  logLevel: (process.env.ACME_LOG_LEVEL ?? 'warn') as 'debug'|'info'|'warn'|'error',
};
```

---

<!-- _class: callout -->

## API Usage — Example

```ts
import { Acme } from '@acme/cloud-sdk';
import { cfg } from './config';

const acme = new Acme({ apiKey: cfg.apiKey, region: cfg.region });

async function createInvoice(input) {
  const res = await acme.invoice.create({
    customerId: input.customerId,
    amount: input.amount,
    currency: 'INR',
  });
  return res.id;
}
```

**Errors:**

```ts
try {
  await createInvoice({ customerId: 'CUST_123', amount: 1299 });
} catch (e) {
  acme.logger.error('Invoice failed', { err: e });
}
```

---

<!--
Background image slide using Marp directives
-->

<!-- _backgroundImage: url('https://images.unsplash.com/photo-1551281044-8f5418240f2b?auto=format&fit=crop&w=1600&q=80') -->

<!-- _backgroundSize: cover -->

<!-- _color: #ffffff -->

# Architecture at a Glance

* Multi-tenant, region-aware API
* SDK retries + backoff
* Structured logs & metrics

> Use the diagram as a mental model when onboarding new contributors.

---

## Mathematical Notes — Algorithmic Complexity

We target linearithmic performance for bulk operations:

Inline: `O(n \log n)`

Block:

$$
T(n) = a\,n\log n + b\,n + c
$$

For batched pagination with page size \$k\$ across \$n\$ items:

$$
\text{Requests} = \left\lceil \frac{n}{k} \right\rceil
$$

---

## Marp Directives Showcase (Custom Styling)

* `<!-- _class: compact -->` to densify a slide
* `<!-- _backgroundImage: url(...) -->` for hero visuals
* `<!-- _color: #fff -->` to improve contrast over images
* Global `paginate: true` adds **page numbers**

```md
---
<!-- _class: compact -->
Your dense content goes here.
```

---

## Export & Automation

* **HTML**: `marp docs/product.md --html`
* **PDF**: `marp docs/product.md --pdf`
* **Slides**: `marp docs/product.md`

**CI Example (GitHub Actions):**

```yaml
name: build-docs
on: [push]
jobs:
  render:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - run: npm i -g @marp-team/marp-cli
      - run: marp docs/product.md --html --pdf --allow-local-files --output dist/
      - uses: actions/upload-pages-artifact@v3
        with: { path: dist }
      - uses: actions/deploy-pages@v4
```

---

## Appendix

* Repo structure

  * `docs/product.md` (this Marp file)
  * `.github/workflows/build-docs.yml` (CI)
  * `assets/` (images, diagrams)
* Changelog follows [Keep a Changelog](https://keepachangelog.com/) format
* SemVer: `MAJOR.MINOR.PATCH`
