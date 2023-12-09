import os, json
from flask import render_template, request, Blueprint, g, abort
from backend.classes import decision, story
from backend.api.aiapi import generateStoryResponse

story_info = Blueprint('story_info', __name__)

@story_info.route('/story/get_new_buffer/<story_id>/<decision_id>/', methods=['POST', 'GET'])
def get_new_buffer(story_id, decision_id):
    story = story.get(story_id)
    decision = decision.get(decision_id)
    context = story.get_context()
    new_story = generateStoryResponse(prompt=decision, context=context)
