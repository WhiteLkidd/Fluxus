import customtkinter as ctk
from tkinter import filedialog, simpledialog, colorchooser
from datetime import datetime
import os
import re
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

app = ctk.CTk()
app.geometry("1180x700")
app.title("📝 SimonPad")
app.minsize(980, 560)
app.resizable(True, True)

current_file = None
current_lang = None
bg_image = None
current_dir = os.getcwd()

editor_font = ["Consolas", 14]
colors = {
    "keyword": "#4FC3F7",
    "comment": "#6A9955",
    "string": "#CE9178",
    "background": "#1e1e1e",
    "text": "#d4d4d4",
    "type": "#C586C0",
    "number": "#B5CEA8",
    "op": "#DCDCAA",
    "use": "#569CD6",
    "panel": "#141414",
    "panel2": "#101010",
    "border": "#2A2A2A",
    "accent": "#4FC3F7",
}

SYNTAX = {
    "py": {
        "keywords": ["def","class","import","from","return","if","else","elif","for","while","True","False","None"],
        "comment": "#"
    },
    "c":  {
        "keywords": ["int","char","return","if","else","for","while","void","struct"],
        "comment": "//"
    },
    "cpp":{
        "keywords": ["int","class","return","if","else","for","while","void","namespace","std"],
        "comment": "//"
    },
    "flx": {
        "keywords": [
            "Use","fun","return","if","else","while","break","continue",
            "and","or","not",
            "true","false","null"
        ],
        "types": ["int","double","String","bool"],
        "comment": "//"
    }
}

# ===================== LAYOUT ROOT =====================
root = ctk.CTkFrame(app, fg_color=colors["panel2"])
root.pack(fill="both", expand=True)

# Paned window: resizable explorer/editor
paned = tk.PanedWindow(root, orient="horizontal", sashwidth=6, bd=0, bg=colors["panel2"], relief="flat")
paned.pack(fill="both", expand=True)

# Left sidebar (explorer)
sidebar = ctk.CTkFrame(root, fg_color=colors["panel"], corner_radius=0)
# Right editor area
main = ctk.CTkFrame(root, fg_color=colors["panel2"], corner_radius=0)

paned.add(sidebar, minsize=190, width=250)
paned.add(main, minsize=500)

# ===================== SIDEBAR CONTENT =====================
# Iconic header
logo_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
logo_frame.pack(pady=(18, 10), padx=14, anchor="w")

ctk.CTkLabel(logo_frame, text="⬛", font=("Segoe UI Emoji", 26)).pack(anchor="w")
ctk.CTkLabel(
    logo_frame,
    text="SimonPad",
    font=("Orbitron", 22, "bold"),
    text_color="white"
).pack(anchor="w", pady=(2, 0))

ctk.CTkLabel(
    logo_frame,
    text="Code with aura",
    font=("Consolas", 10),
    text_color="#8a8a8a"
).pack(anchor="w", pady=(2, 0))

file_label = ctk.CTkLabel(sidebar, text="No file", wraplength=220, text_color="#cfcfcf")
file_label.pack(pady=(10, 6), padx=14, anchor="w")

# Explorer (folder + file list)
expl_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
expl_frame.pack(fill="both", expand=True, padx=10, pady=(6, 10))

expl_top = ctk.CTkFrame(expl_frame, fg_color="transparent")
expl_top.pack(fill="x", pady=(0, 6))

ctk.CTkLabel(expl_top, text="Explorer", font=("Consolas", 12, "bold"), text_color="#bdbdbd").pack(side="left", padx=(4, 0))

def _refresh_explorer():
    try:
        path_label.configure(text=current_dir)
        file_list.delete(0, "end")
        entries = []
        for name in os.listdir(current_dir):
            full = os.path.join(current_dir, name)
            if os.path.isdir(full):
                entries.append(("📁 " + name, full, True))
            else:
                entries.append(("📄 " + name, full, False))
        # folders first
        entries.sort(key=lambda x: (not x[2], x[0].lower()))
        for label, full, isdir in entries:
            file_list.insert("end", label)
        file_list._entries = entries
    except Exception:
        pass

def _go_parent_dir():
    global current_dir
    parent = os.path.dirname(current_dir)
    if parent and parent != current_dir:
        current_dir = parent
        _refresh_explorer()

def _pick_dir():
    global current_dir
    d = filedialog.askdirectory(initialdir=current_dir)
    if d:
        current_dir = d
        _refresh_explorer()

