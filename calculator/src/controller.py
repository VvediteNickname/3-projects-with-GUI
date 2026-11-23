from model import CalculatorModel


class CalculatorController:

    def __init__(self, view):
        self.model = CalculatorModel()
        self.view = view

        # Состояние калькулятора
        self.current = "0"
        self.first_operand = None
        self.operator = None
        self.waiting_for_second = True
        self.just_calculated = False

        # Подключение обработчиков событий
        self.view.set_callbacks({
            "digit": self.on_digit,
            "operator": self.on_operator,
            "equals": self.on_equals,
            "clear": self.on_clear,
            "sqrt": self.on_sqrt,
            "backspace": self.on_backspace
        })

    # ---------- ввод ----------

    def on_digit(self, digit):
        self.view.clear_error()

        # После "=" начинаем новое число
        if self.just_calculated:
            self.current = "0"
            self.just_calculated = False
            self.waiting_for_second = True

        # Если ждём второе число — сбрасываем текущее
        if self.waiting_for_second:
            self.current = "0"
            self.waiting_for_second = False

        # Точка
        if digit == ".":
            if "." in self.current:
                return
            self.current += "."
            self.view.set_display(self.current)
            return

        # Цифры
        if self.current == "0":
            self.current = digit
        else:
            self.current += digit

        self.view.set_display(self.current)

    def on_operator(self, operator):
        self.view.clear_error()

        # Если уже есть оператор — сначала посчитаем
        if self.operator is not None and not self.waiting_for_second:
            if not self._apply_pending():
                return

        self.first_operand = float(self.current)
        self.operator = operator
        self.waiting_for_second = True
        self.just_calculated = False

    def on_equals(self):
        self.view.clear_error()
        if self.current == "88005553535":
            self.view.show_error("""Лучше позвонить, 
                чем у кого-то занимать!""")
            return
    
        if self.operator is None:
            # Нечего считать — просто фиксируем текущее
            self.view.set_display(self.current)
            return

        second = float(self.current) if not self.waiting_for_second else self.first_operand

        try:
            result = self.calculate(self.first_operand, second, self.operator)
        except ZeroDivisionError:
            self.view.show_error("Деление на ноль!")
            self._reset_after_error()
            return
        except Exception as e:
            self.view.show_error(str(e))
            self._reset_after_error()
            return

        self.view.set_display(self._format(result))
        self.current = self._format(result)
        self.first_operand = None
        self.operator = None
        self.waiting_for_second = True
        self.just_calculated = True

    def on_clear(self):
        self.current = "0"
        self.first_operand = None
        self.operator = None
        self.waiting_for_second = True
        self.just_calculated = False
        self.view.set_display("0")
        self.view.clear_error()

    def on_sqrt(self):
        self.view.clear_error()

        # Корень берём от текущего отображаемого значения
        value = float(self.current)

        try:
            result = self.model.sqrt(value)
        except ValueError as e:
            self.view.show_error(str(e))
            return
        except Exception as e:
            self.view.show_error(str(e))
            return

        self.current = self._format(result)
        self.view.set_display(self.current)
        self.just_calculated = True
        self.waiting_for_second = True

    def on_backspace(self):
        self.view.clear_error()

        if self.waiting_for_second or self.just_calculated:
            return

        if len(self.current) <= 1 or (self.current.startswith("-") and len(self.current) == 2):
            self.current = "0"
        else:
            self.current = self.current[:-1]

        self.view.set_display(self.current)

    # ---------- вспомогательное ----------

    def calculate(self, a, b, operator):
        if operator == "+":
            return self.model.add(a, b)
        if operator == "-":
            return self.model.subtract(a, b)
        if operator == "*":
            return self.model.multiply(a, b)
        if operator == "/":
            return self.model.divide(a, b)
        raise ValueError(f"Неизвестная операция: {operator}")

    def _apply_pending(self):
        """Считает first_operand <op> current и сохраняет как first_operand."""
        second = float(self.current)
        try:
            result = self.calculate(self.first_operand, second, self.operator)
        except ZeroDivisionError:
            self.view.show_error("Деление на ноль!")
            self._reset_after_error()
            return False
        except Exception as e:
            self.view.show_error(str(e))
            self._reset_after_error()
            return False

        self.first_operand = result
        self.current = self._format(result)
        self.view.set_display(self.current)
        return True

    def _reset_after_error(self):
        self.current = "0"
        self.first_operand = None
        self.operator = None
        self.waiting_for_second = True
        self.just_calculated = False

    @staticmethod
    def _format(value):
        if value == int(value):
            return str(int(value))
        return str(value)