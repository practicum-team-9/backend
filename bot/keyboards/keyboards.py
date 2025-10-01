from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from texts import (RETRY_EMOGI_BUTON, RETRY_SURVEY, SKIP_EMOGI_BUTTON,
                   SKIP_QUESTION)


async def get_keyboard_buttons(
    skip_button=True
) -> list[list[KeyboardButton]]:
    """Базовые кнопки для клавиатуры."""
    keyboard_buttons = [[KeyboardButton(text=RETRY_EMOGI_BUTON)]]
    if skip_button:
        keyboard_buttons.append(
            [KeyboardButton(text=SKIP_EMOGI_BUTTON)]
        )
    return keyboard_buttons


async def get_keyboard_by_buttons(
        keyboard_buttons: list[list[KeyboardButton]]
) -> ReplyKeyboardMarkup:
    """Формирует итоговую клавиатуру по переданным кнопкам."""
    return ReplyKeyboardMarkup(keyboard=keyboard_buttons, resize_keyboard=True)
