# Quality Checks

Review the artifact in this order.

## 1. Semantic Fidelity

- Every claim, number, label, and relationship is traceable to the input or explicitly marked as an assumption.
- Categories remain distinct; missing values are not silently converted to zero.
- Chronology, direction, and causality are not implied without support.
- Units, denominators, uncertainty, and sample context are retained when relevant.

## 2. Visual Encoding

- The selected visual matches the information structure.
- Length and position carry important quantitative comparisons before area, angle, or color.
- Bar charts normally start at zero. Any truncated quantitative axis is visible and justified.
- Legends are close to the data, and color is not the sole identifier.

## 3. Layout and Legibility

- Nothing is clipped, overlapping, or outside the canvas.
- Text remains readable at the intended display size.
- Reading order and grouping are immediately apparent.
- Connectors terminate clearly and do not cross labels.
- The title states the message rather than merely naming the topic.

## 4. Accessibility and Portability

- Text contrast is sufficient and the graphic remains interpretable without color.
- SVG includes title, description, and a stable viewBox.
- The editable source contains no remote dependency unless the user explicitly accepts one.
- The artifact opens successfully in the target environment.

## 5. Delivery

- Filenames are descriptive and use ASCII kebab-case unless the user requests otherwise.
- Only final artifacts are presented as deliverables.
- The handoff names the editable source and discloses any uncompleted check.
