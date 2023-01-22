from datetime import datetime
from typing import List

from src.dependencies import db
from src.routes.control_tasks.validate_correctness.schema import \
    ValidateCorrectnessControlTask
from src.settings.logging import logger


def Add_validate_correctness_control_tasks_list(
        list: List[ValidateCorrectnessControlTask]) -> bool:
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
        return None
