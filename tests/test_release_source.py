import unittest
from urllib.parse import urlparse
from antigravity_installer.release_source import version_from_url, ALLOWED_HOSTS

class ReleaseSourceTests(unittest.TestCase):
    def test_app_version(self):
        self.assertEqual(version_from_url("https://storage.googleapis.com/x/2.29.0-123/linux-x64/Antigravity.tar.gz"), "2.29.0")
    def test_ide_version(self):
        self.assertEqual(version_from_url("https://edgedl.me.gvt1.com/x/2.6.0-123/linux-x64/Antigravity%20IDE.tar.gz"), "2.6.0")
    def test_unknown_version(self):
        self.assertEqual(version_from_url("https://example.com/file.tar.gz"), "unknown")
    def test_host_allowlist(self):
        self.assertIn(urlparse("https://storage.googleapis.com/a").hostname, ALLOWED_HOSTS)
        self.assertNotIn(urlparse("https://storage.googleapis.com.attacker.invalid/a").hostname, ALLOWED_HOSTS)

if __name__ == "__main__":
    unittest.main()
