import tkinter as tk


class RoundButton(tk.Canvas):
    """Круглая кнопка на Canvas: круг + текст."""

    def __init__(
        self,
        parent,
        text,
        command,
        size=70,
        bg_color="#6B8E23",
        hover_color="#556B2F",
        active_color="#7BA428",
        text_color="#ffffff",
        font=("Arial", 18, "bold"),
        parent_bg="#f5f5dc",
    ):
        super().__init__(
            parent,
            width=size,
            height=size,
            bg=parent_bg,          # фон «вокруг» круга = фон контейнера
            highlightthickness=0,
            bd=0,
            cursor="hand2",
        )
        self.command = command
        self.size = size
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.active_color = active_color
        self.text_color = text_color

        pad = 2
        self.circle = self.create_oval(
            pad, pad, size - pad, size - pad,
            fill=bg_color, outline=bg_color,
        )
        self.label = self.create_text(
            size / 2, size / 2,
            text=text, fill=text_color, font=font,
        )

        # Клик и hover
        self.bind("<Button-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)

    def _on_enter(self, _):
        self.itemconfig(self.circle, fill=self.hover_color, outline=self.hover_color)

    def _on_leave(self, _):
        self.itemconfig(self.circle, fill=self.bg_color, outline=self.bg_color)

    def _on_press(self, _):
        self.itemconfig(self.circle, fill=self.active_color, outline=self.active_color)

    def _on_release(self, event):
        # отпустили внутри кнопки — вернуть hover-цвет и вызвать команду
        inside = 0 <= event.x <= self.size and 0 <= event.y <= self.size
        if inside:
            self.itemconfig(self.circle, fill=self.hover_color, outline=self.hover_color)
            if self.command:
                self.command()
        else:
            self.itemconfig(self.circle, fill=self.bg_color, outline=self.bg_color)


class CalculatorView(tk.Tk):

    # ---------- палитра ----------
    BG          = "#f5f5dc"
    BTN_BG      = "#6B8E23"
    BTN_HOVER   = "#556B2F"
    BTN_ACTIVE  = "#7BA428"
    BTN_FG      = "#ffffff"
    ENTRY_BG    = "#ffffff"
    ENTRY_FG    = "#000000"
    ERROR_FG    = "#b00020"

    BTN_SIZE    = 70   # диаметр кнопки

    def __init__(self):
        super().__init__()

        # Настройки окна
        self.title("Calculator")
        self.minsize(360, 560)
        self.resizable(True, True)
        self.configure(bg=self.BG)

        # Хранилище колбэков
        self.callbacks = {}

        # Поле отображения
        self.display_var = tk.StringVar(value="0")
        self.display = tk.Entry(
            self,
            textvariable=self.display_var,
            state="readonly",
            justify="right",
            font=("Arial", 28),
            bg=self.ENTRY_BG,
            fg=self.ENTRY_FG,
            relief="flat",
            bd=8,
        )
        self.display.pack(padx=20, pady=(20, 10), fill="x")

        # Метка ошибок
        self.status_var = tk.StringVar(value="")
        self.status_label = tk.Label(
            self,
            textvariable=self.status_var,
            fg=self.ERROR_FG,
            bg=self.BG,
            font=("Arial", 11),
            anchor="w",
        )
        self.status_label.pack(padx=20, pady=(0, 10), fill="x")

        # Фрейм для кнопок
        self.buttons_frame = tk.Frame(self, bg=self.BG)
        self.buttons_frame.pack(padx=20, pady=10, expand=True, fill="both")

        self.create_buttons()

        # Клавиатура
        self.bind("<Key>", self._on_key)
        self.display.focus_set()

    def create_buttons(self):
        # (текст, row, col, тип события, значение)
        layout = [
            ("C",  0, 0, "clear", None),
            ("⌫", 0, 1, "backspace", None),
            ("√",  0, 2, "sqrt", None),
            ("/",  0, 3, "operator", "/"),

            ("7", 1, 0, "digit", "7"),
            ("8", 1, 1, "digit", "8"),
            ("9", 1, 2, "digit", "9"),
            ("*", 1, 3, "operator", "*"),

            ("4", 2, 0, "digit", "4"),
            ("5", 2, 1, "digit", "5"),
            ("6", 2, 2, "digit", "6"),
            ("-", 2, 3, "operator", "-"),

            ("1", 3, 0, "digit", "1"),
            ("2", 3, 1, "digit", "2"),
            ("3", 3, 2, "digit", "3"),
            ("+", 3, 3, "operator", "+"),

            ("0", 4, 0, "digit", "0"),
            (".", 4, 1, "digit", "."),
            ("=", 4, 2, "equals", None),
        ]

        for c in range(4):
            self.buttons_frame.grid_columnconfigure(c, weight=1)
        for r in range(5):
            self.buttons_frame.grid_rowconfigure(r, weight=1)

        for text, row, col, kind, value in layout:
            if kind == "equals":
                command = self._emit_equals
                colspan = 2
                # "=" делаем чуть акцентнее
                bg, hover, active = "#556B2F", "#6B8E23", "#7BA428"
            else:
                command = lambda k=kind, v=value: self._emit(k, v)
                colspan = 1
                bg, hover, active = self.BTN_BG, self.BTN_HOVER, self.BTN_ACTIVE

            btn = RoundButton(
                self.buttons_frame,
                text=text,
                command=command,
                size=self.BTN_SIZE,
                bg_color=bg,
                hover_color=hover,
                active_color=active,
                text_color=self.BTN_FG,
                font=("Arial", 18, "bold"),
                parent_bg=self.BG,
            )
            btn.grid(row=row, column=col, columnspan=colspan,
                     padx=6, pady=6, sticky="nsew")

    # ---------- клавиатура ----------

    def _on_key(self, event):
        ch = event.char
        if ch.isdigit() or ch == ".":
            self._emit("digit", ch)
        elif ch in "+-*/":
            self._emit("operator", ch)
        elif ch in ("=", "\r"):
            self._emit("equals", None)
        elif event.keysym == "BackSpace":
            self._emit("backspace", None)
        elif event.keysym == "Escape":
            self._emit("clear", None)

    # ---------- проброс событий ----------

    def _emit(self, kind, value):
        handler = self.callbacks.get(kind)
        if handler is None:
            return
        if value is None:
            handler()
        else:
            handler(value)

    def _emit_equals(self):
        self._emit("equals", None)

    # ---------- публичный API ----------

    def set_display(self, value):
        self.display_var.set(str(value))

    def get_display(self):
        return self.display_var.get()

    def show_error(self, message):
        self.status_var.set(message)

    def clear_error(self):
        self.status_var.set("")

    def set_callbacks(self, callbacks):
        self.callbacks = callbacks