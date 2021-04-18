class ProgressItem:
    def __init__(self, file_name: str, description: str = ''):
        self.file_name = file_name
        self.description = description

    def serialize(self):
        return {
            'file_name': self.file_name,
            'description': self.description
        }

    @staticmethod
    def deserialize(dictionary: dict):
        progress_item = ProgressItem(file_name=dictionary['file_name'], description=dictionary['description'])

        return progress_item
