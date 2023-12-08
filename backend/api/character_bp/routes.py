import os, json
from flask import render_template, request, Blueprint, g, abort
from backend.classes import player

player_info = Blueprint('player_info', __name__)

@player_info.routes('/players/get_player/<player_id>', methods=['GET'])
def get_player(player_id):
    return json.dumps(player.get(player_id).asdict())


@player_info.routes('/players/update_player/<player_id>/<info>', methods=['PUT'])
def update_player(player_id, info):
    pl = player.get(player_id)
    complete = pl.update(info)
    if complete:
        return {'status': 200}
    else:
        return {'status': 405}
    

@player_info.routes('/players/delete_player/<player_id>', methods=['DELETE'])
def delete_player(player_id):
    success, status_code = player.delete(player_id)
    return {'status': status_code} 

@player_info.routes('/players/create_player/<info>', methods=['GET'])
def create_player(info):
    new_player, status_code = player.create(info)
    # TODO: figure out how to add a party member to a party
    return status_code