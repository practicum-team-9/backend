from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from texts import RETRY_SURVEY, SKIP_QUESTION


async def get_keyboard_buttons(
    skip_button=True
) -> list[list[KeyboardButton]]:
    """Базовые кнопки для клавиатуры."""
    keyboard_buttons = [[KeyboardButton(text=RETRY_SURVEY[0])]]
    if skip_button:
        keyboard_buttons.append(
            [KeyboardButton(text=SKIP_QUESTION[0])]
        )
    return keyboard_buttons


async def get_keyboard_by_buttons(
        keyboard_buttons: list[list[KeyboardButton]]
) -> ReplyKeyboardMarkup:
    """Формирует итоговую клавиатуру по переданным кнопкам."""
    return ReplyKeyboardMarkup(keyboard=keyboard_buttons, resize_keyboard=True)
