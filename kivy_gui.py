from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.textinput import TextInput
from kivy.uix.dropdown import DropDown

from typing import List


Builder.load_file("layout.kv")


class MenuScreen(Screen):
    point_counter: int = 0
    criteria_labels: List[Label] = []
    criteria_inputs: List[TextInput] = []
    criteria_buttons: List[ToggleButton] = []
    dropdown_buttons: List[Button] = []

    def __init__(self, **kwargs):
        super(MenuScreen, self).__init__(**kwargs)
        self.setup_ui()

    def setup_ui(self) -> None:
        self.remove_criteria_dropdown = DropDown()
        btn = self.ids["remove_criteria"]
        btn.bind(on_release=self.remove_criteria_dropdown.open)
        self.remove_criteria_dropdown.bind(on_select=lambda _, x: self.remove_criteria(x))

        self.choose_distribution_dropdown = DropDown()
        btn = self.ids["choose_distribution"]
        btn.bind(on_release=self.choose_distribution_dropdown.open)
        self.choose_distribution_dropdown.bind(on_select=lambda _, x: setattr(btn, 'text', x))

        for text in ["Gaussa", "T-student"]:
            sub_btn = Button(text=text, size_hint_y=None)
            sub_btn.bind(on_release=lambda btn_: self.choose_distribution_dropdown.select(btn_.text))
            self.choose_distribution_dropdown.add_widget(sub_btn)

        self.sort_points_dropdown = DropDown()
        btn = self.ids["sort_points"]
        btn.bind(on_release=self.sort_points_dropdown.open)
        self.sort_points_dropdown.bind(on_select=lambda _, x: self.sort_points(x))

    def add_criteria(self) -> None:
        box = self.ids["criteria_layout"]
        box.rows += 1
        criteria_counter = len(self.criteria_labels) + 1

        lbl = Label(text=str(criteria_counter))
        box.add_widget(lbl)
        self.criteria_labels.append(lbl)

        inp = TextInput(hint_text=f"Kryterium {criteria_counter}")
        box.add_widget(inp)
        self.criteria_inputs.append(inp)

        btn = ToggleButton(text="Min", on_press=lambda btn_: self.choose_criteria(btn_))
        box.add_widget(btn)
        self.criteria_buttons.append(btn)

        self.setup_criteria()



        self.ids["11"].cols = criteria_counter

    def setup_criteria(self) -> None:
        i = len(self.criteria_inputs) - 1
        inp = self.criteria_inputs[i]
        text = inp.text if inp.text != "" else inp.hint_text
        sub_btn = Button(text=text, size_hint_y=None)
        sub_btn.bind(on_release=lambda _, idx=i: self.remove_criteria_dropdown.select(idx))
        self.remove_criteria_dropdown.add_widget(sub_btn)
        sub_btn = Button(text=text, size_hint_y=None)
        sub_btn.bind(on_release=lambda _, idx=i: self.sort_points_dropdown.select(idx))
        self.sort_points_dropdown.add_widget(sub_btn)
        self.dropdown_buttons.append(sub_btn)

    def remove_criteria(self, idx: int) -> None:
        box = self.ids["criteria_layout"]
        box.remove_widget(self.criteria_labels[idx])
        self.criteria_labels.pop(idx)
        box.remove_widget(self.criteria_inputs[idx])
        self.criteria_inputs.pop(idx)
        box.remove_widget(self.criteria_buttons[idx])
        self.criteria_buttons.pop(idx)
        self.remove_criteria_dropdown.remove_widget(self.dropdown_buttons[idx])
        self.sort_points_dropdown.remove_widget(self.dropdown_buttons[idx])
        # box.rows -= 1

    def sort_points(self, idx: int) -> None:
        print(idx)
        # box = self.ids["criteria_layout"]
        # box.remove_widget(self.criteria_labels[idx])
        # self.criteria_labels.pop(idx)
        # box.remove_widget(self.criteria_inputs[idx])
        # self.criteria_inputs.pop(idx)
        # box.remove_widget(self.criteria_buttons[idx])
        # self.criteria_buttons.pop(idx)
        # self.remove_criteria_dropdown.remove_widget(self.dropdown_buttons[idx])
        # box.rows -= 1

    def choose_criteria(self, btn: ToggleButton) -> None:
        btn.text = "Max" if btn.text == "Min" else "Min"

    def add_point(self):
        box = self.ids["11"]
        self.ids["11"].rows += 1
        box.add_widget(Label(text="1"))
        # box.add_widget(TextInput(hint_text=f"Kryterium {self.counter + 1}"))
        # btn = ToggleButton(text="Min", on_press=lambda btn: self.click(btn))
        # box.add_widget(btn)
        # self.counter += 1


class TestApp(App):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(MenuScreen(name="menu"))

        return sm
    
if __name__ == "__main__":
    TestApp().run()