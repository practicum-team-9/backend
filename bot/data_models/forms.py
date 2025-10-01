"""Схемы для удобной работы с различными вариантами Яндекс Форм."""

from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, Field


class QuestionType(str, Enum):
    STRING = "string"
    DATE = "date"
    ENUM = "enum"
    BOOLEAN = "boolean"


class ValidationType(str, Enum):
    REQUIRED = "required"
    PHONE = "phone"
    EMAIL = "email"


class Validation(BaseModel):
    type: ValidationType


class OptionItem(BaseModel):
    id: str
    label: str


class FormItem(BaseModel):
    id: str
    label: str
    type: QuestionType
    multiline: Optional[bool] = False
    widget: Optional[str] = None
    items: List[OptionItem] = Field(default_factory=list)
    validations: List[Validation] = Field(default_factory=list)
    comment: Optional[str] = None


class FormPage(BaseModel):
    items: List[FormItem]


class FormStructure(BaseModel):
    id: str
    name: str
    iframe: bool
    texts: Dict[str, str]
    org: Dict[str, str]
    pages: List[FormPage]


class UserAnswer(BaseModel):
    question_id: str
    answer: str
    question_label: Optional[str] = None
