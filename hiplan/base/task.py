class Task:
    def __init__(self, title = "No title", description = '', deadline = None, members = None, goals = None, labels = None):
        self.title = title
        self.description = description
        self.deadline: datetime = deadline
        self.members: List[Member] = members or []
        self.goals: List["Goal"] = goals or []
        self.labels: List["Label"] = labels or []

    def serialize(self):
        return {
            'title': self.title

        }
