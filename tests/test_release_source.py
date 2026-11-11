import unittest
import tempfile
from pathlib import Path
from unittest.mock import patch
from urllib.parse import urlparse
from antigravity_installer.release_source import version_from_url, ALLOWED_HOSTS
from antigravity_installer.installer import installed_versions

class ReleaseSourceTests(unittest.TestCase):
    def test_app_version(self):
        self.assertEqual(version_from_url("https://storage.googleapis.com/x/2.29.0-123/linux-x64/Antigravity.tar.gz"), "2.29.0")
    def test_ide_version(self):
        self.assertEqual(version_from_url("https://edgedl.me.gvt1.com/x/2.6.0-123/linux-x64/Antigravity%20IDE.tar.gz"), "2.6.0")
    def test_unknown_version(self):
        self.assertEqual(version_from_url("https://example.com/file.tar.gz"), "unknown")
    def test_version_detection_never_executes_gui_binaries(self):
        with tempfile.TemporaryDirectory() as tmp:
            paths = {}
            for product in ("app", "ide"):
                path = Path(tmp) / product
                path.write_text("fake executable")
                paths[product] = path
            with patch("antigravity_installer.installer._exe", side_effect=lambda p: paths[p]):
                with patch("antigravity_installer.installer._state", return_value={"app": {"version": "1.2.3"}}):
                    with patch("antigravity_installer.installer.subprocess.run") as run:
                        versions = installed_versions()
                    run.assert_not_called()
            self.assertEqual(versions["app"], "1.2.3")
            self.assertEqual(versions["ide"], "Desconocida")

    def test_host_allowlist(self):
        self.assertIn(urlparse("https://storage.googleapis.com/a").hostname, ALLOWED_HOSTS)
        self.assertNotIn(urlparse("https://storage.googleapis.com.attacker.invalid/a").hostname, ALLOWED_HOSTS)

if __name__ == "__main__":
    unittest.main()
