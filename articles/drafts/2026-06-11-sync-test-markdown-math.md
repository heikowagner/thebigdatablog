---
categories:
- Meta
date: 2026-06-11
slug: sync-test-markdown-math
status: draft
tags:
- test
title: '[SYNC TEST] Markdown & Math Rendering Test'
wp_id: 4831
wp_modified: '2026-06-11T18:54:06'
---

> **Hinweis:** Dies ist ein automatisch erstellter Test-Entwurf zur Prüfung des WordPress-Markdown-Sync. Kann nach dem Test wieder gelöscht werden. *(v2 — math + code fix)*

## Text-Formatierung

**Fett**, *kursiv*, `code`, ~~durchgestrichen~~.

Aufzählung:
- Punkt 1
- Punkt 2
  - Unterpunkt

Nummeriert:
1. Erster
2. Zweiter

## Code-Block

```python
import numpy as np

x = np.linspace(0, 2 * np.pi, 100)
y = np.sin(x)
print(y[:5])
```

## Tabelle

| Methode       | Komplexität | Genauigkeit |
|---------------|-------------|-------------|
| Kernel-Dichte | $O(n^2)$    | hoch        |
| FFT-Methode   | $O(n \log n)$ | sehr hoch |

## Inline-Mathematik

Die Normalverteilung hat die Dichtefunktion $f(x) = \frac{1}{\sigma\sqrt{2\pi}} e^{-\frac{(x-\mu)^2}{2\sigma^2}}$.

## Block-Mathematik

Die Fourier-Transformation:

$$
\hat{f}(\xi) = \int_{-\infty}^{\infty} f(x)\, e^{-2\pi i x \xi}\, dx
$$

Das Gauß-Integral:

$$
\int_{-\infty}^{\infty} e^{-x^2}\, dx = \sqrt{\pi}
$$