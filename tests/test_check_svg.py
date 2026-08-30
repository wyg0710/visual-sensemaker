from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("check_svg", ROOT / "scripts" / "check_svg.py")
assert SPEC and SPEC.loader
CHECK_SVG = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = CHECK_SVG
SPEC.loader.exec_module(CHECK_SVG)


class CheckSvgTests(unittest.TestCase):
    def write_svg(self, content: str) -> Path:
        temporary = tempfile.NamedTemporaryFile(suffix=".svg", delete=False)
        temporary.write(content.encode("utf-8"))
        temporary.close()
        self.addCleanup(Path(temporary.name).unlink, missing_ok=True)
        return Path(temporary.name)

    def test_repository_svgs_have_no_errors(self) -> None:
        paths = sorted((ROOT / "examples").glob("*.svg")) + sorted((ROOT / "assets").glob("*.svg"))
        self.assertTrue(paths, "No repository SVG files were found")
        for path in paths:
            with self.subTest(path=path.relative_to(ROOT)):
                findings = CHECK_SVG.check_svg(path)
                self.assertEqual([], [finding for finding in findings if finding.level == "error"])

    def test_expand_paths_supports_globs(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "b.svg").write_text("<svg/>", encoding="utf-8")
            (root / "a.svg").write_text("<svg/>", encoding="utf-8")
            paths = CHECK_SVG.expand_paths([str(root / "*.svg")])
            self.assertEqual(["a.svg", "b.svg"], [path.name for path in paths])

    def test_missing_viewbox_is_an_error(self) -> None:
        path = self.write_svg(
            '<svg xmlns="http://www.w3.org/2000/svg"><title>Example</title><desc>Example</desc></svg>'
        )
        codes = {finding.code for finding in CHECK_SVG.check_svg(path)}
        self.assertIn("viewbox", codes)

    def test_duplicate_id_is_an_error(self) -> None:
        path = self.write_svg(
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10">'
            '<title>Example</title><desc>Example</desc><g id="same"/><g id="same"/></svg>'
        )
        codes = {finding.code for finding in CHECK_SVG.check_svg(path)}
        self.assertIn("duplicate-id", codes)

    def test_remote_resource_is_an_error(self) -> None:
        path = self.write_svg(
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 10 10">'
            '<title>Example</title><desc>Example</desc><image href="https://example.com/a.png"/></svg>'
        )
        codes = {finding.code for finding in CHECK_SVG.check_svg(path)}
        self.assertIn("remote-resource", codes)


if __name__ == "__main__":
    unittest.main()
