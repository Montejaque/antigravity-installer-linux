#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
mkdir -p .tools dist
APPIMAGETOOL="$ROOT/.tools/appimagetool"
if [[ ! -x "$APPIMAGETOOL" ]]; then
  curl -fL --retry 3 "https://github.com/AppImage/AppImageKit/releases/download/continuous/appimagetool-x86_64.AppImage" -o "$APPIMAGETOOL"
  chmod +x "$APPIMAGETOOL"
fi
rm -rf build AppDir
python3 -m PyInstaller --noconfirm --clean --onedir --windowed --name antigravity-installer --collect-all tkinter --hidden-import _tkinter --add-data "assets:assets" --add-data "docs/GUIA_USUARIO.md:docs" launcher.py
mkdir -p AppDir/usr/bin AppDir/usr/share/applications AppDir/usr/share/icons/hicolor/scalable/apps
cp -a dist/antigravity-installer/. AppDir/usr/bin/
cp assets/antigravity-installer.svg AppDir/usr/share/icons/hicolor/scalable/apps/antigravity-installer.svg
cat > AppDir/AppRun <<'EOF'
#!/bin/sh
set -eu
HERE="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
exec "$HERE/usr/bin/antigravity-installer" "$@"
EOF
chmod +x AppDir/AppRun
cat > AppDir/antigravity-installer.desktop <<'EOF'
[Desktop Entry]
Type=Application
Name=Antigravity Installer
Comment=Instalador de Google Antigravity App e IDE para Linux
Exec=AppRun
Icon=antigravity-installer
Terminal=false
Categories=Development;Utility;
EOF
cp AppDir/antigravity-installer.desktop AppDir/usr/share/applications/
ln -sf usr/share/icons/hicolor/scalable/apps/antigravity-installer.svg AppDir/antigravity-installer.svg
APPIMAGE_EXTRACT_AND_RUN=1 "$APPIMAGETOOL" AppDir dist/Antigravity-Installer-x86_64.AppImage
chmod +x dist/Antigravity-Installer-x86_64.AppImage
file dist/Antigravity-Installer-x86_64.AppImage
test -s dist/Antigravity-Installer-x86_64.AppImage
