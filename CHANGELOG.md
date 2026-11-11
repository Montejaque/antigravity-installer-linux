# Historial de cambios

## 1.1.4
- Corregida la lectura de cabeceras ASAR para detectar la versión real desde los metadatos de Electron.
- Se guarda también la versión en un archivo local de instalación para futuras comprobaciones.

## 1.1.3
- Detección de versión instalada desde los metadatos locales de Electron/ASAR sin ejecutar la aplicación.
- Si el paquete no contiene una versión legible, se identifica como instalada sin mostrar «Desconocida».
- El botón «Guía de ayuda» abre la guía incluida en la AppImage; se elimina la referencia a Releases.

## 1.1.2
- La interfaz identifica expresamente al desarrollador y a Punto Vuela Montejaque.
- Actualizada la guía de ayuda y los metadatos del PDF de la versión.

## 1.1.1
- Corregido el inicio involuntario de Antigravity App e IDE al abrir la AppImage.
- La detección de instalaciones ya no ejecuta los binarios gráficos; consulta únicamente el estado local.
- Eliminado el botón de acceso al repositorio de la interfaz.
- Añadida una prueba para garantizar que la detección de versiones no ejecuta las aplicaciones.

## 1.1.0
- Selección independiente de Antigravity App, Antigravity IDE o ambos.
- Detección de versiones instaladas y consulta de versiones publicadas.
- Instalación, actualización y desinstalación selectiva.
- Guía de ayuda y compilación automatizada mediante GitHub Actions.

## 1.0.0
- Primera versión del instalador gráfico para Linux.
