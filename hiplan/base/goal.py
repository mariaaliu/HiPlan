from hiplan.base.progress_status import ProgressStatus


class Goal:
    def __init__(self, name, progress_status=ProgressStatus.UNSOLVED):
        self.name = name
        self.progress_status = progress_status

    def serialize(self):
        return {
            'name': self.name,
            'progress_status': self.progress_status.value
        }

    @staticmethod
    def deserialize(dictionary: dict):
        goal = Goal(name=dictionary['name'], progress_status=dictionary['progress_status'])

        return goal
