# Design System

Use these defaults unless the user supplies a brand system or the destination imposes constraints.

## Canvas and Layout

- Default static canvas: `1200 x 800` with a matching SVG `viewBox`.
- Use an outer margin of at least 48 px and a consistent 8 px spacing grid.
- Establish reading order before styling. Prefer left-to-right or top-to-bottom flow.
- Align related objects to shared edges or centers. Use whitespace to separate groups.
- Keep connectors behind nodes and route them away from labels.

## Typography

- Use a portable system-font stack: `Inter, Segoe UI, Arial, sans-serif`.
- Recommended sizes on a 1200 x 800 canvas: title 32-40 px, section heading 20-24 px, body 15-18 px, annotation at least 13 px.
- Use no more than three type sizes and two weights unless the content requires more hierarchy.
- Keep text concise. Wrap deliberately; SVG text does not wrap automatically.

## Color

Default light palette:

| Role | Color |
|---|---|
| Canvas | `#F8FAFC` |
| Surface | `#FFFFFF` |
| Primary text | `#0F172A` |
| Secondary text | `#475569` |
| Border | `#CBD5E1` |
| Primary accent | `#2563EB` |
| Secondary accent | `#7C3AED` |
| Success | `#15803D` |
| Warning | `#B45309` |
| Danger | `#B91C1C` |

Do not depend on red-green contrast alone. Pair color with labels, shapes, patterns, or icons. Maintain readable text contrast against its background.

## SVG Construction

- Include a meaningful `<title>` and `<desc>` as the first children of the root SVG.
- Use a `viewBox`, semantic group IDs, and reusable definitions with unique IDs.
- Keep all content inside the viewBox. Avoid `foreignObject` unless HTML text wrapping is essential and the destination supports it.
- Do not embed remote assets. Prefer vector shapes and paths over raster images.
- Add `role="img"` and connect `aria-labelledby` to the title and description IDs.

## Visual Restraint

Use shadows, gradients, and rounded cards only when they clarify grouping or depth. Avoid decorative 3D effects, unnecessary icons, and rainbow palettes. The visual should still communicate when printed in grayscale.
