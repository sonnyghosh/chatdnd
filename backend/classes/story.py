from dataclasses import dataclass, asdict
from class_utils import db, generate_id
import decision

@dataclass
class Story:

    def __init__(self):
        self.id = generate_id()
        self.buffer_queue : list[str] = []

    @classmethod
    def get(cls, story_id : str):
        try:
            story_ref = db.collection('story')
            story = story_ref.document(story_id).get()
            if story.exists:
                story_df = story.asdict()
                story_result = cls(**story_df)
                story_result.story_id = story_id
                return story_result, 200
            return story_result, 404
        except:
            return story_result, 500

    def new_story_element(self, story: str, last_decision: str):
        self.buffer_queue.pop()
        self.buffer_queue[0] += last_decision
        self.buffer_queue.insert(0, story)

    def get_context(self):
        return ''.join(self.buffer_queue)

    def asdict(self):
        return asdict(self)