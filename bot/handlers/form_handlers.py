from aiogram import Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import (KeyboardButton, Message, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)
from services.speechkit import SpeechKitService
from services.yandex_forms import YandexFormsService
from states.form_states import FormFilling

from data_models.forms import FormItem, QuestionType
from database.db_manager import DatabaseManager
from keyboards import get_keyboard_buttons, get_keyboard_by_buttons
from texts import (BOOL_QUESTION, CHOICE_QUESTION, COMPLETION_MESSAGE,
                       DATE_QUESTION, OPTIONAL_QUESTION, REQUIRED_QUESTION,
                       RETRY_SURVEY, SKIP_QUESTION, START_EMOGI_BUTTON,
                       START_SURVEY, STRING_QUESTION, SUBMIT_ERROR_MESSAGE,
                       WELCOME_INSTRUCTION, WRONG_BOOL_CHOICE, WRONG_CHOICE,
                       WRONG_DATE, WRONG_EMAIL, WRONG_PHONE_FORMAT)

from .validators import (validate_date_format, validate_email_format,
                         validate_phone_format)


class FormHandlers:
    def __init__(
        self,
        db: DatabaseManager,
        forms_service: YandexFormsService,
        speech_service: SpeechKitService
    ):
        self.router = Router()
        self.db = db
        self.forms_service = forms_service
        self.speech_service = speech_service

        # Регистрируем обработчики
        self.router.message.register(self.start_handler, CommandStart())
        self.router.message.register(
            self.text_answer_handler,
            StateFilter(FormFilling.text_answer)
        )
        self.router.message.register(
            self.choice_answer_handler,
            StateFilter(FormFilling.choice_answer)
        )
        self.router.message.register(
            self.date_answer_handler,
            StateFilter(FormFilling.date_answer)
        )
        self.router.message.register(
            self.bool_answer_handler,
            StateFilter(FormFilling.bool_answer)
        )
        self.router.message.register(self.stateless_handler)

    async def start_handler(self, message: Message, state: FSMContext):
        """Действия при переходе в бота по ссылке."""
        await state.clear()

        if message.text.startswith('/start'):
            parts = message.text.split()
            if len(parts) > 1:
                identifier = parts[1]
                if identifier:
                    form_data = await self.db.get_form_by_identifier(identifier=identifier)
                    if form_data:
                        form_url = form_data.get('url')
                        questions = await self.forms_service.get_form_structure(form_url)
                        await state.update_data(
                            form_url=form_url,
                            questions=questions,
                            current_question_index=0,
                            answers={},
                            form_identifier=identifier
                        )

                        await self.send_welcome_instruction(message)
                        return

            await message.answer("❌ Форма не найдена или не указан идентификатор")

    async def send_welcome_instruction(self, message: Message):
        """Отправляем голосовую инструкцию при начале опроса."""

        await message.answer_voice(
            voice=await self.speech_service.text_to_speech(
                WELCOME_INSTRUCTION,
                "instruction.ogg"
            ),
            caption="🎧 Инструкция по прохождению анкеты",
            reply_markup=ReplyKeyboardMarkup(
                keyboard=[[KeyboardButton(text=START_EMOGI_BUTTON)]],
                resize_keyboard=True
            )
        )

    async def stateless_handler(self, message: Message, state: FSMContext):
        """Обработчик кнопок при отсутствии состояния."""
        if message.text in START_SURVEY:
            await self.ask_next_question(message, state)
        elif message.text in RETRY_SURVEY:
            await self.restart_form(message, state)

    async def restart_form(self, message: Message, state: FSMContext):
        """Начинаем форму заново."""
        data = await state.get_data()
        form_url = data.get("form_url")
        questions = data.get("questions", [])
        form_identifier = data.get("form_identifier")

        # Кейс перезапуска в процессе опроса.
        if form_url and questions:
            await state.update_data(
                current_question_index=0,
                answers={}
            )
            await message.answer("🔄 Опрос начат заново", reply_markup=ReplyKeyboardRemove())
            await self.ask_next_question(message, state)
        # Кейс перезапуска после прохождения опроса.
        elif form_identifier:
            await self.restart_form_by_identifier(message, state, form_identifier)

    async def restart_form_by_identifier(self, message: Message, state: FSMContext, identifier: str):
        """Перезапускаем форму по идентификатору."""
        form_data = await self.db.get_form_by_identifier(identifier=identifier)
        form_url = form_data.get('url')
        questions = await self.forms_service.get_form_structure(form_url)
        await state.update_data(
            form_url=form_url,
            questions=questions,
            current_question_index=0,
            answers={},
            form_identifier=identifier
        )
        await message.answer("🔄 Опрос начат заново", reply_markup=ReplyKeyboardRemove())
        await self.ask_next_question(message, state)

    async def ask_next_question(self, message: Message, state: FSMContext):
        data = await state.get_data()
        questions = data.get("questions", [])
        current_index = data.get("current_question_index", 0)
        answers = data.get("answers", {})

        while (current_index < len(questions) and
               questions[current_index].id in answers):
            current_index += 1

        if current_index < len(questions):
            question = questions[current_index]
            question_text = ""
            required_question = False
            question_validations = question.validations
            for validator in question_validations:
                if validator.type == "required":
                    required_question = True
            if required_question:
                question_text += REQUIRED_QUESTION
            else:
                question_text += OPTIONAL_QUESTION
            question_type = question.type
            if question_type == "string":
                question_text += STRING_QUESTION
                question_text += question.label
            elif question_type == "date":
                question_text += DATE_QUESTION
                question_text += question.label + "."
            elif question_type == "boolean":
                question_text += BOOL_QUESTION
                question_text += question.label + "."
            elif question_type == "enum":
                items = question.items
                question_text += CHOICE_QUESTION
                question_text += question.label + "."
                counter = 1
                for item in items:
                    question_text += str(counter) + "." + item.label + ", "
                    counter += 1

            if question.comment:
                question_text += f"\n\n💡 {question.comment}"

            await message.answer_voice(
                voice=await self.speech_service.text_to_speech(
                    question_text,
                    "question.ogg"
                ),
                caption=f"🎯 Вопрос {current_index + 1}/{len(questions)}"
            )
            text_caption = f"🎯 Вопрос {current_index + 1}/{len(questions)}\n\n{question_text}"
            await message.answer(text_caption)
            await self.setup_question_state(
                message,
                state,
                question,
                current_index,
                skip_button=not required_question
            )
        else:
            await self.submit_form(message, state)

    async def setup_question_state(
        self,
        message: Message,
        state: FSMContext,
        question: FormItem,
        current_index: int,
        skip_button=False
    ):
        """Определяемся с состоянием в зависимости от типа вопроса."""
        await state.update_data(
            current_question_id=question.id,
            current_question_index=current_index
        )
        if question.type == QuestionType.STRING:
            await self.setup_text_question(message, state, skip_button=skip_button)
        elif question.type == QuestionType.ENUM:
            await self.setup_choice_question(message, state, question, skip_button=skip_button)
        elif question.type == QuestionType.DATE:
            await self.setup_date_question(message, state, skip_button=skip_button)
        elif question.type == QuestionType.BOOLEAN:
            await self.setup_bool_question(message, state, skip_button=skip_button)

    async def setup_text_question(
        self,
        message: Message,
        state: FSMContext,
        skip_button=False
    ):
        """Состояние текстового вопроса."""
        await message.answer(
            "Введите ответ:",
            reply_markup=await get_keyboard_by_buttons(
                await get_keyboard_buttons(skip_button=skip_button)
            )
        )
        await state.set_state(FormFilling.text_answer)

    async def setup_choice_question(
        self,
        message: Message,
        state: FSMContext,
        question: FormItem,
        skip_button=False
    ):
        """Состояние вопроса с вариантами ответа."""
        keyboard_buttons = await get_keyboard_buttons(skip_button=skip_button)
        for item in question.items:
            keyboard_buttons.append([KeyboardButton(text=item.label)])
        await message.answer(
            "Выберите вариант из списка ниже:",
            reply_markup=await get_keyboard_by_buttons(keyboard_buttons)
        )
        await state.set_state(FormFilling.choice_answer)

    async def setup_date_question(
            self,
            message: Message,
            state: FSMContext,
            skip_button=False
    ):
        """Состояние вопроса с датой."""
        await message.answer(
            "Введите ответ:",
            reply_markup=await get_keyboard_by_buttons(
                await get_keyboard_buttons(skip_button=skip_button)
            )
        )
        await state.set_state(FormFilling.date_answer)

    async def setup_bool_question(
            self,
            message: Message,
            state: FSMContext,
            skip_button=False
    ):
        """Состояние булевого вопроса."""
        keyboard_buttons = await get_keyboard_buttons(skip_button=skip_button)
        keyboard_buttons.extend([
            [KeyboardButton(text="Да"), KeyboardButton(text="Нет")]
        ])
        await message.answer(
            "Выберите ответ:",
            reply_markup=await get_keyboard_by_buttons(keyboard_buttons)
        )
        await state.set_state(FormFilling.bool_answer)

    async def text_answer_handler(self, message: Message, state: FSMContext):
        """Обработчи тектового ответа."""
        if message.text in SKIP_QUESTION:
            answer = ""
            await self.save_answer_and_continue(message, state, answer)
        elif message.text in RETRY_SURVEY:
            await self.restart_form(message, state)
        else:
            data = await state.get_data()
            current_question_index = data.get("current_question_index")
            current_question = data.get("questions")[current_question_index]
            validation_type = None
            validation = current_question.validations
            for validator in validation:
                if validator.type == "phone":
                    validation_type = "phone"
                if validator.type == "email":
                    validation_type = "email"

            if validation_type == "phone":
                if not validate_phone_format(message.text):

                    await message.answer_voice(
                        voice=await self.speech_service.text_to_speech(
                            WRONG_PHONE_FORMAT,
                            "wrong_phone_format.ogg"
                        ),
                        caption="❌ Неверный формат номера телефона"
                    )
                    return
                answer = message.text

            elif validation_type == "email":
                if not validate_email_format(message.text):
                    await message.answer_voice(
                        voice=await self.speech_service.text_to_speech(
                            WRONG_EMAIL,
                            "wrong_email.ogg"
                        ),
                        caption="❌ Неверный формат e-mail"
                    )
                    return
                answer = message.text.strip()
            else:
                answer = message.text
            await self.save_answer_and_continue(message, state, answer)

    async def choice_answer_handler(self, message: Message, state: FSMContext):
        """Обработчик ответа с выбором из вариантов."""
        if message.text in SKIP_QUESTION:
            answer = ""
            await self.save_answer_and_continue(message, state, answer)
        elif message.text in RETRY_SURVEY:
            await self.restart_form(message, state)
        else:
            data = await state.get_data()
            current_question_index = data.get("current_question_index", 0)
            questions = data.get("questions", [])
            question = questions[current_question_index]
            selected_item = None

            for item in question.items:
                if item.label.lower() == message.text.lower():
                    selected_item = item
                    break

            if selected_item:
                await self.save_answer_and_continue(message, state, selected_item.id)
            else:
                await message.answer_voice(
                    voice=await self.speech_service.text_to_speech(
                        WRONG_CHOICE,
                        "wrong_choice.ogg"
                    ),
                    caption="❌ Пожалуйста, выберите вариант из списка"
                )

    async def date_answer_handler(self, message: Message, state: FSMContext):
        """Обработчик ответа с датой."""
        if message.text in SKIP_QUESTION:
            answer = ""
            await self.save_answer_and_continue(message, state, answer)
        elif message.text in RETRY_SURVEY:
            await self.restart_form(message, state)
        else:
            # Велидируем формат даты.
            if not validate_date_format(message.text):
                await message.answer_voice(
                    voice=await self.speech_service.text_to_speech(
                        WRONG_DATE,
                        "wrong_date.ogg"
                    ),
                    caption="❌ Неверный формат даты"
                )
                return
            answer = message.text
            await self.save_answer_and_continue(message, state, answer)

    async def bool_answer_handler(self, message: Message, state: FSMContext):
        """Обработчик булевого ответа."""
        if message.text in SKIP_QUESTION:
            answer = ""
            await self.save_answer_and_continue(message, state, answer)
        elif message.text in RETRY_SURVEY:
            await self.restart_form(message, state)
        elif message.text in ("Да", "да"):
            answer = "true"
            await self.save_answer_and_continue(message, state, answer)
        elif message.text in ("Нет", "нет"):
            answer = "false"
            await self.save_answer_and_continue(message, state, answer)
        else:
            await message.answer_voice(
                voice=await self.speech_service.text_to_speech(
                    WRONG_BOOL_CHOICE,
                    "wrong_bool_choice.ogg"
                ),
                caption="❌ Пожалуйста, выберите 'Да' или 'Нет'"
            )

    async def save_answer_and_continue(self, message: Message, state: FSMContext, answer: str):
        """Сохраняем ответ в контексте и переходим к следующему вопросу."""
        data = await state.get_data()
        current_question_id = data.get("current_question_id")
        answers = data.get("answers", {})

        answers[current_question_id] = answer

        await state.update_data(answers=answers)

        await state.update_data(
            current_question_index=data.get("current_question_index", 0) + 1
        )

        await self.ask_next_question(message, state)

    async def send_completion_message(self, message: Message, state: FSMContext):
        """Отправляем голосовое сообщение после успешного прохождения всех вопросов."""

        await message.answer_voice(
            voice=await self.speech_service.text_to_speech(
                COMPLETION_MESSAGE,
                "completion.ogg"
            ),
            caption="✅ Анкета завершена",
            reply_markup=await get_keyboard_by_buttons(
                await get_keyboard_buttons(skip_button=False)
            )
        )
        data = await state.get_data()
        form_identifier = data.get("form_identifier")
        await state.clear()
        await state.update_data(form_identifier=form_identifier)

    async def submit_form(self, message: Message, state: FSMContext):
        """Отправка данных в Яндекс Формы."""
        data = await state.get_data()
        form_url = data.get("form_url")
        answers = data.get("answers", {})
        questions = data.get("questions", [])

        success = await self.forms_service.submit_form(form_url, answers, questions)
        if success:
            await self.send_completion_message(message, state)
        else:
            form_identifier = data.get("form_identifier")
            await state.clear()
            await state.update_data(form_identifier=form_identifier)
            await message.answer_voice(
                voice=await self.speech_service.text_to_speech(
                    SUBMIT_ERROR_MESSAGE,
                    "submit_error.ogg"
                ),
                caption="❌ Произошла ошибка при отправке формы.",
                reply_markup=await get_keyboard_by_buttons(
                    await get_keyboard_buttons(skip_button=False)
                )
            )
