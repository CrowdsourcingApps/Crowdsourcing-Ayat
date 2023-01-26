import random
from datetime import datetime
from functools import lru_cache
from typing import List

from src.dependencies import db
from src.routes.control_tasks.validate_correctness.schema import LabelEnum
from src.routes.control_tasks.validate_correctness.schema import \
    ValidateCorrectnessControlTask as VCCT
from src.settings.logging import logger


def Add_validate_correctness_control_tasks_list(
        list: List[VCCT]) -> bool:
    try:
        for control_task in list:
            control_task_dict = dict(control_task)
            control_task_dict['create_date'] = str(datetime.now())
            rec_id = control_task_dict['recording_id']
            del control_task_dict['recording_id']
            db_node = db.child('validate_correctness_control_tasks')
            db_node.child(rec_id).set(control_task_dict)
        return True
    except Exception as ex:
        logger.exception('[Firebase] - Add new ValidateCorrectnessControlTask'
                         f'node error: {ex}')
        return False


def get_validate_correctness_entrance_exam_list(
        previous_solved_questions: List[str]) -> List[VCCT]:
    try:
        dbnode = db.child('validate_correctness_control_tasks')
        golden_tasks = dbnode.order_by_child('golden').equal_to(True).get()
        if golden_tasks.pyres is None:
            return None
        items = golden_tasks.val().items()
        ct_type1 = [{'recording_id': id, **item} for id, item in items
                    if item['label'] == LabelEnum.Correct
                    and id not in previous_solved_questions]
        ct_type2 = [{'recording_id': id, **item} for id, item in items
                    if item['label'] == LabelEnum.InCorrect
                    and id not in previous_solved_questions]
        ct_type3 = [{'recording_id': id, **item} for id, item in items
                    if item['label'] == LabelEnum.MultipleAya
                    and id not in previous_solved_questions]
        ct_type4 = [{'recording_id': id, **item} for id, item in items
                    if item['label'] == LabelEnum.NotMatchAya
                    and id not in previous_solved_questions]
        ct_type5 = [{'recording_id': id, **item} for id, item in items
                    if item['label'] == LabelEnum.NotRelatedToQuran
                    and id not in previous_solved_questions]
        test_questions = []
        test_questions += random.choices(ct_type1, k=2)
        test_questions += random.choices(ct_type2, k=2)
        test_questions += random.choices(ct_type3, k=1)
        test_questions += random.choices(ct_type4, k=1)
        test_questions += random.choices(ct_type5, k=1)

        try:
            obj_list = [VCCT(**test) for test in test_questions]
            return obj_list
        except Exception as ex:
            logger.exception('Parsing firebase VCCT list to'
                             f' VCCT list of objects error: {ex}')
            return None
    except Exception as ex:
        logger.exception('[Firebase] - get contol tasks from validate '
                         f'correctness control tasks node error: {ex}')
        return None


@lru_cache(maxsize=50)
def get_control_task_question_label(recording_id: str) -> LabelEnum:
    try:
        dbnode = db.child('validate_correctness_control_tasks')
        question = dbnode.child(recording_id).get()
        if question.pyres is None:
            return None
        label = question.val()['label']
        return label
    except Exception as ex:
        logger.exception('[Firebase] - get contol task question label'
                         ' from validate correctness control tasks'
                         f' node error: {ex}')
        return None