btn_row = ctk.CTkFrame(expl_frame, fg_color="transparent")
btn_row.pack(fill="x", padx=4, pady=(0, 8))

ctk.CTkButton(btn_row, text="⬆", width=36, height=32, command=_go_parent_dir).pack(side="left", padx=(0, 6))
ctk.CTkButton(btn_row, text="📁", width=36, height=32, command=_pick_dir).pack(side="left")

path_label = ctk.CTkLabel(expl_frame, text=current_dir, wraplength=220, justify="left", text_color="#9c9c9c", font=("Consolas", 10))
path_label.pack(fill="x", padx=6, pady=(0, 6))

file_list = tk.Listbox(
    expl_frame,
    font=("Consolas", 11),
    bg=colors["panel"],
    fg="#d9d9d9",
    selectbackground="#2a5aa8",
    selectforeground="#ffffff",
    highlightthickness=1,
    highlightbackground=colors["border"],
    bd=0,
    activestyle="none"
)
file_list.pack(fill="both", expand=True, padx=6, pady=(0, 10))
file_list._entries = []

def detect_language(name, content=None):
    global current_lang
    ext = name.split(".")[-1].lower()

    if ext in ("flx", "fluxus", "flux"):
        current_lang = "flx"
        return

    if ext in SYNTAX:
        current_lang = ext
        return

    if content:
        if (
            re.search(r"(?m)^\s*Use\s+fluxus\.start\s*;", content)
            or re.search(r"(?m)^\s*Use\s+fluxus\.math\s*;", content)
            or re.search(r"(?m)^\s*Use\s+fluxus\.colrs\s*;", content)
            or re.search(r"(?m)^\s*Use\s+fluxus\.filesys\s*;", content)
            or re.search(r"(?m)^\s*Use\s+knihovna\s*;", content)
        ):
            current_lang = "flx"
            return

    current_lang = None

def _open_path_in_editor(path, content=None):
    global current_file, current_dir
    current_file = path
    current_dir = os.path.dirname(path) if os.path.dirname(path) else current_dir
    file_label.configure(text=os.path.basename(path))

    if content is None:
        editor.delete("1.0", "end")
    else:
        editor.delete("1.0", "end")
        editor.insert("1.0", content)

    detect_language(path, content or "")
    highlight()
    _refresh_explorer()

def new_file():
    global current_dir
    name = simpledialog.askstring("New File", "File name:")
    if not name:
        return
    path = os.path.join(current_dir, name)
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, "w", encoding="utf-8").close()
    except Exception as e:
        messagebox.showerror("Error", f"Cannot create file:\n{e}")
        return
    _open_path_in_editor(path, "")

def open_file():
    global current_dir
    path = filedialog.askopenfilename(initialdir=current_dir)
    if not path:
        return
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception as e:
        messagebox.showerror("Error", f"Cannot open file:\n{e}")
        return
    _open_path_in_editor(path, content)

def save_file():
    if not current_file:
        # save-as
        path = filedialog.asksaveasfilename(initialdir=current_dir, defaultextension=".txt")
        if not path:
            return
        try:
            with open(path, "w", encoding="utf-8") as f:
                f.write(editor.get("1.0", "end-1c"))
        except Exception as e:
            messagebox.showerror("Error", f"Cannot save file:\n{e}")
            return
        _open_path_in_editor(path, editor.get("1.0", "end-1c"))
        return

    try:
        with open(current_file, "w", encoding="utf-8") as f:
            f.write(editor.get("1.0", "end-1c"))
    except Exception as e:
        messagebox.showerror("Error", f"Cannot save file:\n{e}")

