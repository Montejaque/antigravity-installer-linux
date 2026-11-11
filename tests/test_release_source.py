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
            self.assertEqual(versions["ide"], "Instalada (versión no detectada)")

    def test_reads_version_from_asar_package_metadata(self):
        import json, struct
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp); resources=root/"resources"; resources.mkdir()
            package=json.dumps({"name":"antigravity","version":"9.8.7"}).encode()
            header={"files":{"package.json":{"size":len(package),"offset":"0"}}}
            raw=json.dumps(header).encode(); padded=raw+b"\\0"*((4-len(raw)%4)%4)
            pickle=struct.pack("<I",len(raw))+padded
            archive=resources/"app.asar"
            archive.write_bytes(struct.pack("<II",4,len(pickle))+pickle+package)
            exe=root/"Antigravity"; exe.write_text("fake")
            with patch("antigravity_installer.installer._exe",return_value=exe):
                with patch("antigravity_installer.installer._state",return_value={}):
                    self.assertEqual(installed_versions()["app"],"9.8.7")

    def test_host_allowlist(self):
        self.assertIn(urlparse("https://storage.googleapis.com/a").hostname, ALLOWED_HOSTS)
        self.assertNotIn(urlparse("https://storage.googleapis.com.attacker.invalid/a").hostname, ALLOWED_HOSTS)

if __name__ == "__main__":
    unittest.main()
