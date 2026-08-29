# Contributing

Thank you for helping make Visual Explainer more accurate and useful.

## Good contributions

- a realistic input that exposes a routing or layout failure;
- a narrow correction to a documented visual rule;
- an accessibility or portability improvement;
- a deterministic validation check with a focused test;
- an example that demonstrates a distinct information structure.

Avoid adding templates or universal rules based on a single aesthetic preference. New behavior should improve meaning, reliability, or portability for a clear class of requests.

## Before opening a pull request

Run:

```bash
python scripts/check_svg.py examples/*.svg
python -m unittest discover -s tests -v
```

Render every added or changed visual and inspect it at its intended display size. In the pull request, describe the input, expected outcome, verification performed, and any remaining limitation.
