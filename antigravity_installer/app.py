import threading, tkinter as tk, sys
from pathlib import Path
from tkinter import ttk, messagebox
from .installer import install,check_updates,installed_versions,repair_access,uninstall,launch
from . import __version__

BG="#FFFFFF"; INK="#252525"; MUTED="#646464"; YELLOW="#F3D54E"; PANEL="#F5F5F5"

class App:
    def __init__(self,root):
        self.root=root; root.title("Antigravity Installer · Linux"); root.geometry("820x720"); root.minsize(650,620); root.configure(bg=BG)
        style=ttk.Style(root)
        try: style.theme_use("clam")
        except tk.TclError: pass
        style.configure("TFrame",background=BG); style.configure("TLabel",background=BG,foreground=INK,font=("Inter",10))
        style.configure("TButton",font=("Inter",9),padding=8); style.configure("Horizontal.TProgressbar",troughcolor="#EEEEEE",background=YELLOW)
        outer=ttk.Frame(root,padding=24); outer.pack(fill="both",expand=True)
        tk.Label(outer,text="ANTIGRAVITY",bg=BG,fg=INK,font=("Inter",25,"bold")).pack(anchor="w")
        tk.Label(outer,text="INSTALLER FOR LINUX · APP + IDE · v"+__version__,bg=BG,fg=MUTED,font=("Inter",9,"bold")).pack(anchor="w",pady=(2,12))
        tk.Frame(outer,bg=YELLOW,height=4).pack(fill="x",pady=(0,14))
        tk.Label(outer,text="DESCARGAS OFICIALES DE GOOGLE · INSTALACIÓN POR USUARIO · SIN ROOT",bg="#FFF8D9",fg="#594900",padx=12,pady=10,font=("Inter",9,"bold")).pack(fill="x")
        self.app=tk.BooleanVar(value=True); self.ide=tk.BooleanVar(value=True)
        box=tk.Frame(outer,bg=PANEL,padx=14,pady=12); box.pack(fill="x",pady=14)
        tk.Label(box,text="¿QUÉ COMPONENTES QUIERES GESTIONAR?",bg=PANEL,fg=MUTED,font=("Inter",9,"bold")).pack(anchor="w")
        row=tk.Frame(box,bg=PANEL); row.pack(fill="x",pady=8)
        tk.Checkbutton(row,text="Antigravity App",variable=self.app,bg=PANEL,selectcolor="white",font=("Inter",10,"bold")).pack(side="left",padx=(0,24))
        tk.Checkbutton(row,text="Antigravity IDE",variable=self.ide,bg=PANEL,selectcolor="white",font=("Inter",10,"bold")).pack(side="left")
        self.versions=tk.StringVar(value="App: —     IDE: —")
        tk.Label(outer,textvariable=self.versions,bg=BG,fg=INK,font=("Inter",10,"bold")).pack(anchor="w",pady=(0,12))
        self.status=tk.StringVar(value="Selecciona los componentes y una operación.")
        tk.Label(outer,textvariable=self.status,bg=BG,fg=MUTED,wraplength=740,justify="left").pack(anchor="w",pady=6)
        self.progress=ttk.Progressbar(outer,mode="indeterminate"); self.progress.pack(fill="x",pady=8)
        actions=ttk.Frame(outer); actions.pack(fill="x",pady=8)
        ttk.Button(actions,text="Instalar / actualizar seleccionados",command=lambda:self.run("install")).pack(fill="x",pady=3)
        ttk.Button(actions,text="Comprobar versiones",command=lambda:self.run("check")).pack(fill="x",pady=3)
        ttk.Button(actions,text="Reparar accesos",command=self.repair).pack(fill="x",pady=3)
        ttk.Button(actions,text="Desinstalar seleccionados",command=lambda:self.run("uninstall")).pack(fill="x",pady=3)
        launchrow=ttk.Frame(outer); launchrow.pack(fill="x",pady=6)
        ttk.Button(launchrow,text="Abrir App",command=lambda:self.open_product("app")).pack(side="left",expand=True,fill="x",padx=3)
        ttk.Button(launchrow,text="Abrir IDE",command=lambda:self.open_product("ide")).pack(side="left",expand=True,fill="x",padx=3)
        links=ttk.Frame(outer); links.pack(fill="x",pady=(10,0))
        ttk.Button(links,text="Guía de ayuda",command=self.show_guide).pack(side="left",padx=3)
        credits=tk.Frame(outer,bg=BG); credits.pack(side="bottom",fill="x",pady=(14,0))
        tk.Label(credits,text="Desarrollado por Francisco Javier Gallego Orellana",bg=BG,fg=INK,font=("Inter",8,"bold")).pack(anchor="w")
        tk.Label(credits,text="Punto Vuela Montejaque · montejaque@puntosvuela.es",bg=BG,fg=MUTED,font=("Inter",8)).pack(anchor="w")
        self.refresh()
    def show_guide(self):
        base=Path(getattr(sys,"_MEIPASS",Path(__file__).resolve().parents[1]))
        guide=base/"docs"/"GUIA_USUARIO.md"
        if not guide.is_file():
            messagebox.showerror("Guía de ayuda","No se encuentra el archivo de ayuda incluido en esta instalación.",parent=self.root)
            return
        window=tk.Toplevel(self.root)
        window.title("Guía de ayuda · Antigravity Installer")
        window.geometry("760x620")
        window.transient(self.root)
        frame=ttk.Frame(window,padding=12); frame.pack(fill="both",expand=True)
        text=tk.Text(frame,wrap="word",font=("Inter",10),padx=12,pady=10,relief="flat")
        scroll=ttk.Scrollbar(frame,orient="vertical",command=text.yview)
        text.configure(yscrollcommand=scroll.set)
        scroll.pack(side="right",fill="y"); text.pack(side="left",fill="both",expand=True)
        text.insert("1.0",guide.read_text(encoding="utf-8"))
        text.configure(state="disabled")

    def selected(self):
        items=[]
        if self.app.get(): items.append("app")
        if self.ide.get(): items.append("ide")
        if not items: messagebox.showwarning("Selección","Selecciona App, IDE o ambos.",parent=self.root)
        return items
    def refresh(self):
        v=installed_versions(); self.versions.set("Antigravity App: "+str(v["app"] or "No instalada")+"     |     Antigravity IDE: "+str(v["ide"] or "No instalado"))
    def run(self,action):
        products=self.selected()
        if not products:return
        if action=="uninstall" and not messagebox.askyesno("Confirmar","¿Desinstalar los componentes seleccionados? Los perfiles personales no se borran.",parent=self.root):return
        def work():
            try:
                self.root.after(0,lambda:self.progress.start(10))
                if action=="install": result=install(products,status=lambda s:self.root.after(0,lambda:self.status.set(s)))
                elif action=="check":
                    data=check_updates(products); result="\n".join("%s · instalada: %s · disponible: %s · %s"%(p.upper(),data["current"][p] or "no",data["latest"][p],"actualizada" if not data["updates"][p] else "hay actualización") for p in products)
                else: uninstall(products); result="Desinstalación completada."
                self.root.after(0,lambda:self.status.set(str(result)))
                self.root.after(0,self.refresh)
                if action=="install":
                    details=[]
                    for product in products:
                        label="Antigravity App" if product=="app" else "Antigravity IDE"
                        version=result.get(product) if isinstance(result,dict) else None
                        details.append(label+((" · versión "+str(version)) if version else " · instalada"))
                    summary="La instalación ha finalizado correctamente.\\n\\n"+"\\n".join(details)
                    self.root.after(0,lambda:messagebox.showinfo("Instalación completada",summary,parent=self.root))
            except Exception as exc: self.root.after(0,lambda:messagebox.showerror("Antigravity Installer",str(exc),parent=self.root))
            finally: self.root.after(0,self.progress.stop)
        threading.Thread(target=work,daemon=True).start()
    def repair(self):
        try: repair_access(); self.status.set("Accesos reparados."); self.refresh()
        except Exception as e: messagebox.showerror("Reparar accesos",str(e),parent=self.root)
    def open_product(self,p):
        try: launch(p)
        except Exception as e: messagebox.showerror("Abrir aplicación",str(e),parent=self.root)

def main():
    root=tk.Tk(); App(root); root.mainloop()
if __name__=="__main__": main()
