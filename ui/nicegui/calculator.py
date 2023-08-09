from nicegui import app, ui

app.native.window_args['resizable'] = False
app.native.start_args['debug'] = True

class Calculator:
    def __init__(self):

        self.__expression = ""

        self.expression_text = ui.input('Expression')

        with ui.grid(columns=4):
            self.clear_button = ui.button('AC', on_click=self.on_clear)
            self.negate_button = ui.button('+/-')
            self.percent_button = ui.button('%')
            self.divide_button = ui.button('/', on_click=self.on_digit)

            self.button1 = ui.button('1', on_click=self.on_digit)
            self.button2 = ui.button('2', on_click=self.on_digit)
            self.button3 = ui.button('3', on_click=self.on_digit)
            self.multiply_button = ui.button('*', on_click=self.on_digit)

            self.button4 = ui.button('4', on_click=self.on_digit)
            self.button5 = ui.button('5', on_click=self.on_digit)
            self.button6 = ui.button('6', on_click=self.on_digit)
            self.minus_button = ui.button('-', on_click=self.on_digit)

            self.button7 = ui.button('7', on_click=self.on_digit)
            self.button8 = ui.button('8', on_click=self.on_digit)
            self.button9 = ui.button('9', on_click=self.on_digit)
            self.plus_button = ui.button('+', on_click=self.on_digit)

            self.button7 = ui.button('0', on_click=self.on_digit)
            self.button8 = ui.button('.', on_click=self.on_digit)
            ui.label()
            self.plus_button = ui.button('=', on_click=self.on_equal)

    @property
    def expression(self):
        return self.__expression
    
    @expression.setter
    def expression(self, value):
        self.__expression = value
        self.expression_text.set_value(value)

    def on_digit(self, e):
        print("digit")
        self.expression += e.sender.text

    def on_clear(self, e):
        print("clear")
        self.expression = ''

    def on_equal(self, e):
        print("equal") 
        try:
            self.expression = str(eval(self.expression))   
        except BaseException as e:
            ui.notify(str(e))


if __name__ in {"__main__", "__mp_main__"}:

    calc = Calculator()

    #ui.run(native=True, window_size=(400, 400), fullscreen=False)
    ui.run()