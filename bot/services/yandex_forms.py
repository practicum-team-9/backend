from typing import Any, Dict, List

import aiohttp

from bot.config import settings
from bot.data_models.forms import FormItem, QuestionType


class YandexFormsService:
    """Сервис для взаимодействия с API Яндекс форм."""

    def __init__(self):
        self.base_url = settings.YANDEX_FORMS_URL

    def _extract_survey_id(self, form_url: str) -> str:
        """Метод для извлечения идентификатора формы из url."""

        clean_url = form_url.strip("/")
        parts = clean_url.split("/")
        if len(parts) >= 2:
            return parts[-1]
        return ""

    async def get_form_structure(self, form_url: str) -> List[FormItem]:
        """Метод для получения формы, готовой для работы с ботом."""

        survey_id = self._extract_survey_id(form_url)

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.base_url}{survey_id}/form"
            ) as response:
                form_data = await response.json()
                return self._parse_form_structure(form_data)

    def _parse_form_structure(self, form_data: Dict[str, Any]) -> List[FormItem]:
        """Метод для извлечения данных из формы в нужном формате."""
        questions = []

        pages = form_data.get("pages", form_data.get(
            "data", {}).get("pages", []))

        for page in pages:
            items = page.get("items", [])
            for item_data in items:
                question = FormItem(
                    id=item_data.get("id", ""),
                    label=item_data.get("label", ""),
                    type=item_data.get("type", "string"),
                    multiline=item_data.get("multiline", False),
                    widget=item_data.get("widget"),
                    items=[
                        {"id": opt.get("id"), "label": opt.get("label")}
                        for opt in item_data.get("items", [])
                    ],
                    validations=item_data.get("validations", []),
                    comment=item_data.get("comment")
                )
                questions.append(question)

        return questions

    async def submit_form(
            self,
            form_url: str,
            answers: Dict[str, str],
            form_structure: List[FormItem] = None
    ) -> bool:
        """Метод для отправки данных на заполнение формы."""

        survey_id = self._extract_survey_id(form_url)

        if not survey_id:
            return False

        if form_structure is None:
            form_structure = await self.get_form_structure(form_url)

        formatted_answers = self._format_answers_for_submission(
            answers, form_structure
        )

        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.base_url}{survey_id}/form",
                    json=formatted_answers,
                ) as response:
                    return response.status in [200, 201]

        except Exception:
            return False

    def _format_answers_for_submission(
        self,
        answers: Dict[str, str],
        form_structure: List[FormItem]
    ) -> Dict[str, Any]:
        """Метод приводит ответы из бота к нужному формату."""

        formatted = {}
        field_types = {}

        for question in form_structure:
            field_types[question.id] = question.type

        for field_id, value in answers.items():
            if not value or not value.strip():
                continue

            value = value.strip()
            field_type = field_types.get(field_id, "string")

            if field_type == QuestionType.ENUM:
                formatted[field_id] = [value]
            elif field_type == QuestionType.BOOLEAN:
                formatted[field_id] = value.lower() == "true"
            elif field_type == QuestionType.DATE:
                formatted[field_id] = value
            elif field_type == QuestionType.STRING:
                formatted[field_id] = value
            else:
                formatted[field_id] = value

        return formatted
