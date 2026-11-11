# Guía de ayuda · Antigravity Installer para Linux

**Punto Vuela Montejaque · Versión 1.1.0 · Linux x86_64**

## 1. Qué hace
Instala y mantiene Google Antigravity App y Antigravity IDE desde una interfaz gráfica. La AppImage contiene el instalador, no los programas originales. Los paquetes se descargan desde la página oficial de Google al realizar la operación.

## 2. Requisitos
- Linux x86_64 y entorno gráfico.
- Conexión a Internet.
- Requisitos de bibliotecas del sistema publicados por Google para sus aplicaciones Linux.
- No necesita contraseña de administrador ni permisos sudo.

## 3. Descargar y ejecutar
Descarga `Antigravity-Installer-x86_64.AppImage` desde [Releases](https://github.com/Montejaque/antigravity-installer-linux/releases), permite su ejecución y ábrela. También puedes ejecutar `chmod +x Antigravity-Installer-x86_64.AppImage` y después `./Antigravity-Installer-x86_64.AppImage`.

## 4. Elegir qué instalar
Marca Antigravity App, Antigravity IDE o ambas. Pulsa **Instalar / actualizar seleccionados**. Solo se descargan y modifican los componentes marcados; el que no selecciones permanece intacto.

## 5. Comprobar versiones
Pulsa **Comprobar versiones** para consultar la versión instalada y la disponible de los componentes seleccionados. La consulta no descarga ni modifica las aplicaciones.

## 6. Actualizar
Marca App, IDE o ambas y pulsa **Instalar / actualizar seleccionados**. Cierra antes las aplicaciones que vayas a actualizar. La operación sustituye solo los componentes seleccionados.

## 7. Reparar accesos
Pulsa **Reparar accesos** para regenerar los lanzadores de los componentes instalados en el menú de aplicaciones.

## 8. Desinstalar
Marca los componentes que quieras quitar y pulsa **Desinstalar seleccionados**. La desinstalación no elimina perfiles personales, sesiones, configuraciones ni proyectos.

## 9. Ubicaciones
- App: `~/.local/opt/antigravity-app/`
- IDE: `~/.local/opt/antigravity-ide/`
- Lanzadores: `~/.local/bin/`
- Menú: `~/.local/share/applications/`
- Estado: `~/.local/opt/.antigravity-installer-state.json`

## 10. Seguridad y privacidad
Las descargas se validan contra HTTPS y los dominios oficiales de Google `storage.googleapis.com` y `edgedl.me.gvt1.com`. No se solicitan credenciales de Google, no se usan mirrors y no se modifican bibliotecas del sistema. Si Google cambia el formato de su página de descargas, el instalador se detiene en lugar de inventar una URL.

## 11. Ayuda
Comprueba la conexión y vuelve a intentar la operación si falla una descarga. No sustituyas bibliotecas del sistema ni intentes actualizar glibc manualmente.

## 12. Desarrollador
**Francisco Javier Gallego Orellana · Punto Vuela Montejaque**  
Avenida Andalucía, 48 · 29360 Montejaque (Málaga)  
633 402 959 · montejaque@puntosvuela.es  
https://puntosvuela.es/centros/montejaque

Google y Antigravity son marcas de Google LLC. Este proyecto es independiente y no está afiliado ni patrocinado por Google.
