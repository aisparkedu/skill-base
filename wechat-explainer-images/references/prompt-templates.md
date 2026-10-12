# Prompt templates

Use these as structures. Replace every bracketed field with article-specific content.

## Shared style block

```text
Create a polished Chinese editorial infographic for a WeChat article, portrait 3:4. Warm cream technical-paper background, very subtle pale-blue blueprint grid, engineering-blue primary, warm-orange emphasis, mint-green success accents, dark-navy rounded outlines. Premium flat vector editorial illustration with restrained paper-cut shadows, generous margins, crisp hierarchy, high legibility on a phone, no photorealism, no watermark, no logo, no QR code, no fake app interface.

Use the supplied image only as a STYLE REFERENCE for palette, spacing, line language, paper depth, and editorial finish. Do not copy its words, brands, logos, products, icons, character identity, or exact composition.
```

## Cover template

```text
[SHARED STYLE BLOCK]

This is the main cover. Build one dramatic focal scene: [FOCAL SCENE].

Render only this exact Chinese copy:
- Main headline: “[HEADLINE]”
- Supporting line: “[SUPPORTING LINE]”
- Small hook labels: “[HOOK 1]” / “[HOOK 2]” / “[HOOK 3]”

Make the headline the strongest text. Keep hook labels secondary. The image must create curiosity at thumbnail size while staying credible and instructional.
```

## Explainer template

```text
[SHARED STYLE BLOCK]

This is an inline explainer card about [SECTION TOPIC].

Render only this exact Chinese copy:
- Eyebrow: “[EYEBROW]”
- Title: “[TITLE]”
- Subtitle: “[SUBTITLE]”
- Diagram labels in reading order: “[LABEL 1]”, “[LABEL 2]”, “[LABEL 3]”[, ...]
- Bottom takeaway: “[TAKEAWAY]”

Central visual: [CONCRETE VISUAL METAPHOR OR DIAGRAM]. Make the reading order unmistakable. Every object must support the message. Do not add extra prose or invented labels.
```

## Text repair template

```text
Keep the composition, colors, objects, spacing, and style unchanged. Correct only the following visible Chinese text:
- Replace “[WRONG]” with “[RIGHT]”.

Do not change any other text. Preserve the portrait 3:4 composition and all margins.
```

## Prompt-writing cautions

- Put exact copy in a separate list and say “render only this exact Chinese copy.”
- Prefer short labels. If a sentence is essential, place it only in the subtitle or takeaway.
- Describe the central diagram concretely; do not rely on vague phrases such as “technology feel.”
- Avoid asking the model to draw real product interfaces. Use screenshots from the article for proof instead.

