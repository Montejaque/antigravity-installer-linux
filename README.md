# Antigravity Installer for Linux

**Versión 1.1.4 · Punto Vuela Montejaque**

Instalador gráfico AppImage para Google Antigravity App y Antigravity IDE. Permite instalar, actualizar, comprobar versiones, reparar accesos y desinstalar cada componente por separado, sin permisos de administrador.

## Descargas
Consulta [Releases](https://github.com/Montejaque/antigravity-installer-linux/releases). Cada versión publicada incluirá:
- `Antigravity-Installer-x86_64.AppImage`
- `Guia-Ayuda-Antigravity.pdf`

La AppImage contiene el instalador, no los programas originales. Los paquetes se descargan en el momento de la instalación desde la página oficial de Google.

## Funciones
- Selección independiente de App, IDE o ambos.
- Detección de versiones instaladas y consulta de versiones publicadas.
- Instalación y actualización selectiva.
- Accesos directos del menú de aplicaciones.
- Desinstalación selectiva conservando perfiles y proyectos.
- Instalación en el perfil del usuario, sin sudo ni escritura en /usr.

## Compatibilidad
Linux x86_64. La AppImage se construye en Ubuntu 20.04 para mantener compatibilidad con sistemas con glibc 2.31. ARM64 no está incluido.

## Uso
Descarga la AppImage desde Releases, dale permiso con `chmod +x Antigravity-Installer-x86_64.AppImage` y ejecútala.

## Desarrollo
Consulta [Guía de ayuda](docs/GUIA_USUARIO.md), [Construcción](docs/BUILD_APPIMAGE.md) y [Seguridad](SECURITY.md). GitHub Actions ejecuta pruebas, genera AppImage y PDF y publica ambos archivos al crear una etiqueta v*.

## Contacto
**Francisco Javier Gallego Orellana · Punto Vuela Montejaque**  
Avenida Andalucía, 48 · 29360 Montejaque (Málaga)  
633 402 959 · montejaque@puntosvuela.es  
https://puntosvuela.es/centros/montejaque

Google y Antigravity son marcas de Google LLC. Proyecto independiente, no afiliado ni patrocinado por Google.
