import json, shutil, subprocess, tempfile, time, re
from pathlib import Path
from .release_source import latest_downloads, version_from_url, download

HOME=Path.home(); OPT=HOME/".local/opt"; BIN=HOME/".local/bin"
DESKTOP=HOME/".local/share/applications"; ICONS=HOME/".local/share/icons"
APP_DIR=OPT/"antigravity-app"; IDE_DIR=OPT/"antigravity-ide"
STATE=OPT/".antigravity-installer-state.json"
ICON_URL="https://antigravity.google/assets/image/brand/antigravity-icon__full-color.svg"

def _state():
    try: return json.loads(STATE.read_text(encoding="utf-8"))
    except Exception: return {}
def _save_state(data):
    OPT.mkdir(parents=True,exist_ok=True); STATE.write_text(json.dumps(data,indent=2),encoding="utf-8")
def _exe(product):
    if product=="app": return APP_DIR/"antigravity"
    candidate=IDE_DIR/"bin/antigravity-ide"
    return candidate if candidate.exists() else IDE_DIR/"antigravity-ide"
def _binary_version(path):
    if not path.exists(): return None
    for arg in ("--version","-v","-version"):
        try:
            result=subprocess.run([str(path),arg],capture_output=True,text=True,timeout=8)
            match=re.search(r"\b\d+\.\d+(?:\.\d+)?(?:[-+][\w.-]+)?\b",(result.stdout or "")+(result.stderr or ""))
            if match: return match.group(0)
        except Exception: pass
    return None
def installed_versions():
    state=_state(); result={}
    for p in ("app","ide"):
        result[p]=(_binary_version(_exe(p)) or state.get(p,{}).get("version")) if _exe(p).exists() else None
    return result
def _icon():
    ICONS.mkdir(parents=True,exist_ok=True); path=ICONS/"antigravity.svg"
    if not path.exists():
        try:
            from urllib.request import Request,urlopen
            with urlopen(Request(ICON_URL,headers={"User-Agent":"Mozilla/5.0"}),timeout=15) as r: data=r.read()
            if b"<svg" not in data[:2048]: raise ValueError("SVG inválido")
            path.write_bytes(data)
        except Exception:
            path.write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 128 128"><rect width="128" height="128" rx="26" fill="#252525"/><path d="M64 12 80 48 116 64 80 80 64 116 48 80 12 64 48 48Z" fill="#F3D54E"/></svg>')
    return path
def _launcher(product):
    name="antigravity-app" if product=="app" else "antigravity-ide"
    display="Antigravity App" if product=="app" else "Antigravity IDE"
    BIN.mkdir(parents=True,exist_ok=True); DESKTOP.mkdir(parents=True,exist_ok=True)
    wrapper=BIN/name; wrapper.write_text('#!/bin/sh\nexec "'+str(_exe(product))+'" "$@"\n'); wrapper.chmod(0o755)
    desktop=DESKTOP/(name+".desktop")
    desktop.write_text("[Desktop Entry]\nType=Application\nName="+display+"\nExec="+str(wrapper)+" %U\nIcon="+str(_icon())+"\nTerminal=false\nCategories=Development;Utility;\n")
    desktop.chmod(0o644)
def repair_access():
    for p in ("app","ide"):
        if _exe(p).exists(): _launcher(p)
    try: subprocess.run(["update-desktop-database",str(DESKTOP)],check=False,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    except FileNotFoundError: pass
def check_updates(products=None):
    products=tuple(products or ("app","ide"))
    if not products or set(products)-{"app","ide"}: raise ValueError("Selección de componentes no válida.")
    urls=latest_downloads(products); current=installed_versions()
    latest={p:version_from_url(urls[p]) for p in products}
    return {"current":{p:current[p] for p in products},"latest":latest,
            "installed":{p:current[p] is not None for p in products},
            "updates":{p:latest[p]!="unknown" and current[p]!=latest[p] for p in products}}
def _extract(archive,target,executable):
    stage=Path(tempfile.mkdtemp(prefix=".antigravity-stage-",dir=str(OPT)))
    try:
        subprocess.run(["tar","-xzf",str(archive),"-C",str(stage),"--strip-components=1","--no-same-owner"],check=True,capture_output=True)
        exe=stage/executable
        if not exe.is_file(): raise RuntimeError("El paquete no contiene el ejecutable esperado: "+executable)
        exe.chmod(exe.stat().st_mode|0o111)
        backup=target.with_name(target.name+".previous")
        if backup.exists(): shutil.rmtree(backup)
        if target.exists(): target.rename(backup)
        stage.rename(target)
        if backup.exists(): shutil.rmtree(backup)
    except Exception:
        shutil.rmtree(stage,ignore_errors=True); raise
def install(products=None,progress=None,status=None):
    products=tuple(products or ("app","ide"))
    if not products or set(products)-{"app","ide"}: raise ValueError("Selecciona App, IDE o ambas.")
    OPT.mkdir(parents=True,exist_ok=True); urls=latest_downloads(products); state=_state()
    jobs={"app":(APP_DIR,"antigravity","Antigravity-App.tar.gz"),"ide":(IDE_DIR,"bin/antigravity-ide","Antigravity-IDE.tar.gz")}
    for i,p in enumerate(products,1):
        target,executable,filename=jobs[p]; version=version_from_url(urls[p]); archive=OPT/filename
        if status: status("(%d/%d) Descargando %s · %s"%(i,len(products),p.upper(),version))
        download(urls[p],str(archive),progress)
        if status: status("Instalando %s…"%p.upper())
        _extract(archive,target,executable); archive.unlink(missing_ok=True)
        state[p]={"version":version,"source_url":urls[p],"installed_at":time.strftime("%Y-%m-%dT%H:%M:%S")}
        _save_state(state)
    repair_access(); return installed_versions()
def launch(product):
    path=_exe(product)
    if not path.exists(): raise RuntimeError("El componente seleccionado no está instalado.")
    subprocess.Popen([str(path)],start_new_session=True)
def uninstall(products=None):
    products=tuple(products or ("app","ide"))
    if not products or set(products)-{"app","ide"}: raise ValueError("Selección no válida.")
    for p in products:
        target=APP_DIR if p=="app" else IDE_DIR; name="antigravity-app" if p=="app" else "antigravity-ide"
        shutil.rmtree(target,ignore_errors=True); (BIN/name).unlink(missing_ok=True); (DESKTOP/(name+".desktop")).unlink(missing_ok=True)
    state=_state()
    for p in products: state.pop(p,None)
    _save_state(state)
