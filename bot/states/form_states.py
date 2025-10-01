from aiogram.fsm.state import State, StatesGroup


class FormFilling(StatesGroup):
    """Стейты для раличных этапов заполнения формы."""
    waiting_for_answer = State()
    text_answer = State()
    choice_answer = State()
    date_answer = State()
    bool_answer = State()
