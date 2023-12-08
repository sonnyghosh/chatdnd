from class_utils import db
import decision
class Story:

    def __init__(self):
        self.buffer_queue : list[str] = []
        self.decision_queue : list[decision.Decision] = []

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
