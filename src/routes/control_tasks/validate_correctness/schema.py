from enum import Enum

from src.routes.control_tasks.schema import CommonControltask


class LabelEnum(str, Enum):
    Correct = 'correct'
    InCorrect = 'in_correct'
    NotRelatedToQuran = 'not_related_quran'
    NotMatchAya = 'not_match_aya'
    MultipleAya = 'multiple_aya'


class ValidateCorrectnessControlTask(CommonControltask):
    label: LabelEnum
