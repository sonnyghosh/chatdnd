import os, json
from flask import render_template, request, Blueprint, g, abort
from backend.classes import decision, story
from backend.api.aiapi import generateStoryResponse

story_info = Blueprint('story_info', __name__)

@story_info.route('/story/get_new_buffer/<decision_id>/', methods=['POST', 'GET'])
def get_new_buffer(decision_id):
    dec = decision.get(decision_id)