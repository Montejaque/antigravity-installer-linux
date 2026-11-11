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
    if product=="app":
        for name in ("Antigravity","antigravity"):
            candidate=APP_DIR/name
            if candidate.exists(): return candidate
        return APP_DIR/"Antigravity"
    for name in ("antigravity-ide","Antigravity IDE"):
        candidate=IDE_DIR/name
        if candidate.exists(): return candidate
    return IDE_DIR/"antigravity-ide"
def _asar_member(archive, member):
    """Read one small file from an Electron ASAR without launching the app."""
    import struct
    try:
        with archive.open("rb") as stream:
            prefix=stream.read(8)
            if len(prefix)!=8: return None
            header_size=struct.unpack("<I",prefix[0:4])[0]
            json_size=struct.unpack("<I",prefix[4:8])[0]
            if header_size<8 or json_size<=0 or json_size>16*1024*1024: return None
            header_bytes=stream.read(json_size)
            if len(header_bytes)!=json_size: return None
            header=json.loads(header_bytes.decode("utf-8"))
            node=header.get("files",{})
            parts=member.split("/")
            for index,part in enumerate(parts):
                node=node.get(part,{})
                if index<len(parts)-1: node=node.get("files",{})
            if not isinstance(node,dict) or "offset" not in node or "size" not in node: return None
            size=int(node["size"])
            if size<=0 or size>1024*1024: return None
            stream.seek(8+header_size+int(node["offset"]))
            return stream.read(size)
    except Exception:
        return None

def _installed_metadata_version(executable):
    root=executable.parent
    resources=root/"resources"
    candidates=(root/".antigravity-linux-version",resources/"app"/"product.json",resources/"app"/"package.json",
                resources/"product.json",root/"package.json")
    for metadata in candidates:
        try:
            data=json.loads(metadata.read_text(encoding="utf-8"))
            version=data.get("version")
            if isinstance(version,str) and re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?",version):
                return version
        except Exception:
            pass
    archive=resources/"app.asar"
    if archive.is_file():
        for member in ("product.json","package.json"):
            raw=_asar_member(archive,member)
            if raw:
                try:
                    version=json.loads(raw.decode("utf-8")).get("version")
                    if isinstance(version,str) and re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][0-9A-Za-z.-]+)?",version):
                        return version
                except Exception:
                    pass
    return None

def installed_versions():
    """Detect versions from saved state or local Electron metadata, without executing binaries."""
    state=_state()
    result={}
    for product in ("app","ide"):
        executable=_exe(product)
        if not executable.is_file():
            result[product]=None
            continue
        recorded=state.get(product,{})
        version=recorded.get("version") if isinstance(recorded,dict) else None
        result[product]=version or _installed_metadata_version(executable) or "Instalada (versión no detectada)"
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
        if _exe(p).is_file(): _launcher(p)
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
def _extract(archive,target,executable_names):
    stage=Path(tempfile.mkdtemp(prefix=".antigravity-stage-",dir=str(OPT)))
    try:
        # Do not strip a presumed top-level folder: Google's App and IDE tarballs
        # do not necessarily share the same archive layout.
        subprocess.run(["tar","-xzf",str(archive),"-C",str(stage),"--no-same-owner"],check=True,capture_output=True)
        candidates=[]
        for name in executable_names:
            candidates.extend(p for p in stage.rglob(name) if p.is_file())
        if not candidates: raise RuntimeError("El paquete no contiene el ejecutable esperado: "+", ".join(executable_names))
        exe=candidates[0]; root=exe.parent
        exe.chmod(exe.stat().st_mode|0o111)
        backup=target.with_name(target.name+".previous")
        if backup.exists(): shutil.rmtree(backup)
        if target.exists(): target.rename(backup)
        if root==stage: stage.rename(target)
        else: root.rename(target); shutil.rmtree(stage,ignore_errors=True)
        if backup.exists(): shutil.rmtree(backup)
    except Exception:
        shutil.rmtree(stage,ignore_errors=True); raise
def install(products=None,progress=None,status=None):
    products=tuple(products or ("app","ide"))
    if not products or set(products)-{"app","ide"}: raise ValueError("Selecciona App, IDE o ambas.")
    OPT.mkdir(parents=True,exist_ok=True); urls=latest_downloads(products); state=_state()
    jobs={"app":(APP_DIR,("Antigravity","antigravity"),"Antigravity-App.tar.gz"),
          "ide":(IDE_DIR,("antigravity-ide","Antigravity IDE"),"Antigravity-IDE.tar.gz")}
    for i,p in enumerate(products,1):
        target,executables,filename=jobs[p]; version=version_from_url(urls[p]); archive=OPT/filename
        if status: status("(%d/%d) Descargando %s · %s"%(i,len(products),p.upper(),version))
        download(urls[p],str(archive),progress)
        if status: status("Instalando %s…"%p.upper())
        _extract(archive,target,executables); archive.unlink(missing_ok=True)
        state[p]={"version":version,"source_url":urls[p],"installed_at":time.strftime("%Y-%m-%dT%H:%M:%S")}
        (target/".antigravity-linux-version").write_text(version+"\\n",encoding="utf-8")
        _save_state(state)
    repair_access(); return installed_versions()
def launch(product):
    path=_exe(product)
    if not path.is_file(): raise RuntimeError("El componente seleccionado no está instalado.")
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
