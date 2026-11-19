import tkinter as tk

from view import CalculatorView
from controller import CalculatorController


def main():
    # Небольшая настройка чёткости: Tk на Linux берёт scaling из системы,
    # но если картинка мыльная/крупная — подкрути 1.0..1.5 под свой монитор.
    root = tk.Tk()
    root.tk.call("tk", "scaling", 1.333)   # ≈96 DPI; попробуй 1.0 или 1.5
    root.destroy()

    view = CalculatorView()
    controller = CalculatorController(view)

    view.mainloop()


if __name__ == "__main__":
    main()