def _open_from_explorer(_e=None):
    sel = file_list.curselection()
    if not sel:
        return
    idx = sel[0]
    if not hasattr(file_list, "_entries") or idx >= len(file_list._entries):
        return
    label, full, isdir = file_list._entries[idx]
    if isdir:
        global current_dir
        current_dir = full
        _refresh_explorer()
        return

    try:
        with open(full, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()
    except Exception as e:
        messagebox.showerror("Error", f"Cannot open file:\n{e}")
        return
    _open_path_in_editor(full, content)

file_list.bind("<Double-Button-1>", _open_from_explorer)
file_list.bind("<Return>", _open_from_explorer)

# Buttons (compact)
btns = ctk.CTkFrame(sidebar, fg_color="transparent")
btns.pack(fill="x", padx=10, pady=(0, 12))

ctk.CTkButton(btns, text="📄 New", command=new_file, height=36).pack(fill="x", pady=6)
ctk.CTkButton(btns, text="📂 Open", command=open_file, height=36).pack(fill="x", pady=6)
ctk.CTkButton(btns, text="💾 Save", command=save_file, height=36).pack(fill="x", pady=6)

# ===================== EDITOR =====================
editor = ctk.CTkTextbox(
    main,
    font=(editor_font[0], editor_font[1]),
    undo=True,
    fg_color=colors["background"],
    text_color=colors["text"],
    wrap="none",
    corner_radius=10
)
editor.pack(fill="both", expand=True, padx=12, pady=12)

# Status bar bottom (small)
status = ctk.CTkLabel(
    app,
    anchor="w",
    text_color="#a6a6a6",
    fg_color=colors["panel2"],
    font=("Consolas", 10)
)
status.pack(fill="x", ipady=2)

# ===================== TAGS =====================
editor.tag_config("kw", foreground=colors["keyword"])
editor.tag_config("typ", foreground=colors["type"])
editor.tag_config("com", foreground=colors["comment"])
editor.tag_config("str", foreground=colors["string"])
editor.tag_config("num", foreground=colors["number"])
editor.tag_config("op", foreground=colors["op"])
editor.tag_config("use", foreground=colors["use"])

def _tag_spans(tag, text, pattern, flags=0):
    for m in re.finditer(pattern, text, flags):
        editor.tag_add(tag, f"1.0+{m.start()}c", f"1.0+{m.end()}c")

def highlight():
    for t in ("kw","typ","com","str","num","op","use"):
        editor.tag_remove(t, "1.0", "end")

    if current_lang not in SYNTAX:
        return

    text = editor.get("1.0", "end-1c")
    rules = SYNTAX[current_lang]

    _tag_spans("str", text, r"\".*?(?<!\\)\"|\'.*?(?<!\\)\'")
    cmark = re.escape(rules["comment"])
    _tag_spans("com", text, rf"{cmark}.*")
    _tag_spans("num", text, r"\b\d+(\.\d+)?\b")

    if current_lang == "flx":
        _tag_spans("op", text, r"(<-)|(\*)|(&)|(\[\])|(\[)|(\])|(\{)|(\})|(;)|(\()|(\))|(\.)|(:)")
        _tag_spans("use", text, r"(?m)^\s*Use\s+[A-Za-z0-9_.]+\s*;")
        for t in rules.get("types", []):
            _tag_spans("typ", text, rf"\b{re.escape(t)}\b")

    for kw in rules["keywords"]:
        _tag_spans("kw", text, rf"\b{re.escape(kw)}\b")

# ===================== SETTINGS =====================
def open_settings():
    global bg_image
    win = ctk.CTkToplevel(app)
    win.geometry("420x560")
    win.title("Settings")
    win.grab_set()

    ctk.CTkLabel(win, text="Editor Settings", font=("Orbitron", 18)).pack(pady=14)

    def set_font_size(val):
        editor_font[1] = int(val)
        editor.configure(font=(editor_font[0], editor_font[1]))
        highlight()

    ctk.CTkLabel(win, text="Font Size").pack()
    ctk.CTkSlider(win, from_=10, to=30, command=set_font_size).pack(pady=8, padx=18, fill="x")

    def pick_color(key):
        col = colorchooser.askcolor()[1]
        if col:
            colors[key] = col
            editor.tag_config("kw", foreground=colors["keyword"])
            editor.tag_config("typ", foreground=colors["type"])
            editor.tag_config("com", foreground=colors["comment"])
            editor.tag_config("str", foreground=colors["string"])
            editor.tag_config("num", foreground=colors["number"])
            editor.tag_config("op", foreground=colors["op"])
            editor.tag_config("use", foreground=colors["use"])
            editor.configure(fg_color=colors["background"], text_color=colors["text"])
            highlight()

    ctk.CTkButton(win, text="Keyword Color", command=lambda: pick_color("keyword")).pack(pady=5)
    ctk.CTkButton(win, text="Type Color", command=lambda: pick_color("type")).pack(pady=5)
    ctk.CTkButton(win, text="Comment Color", command=lambda: pick_color("comment")).pack(pady=5)
    ctk.CTkButton(win, text="String Color", command=lambda: pick_color("string")).pack(pady=5)
    ctk.CTkButton(win, text="Number Color", command=lambda: pick_color("number")).pack(pady=5)
    ctk.CTkButton(win, text="Operator Color", command=lambda: pick_color("op")).pack(pady=5)
    ctk.CTkButton(win, text="Use/Import Color", command=lambda: pick_color("use")).pack(pady=5)
    ctk.CTkButton(win, text="Background Color", command=lambda: pick_color("background")).pack(pady=5)
    ctk.CTkButton(win, text="Text Color", command=lambda: pick_color("text")).pack(pady=5)

    def set_bg_image():
        global bg_image
        path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg *.bmp")])
        if path:
            img = Image.open(path)
            img = img.resize((max(1, editor.winfo_width()), max(1, editor.winfo_height())))
            bg_image = ImageTk.PhotoImage(img)
            editor.configure(fg_color="transparent")
            editor.image_create("1.0", image=bg_image)
            highlight()

    ctk.CTkButton(win, text="Set Background Image", command=set_bg_image).pack(pady=12)

ctk.CTkButton(sidebar, text="⚙ Settings", command=open_settings, height=36).pack(fill="x", padx=10, pady=(0, 14))

# ===================== STATUS UPDATE =====================
def update_status():
    lines = editor.index("end-1c").split(".")[0]
    lang = current_lang or "text"
    fname = os.path.basename(current_file) if current_file else "No file"
    status.configure(text=f"{fname}   |   Lines: {lines}   |   Lang: {lang}   |   {datetime.now().strftime('%H:%M:%S')}")
    app.after(700, update_status)

# ===================== FLUXUS AUTOCOMPLETE =====================
FLX_SUGGESTIONS = []
FLX_SUGGESTIONS += SYNTAX["flx"]["keywords"]
FLX_SUGGESTIONS += SYNTAX["flx"]["types"]
FLX_SUGGESTIONS += ["fluxus.start","fluxus.math","fluxus.colrs","fluxus.filesys"]
FLX_SUGGESTIONS += [
    "println()","toStr()","len()","randInt()",
    "clear()","sleep()","key()","getln()","gotoXY()","setColor()","hideCursor()","showCursor()",
    "readFile()","writeFile()","appendFile()","exists()","deleteFile()","mkdir()","listDir()",
    "sin()","cos()","tan()","sqrt()","floor()","ceil()","pow()","min()","max()"
]

FLX_SNIPPETS = {
    "use": "Use fluxus.start;\n",
    "usem": "Use fluxus.math;\n",
    "usec": "Use fluxus.colrs;\n",
    "usef": "Use fluxus.filesys;\n",
    "fun": "fun name(int a){\n    return a;\n}\n",
    "struct": "struct TypeName {\n    field: value\n};\n",
    "structp": "struct Person {\n    name: \"\",\n    age: 0\n};\n",
    "structv": "var <- struct TypeName {\n    field: value\n};\n",
}


FLX_SUGGESTIONS = sorted(set(FLX_SUGGESTIONS), key=lambda x: x.lower())

_sugg_win = None
_sugg_list = None
_sugg_items = []
_sugg_start_index = None

def _get_current_word():
    insert = editor.index("insert")
    line_start = insert.split(".")[0] + ".0"
    left = editor.get(line_start, insert)
    m = re.search(r"([A-Za-z_][A-Za-z0-9_\.]*)$", left)
    if not m:
        return "", None, insert
    word = m.group(1)
    start_col = int(insert.split(".")[1]) - len(word)
    start_index = insert.split(".")[0] + f".{start_col}"
    return word, start_index, insert

def _hide_suggestions():
    global _sugg_win, _sugg_list, _sugg_items, _sugg_start_index
    if _sugg_win is not None:
        try:
            _sugg_win.destroy()
        except Exception:
            pass
    _sugg_win = None
    _sugg_list = None
    _sugg_items = []
    _sugg_start_index = None

def _apply_suggestion(choice):
    global _sugg_start_index
    if _sugg_start_index is None:
        return

    if choice in FLX_SNIPPETS:
        insert_text = FLX_SNIPPETS[choice]
    else:
        insert_text = choice
        if choice.endswith("()"):
            insert_text = choice[:-1]

    editor.delete(_sugg_start_index, "insert")
    editor.insert(_sugg_start_index, insert_text)
    _hide_suggestions()
    highlight()

def _place_sugg_window():
    bbox = editor.bbox("insert")
    if not bbox:
        return
    x, y, w, h = bbox
    rx = editor.winfo_rootx() + x
    ry = editor.winfo_rooty() + y + h + 2
    _sugg_win.geometry(f"+{rx}+{ry}")

def _show_suggestions(items, start_index):
    global _sugg_win, _sugg_list, _sugg_items, _sugg_start_index
    _sugg_items = items
    _sugg_start_index = start_index

    if _sugg_win is None:
        _sugg_win = tk.Toplevel(app)
        _sugg_win.overrideredirect(True)
        _sugg_win.attributes("-topmost", True)
        _sugg_win.configure(bg="#111111")

        _sugg_list = tk.Listbox(
            _sugg_win,
            font=(editor_font[0], max(11, editor_font[1]-2)),
            width=36,
            height=min(10, max(3, len(items))),
            activestyle="none",
            bg="#111111",
            fg="#d4d4d4",
            selectbackground="#2a5aa8",
            selectforeground="#ffffff",
            highlightthickness=1,
            highlightbackground="#2a2a2a",
            bd=0
        )
        _sugg_list.pack(fill="both", expand=True)

        def on_pick(_e=None):
            sel = _sugg_list.curselection()
            if not sel:
                return
            choice = _sugg_items[sel[0]]
            _apply_suggestion(choice)

        _sugg_list.bind("<Double-Button-1>", on_pick)
        _sugg_list.bind("<Return>", on_pick)
        _sugg_list.bind("<Tab>", on_pick)
        _sugg_list.bind("<ButtonRelease-1>", on_pick)
        _sugg_list.bind("<Escape>", lambda _e=None: (_hide_suggestions(), "break")[1])

        def on_up(_e=None):
            if not _sugg_items:
                return "break"
            i = _sugg_list.curselection()
            idx = i[0] if i else 0
            idx = max(0, idx-1)
            _sugg_list.selection_clear(0, "end")
            _sugg_list.selection_set(idx)
            _sugg_list.activate(idx)
            return "break"

        def on_down(_e=None):
            if not _sugg_items:
                return "break"
            i = _sugg_list.curselection()
            idx = i[0] if i else -1
            idx = min(len(_sugg_items)-1, idx+1)
            _sugg_list.selection_clear(0, "end")
            _sugg_list.selection_set(idx)
            _sugg_list.activate(idx)
            return "break"

        _sugg_list.bind("<Up>", on_up)
        _sugg_list.bind("<Down>", on_down)

    _sugg_list.delete(0, "end")
    for it in items:
        _sugg_list.insert("end", it)

    if items:
        _sugg_list.selection_clear(0, "end")
        _sugg_list.selection_set(0)
        _sugg_list.activate(0)

    _sugg_list.configure(height=min(10, max(3, len(items))))
    _place_sugg_window()

def _update_suggestions(force=False):
    if current_lang != "flx":
        _hide_suggestions()
        return

    word, start_index, _ins = _get_current_word()
    if not force and (not word or len(word) < 1):
        _hide_suggestions()
        return

    prefix = (word or "").lower()
    items = []

    if prefix:
        for k in FLX_SNIPPETS.keys():
            if k.lower().startswith(prefix):
                items.append(k)
        for s in FLX_SUGGESTIONS:
            if s.lower().startswith(prefix):
                items.append(s)
    else:
        items = list(FLX_SNIPPETS.keys()) + FLX_SUGGESTIONS

    seen = set()
    out = []
    for it in items:
        if it not in seen:
            seen.add(it)
            out.append(it)

    out = out[:50]
    if not out:
        _hide_suggestions()
        return

    if start_index is None:
        start_index = editor.index("insert")

    _show_suggestions(out, start_index)

def _ctrl_space(_e=None):
    _update_suggestions(force=True)
    return "break"

def _on_click_any(_e=None):
    _hide_suggestions()

def _tab_apply_or_indent(_e=None):
    global _sugg_list, _sugg_items
    if _sugg_list is not None and _sugg_items:
        sel = _sugg_list.curselection()
        idx = sel[0] if sel else 0
        choice = _sugg_items[idx]
        _apply_suggestion(choice)
        return "break"
    return None

_highlight_job = None
_sugg_job = None

def on_key_release(_e=None):
    global _highlight_job, _sugg_job
    if _highlight_job:
        app.after_cancel(_highlight_job)
    _highlight_job = app.after(60, highlight)

    if _sugg_job:
        app.after_cancel(_sugg_job)
    _sugg_job = app.after(40, _update_suggestions)

# binds (editor EXISTS here ✅)
editor.bind("<KeyRelease>", on_key_release)
editor.bind("<Control-space>", _ctrl_space)
editor.bind("<Tab>", _tab_apply_or_indent)
editor.bind("<Button-1>", _on_click_any)
editor.bind("<MouseWheel>", _on_click_any)
editor.bind("<FocusOut>", _on_click_any)

# Init explorer + status
_refresh_explorer()
update_status()

app.mainloop()
