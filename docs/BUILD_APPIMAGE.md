# Construcción de AppImage y PDF

El proyecto se compila en GitHub Actions dentro de Ubuntu 20.04 x86_64. No es necesario instalar herramientas de compilación en el equipo del usuario.

## Construcción local
En Ubuntu 20.04 x86_64 instala Python 3, Tkinter, PyInstaller, ReportLab, curl, file, libfuse2, binutils, patchelf y tar. Después ejecuta:

```bash
python3 -m pip install "pyinstaller==6.11.1" "reportlab==4.2.5"
bash scripts/build-appimage.sh
python3 scripts/build-help-pdf.py
```

## Publicación automatizada
El workflow `.github/workflows/ci.yml` ejecuta pruebas y genera la AppImage y la guía PDF. Al crear una etiqueta `v*`, ambos ficheros se adjuntan automáticamente a una GitHub Release. La publicación solo se considera correcta cuando el workflow termina en verde y ambos archivos aparecen en Assets.
