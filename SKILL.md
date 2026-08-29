---
name: visual-sensemaker
description: Transform text, notes, tables, or structured data into clear, accurate, editable visual explanations. Use when a user asks to visualize, diagram, map, compare, summarize visually, or turn information into a flowchart, timeline, hierarchy, concept map, comparison, or basic data chart. Do not use for photo editing, decorative artwork, CAD, or specialized plots that require domain-specific conventions.
---

# Visual Sensemaker

Turn information into a visual that makes its structure easier to understand without changing its meaning.

## Workflow

1. Identify the audience, the single message the visual should communicate, and the source material. Infer low-risk presentation preferences; ask only when missing information would change the meaning.
2. Separate source facts from interpretation. Preserve labels, quantities, units, ordering, uncertainty, and attribution. Never invent content to fill visual space.
3. Read [references/visual-routing.md](references/visual-routing.md) and select one primary visual structure. Use a small multi-panel composition only when the content contains genuinely different structures.
4. Choose the deliverable:
   - Use SVG by default for static, editable visuals.
   - Use a self-contained HTML file when interaction materially improves understanding.
   - Use Mermaid only when the user prioritizes text-based maintenance or Markdown embedding over precise layout.
   - Add PNG or PDF only when requested or when the destination requires it; keep the editable source.
5. Read [references/design-system.md](references/design-system.md) when producing SVG or HTML. Build a clear hierarchy before adding decoration.
6. Read [references/quality-checks.md](references/quality-checks.md) before delivery. If the output is SVG, run `python scripts/check_svg.py <file.svg>` from this skill directory.
7. Render or open the result with an available visual inspection tool. Check the actual artifact, not only its source. Fix clipping, overlap, illegible text, broken references, misleading encodings, and weak hierarchy before delivery.

## Output Contract

Deliver the visual source and a rendered preview when the host supports one. Briefly state:

- the selected visual structure and why it fits;
- any consequential assumptions or transformations;
- the files produced and which one remains editable;
- any check that could not be completed.

Keep intermediate drafts out of the final deliverables unless the user asks for them.

## Non-negotiable Constraints

- Accuracy outranks visual drama.
- Do not imply unsupported causality, certainty, scale, or chronology.
- Keep quantitative axes, units, baselines, and uncertainty explicit.
- Use color as a secondary cue, never the only cue.
- Prefer a smaller readable visual over a dense poster.
- Do not embed remote fonts, scripts, images, or tracking resources in a self-contained deliverable.
