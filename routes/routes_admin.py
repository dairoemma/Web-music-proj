from flask import Flask, request, jsonify
from helper_function import jwt_initialization
from modules.user import get_all_user, get_user, insert_user, delete_user, update_user
from modules.musician import get_all_musician, get_musician, get_music, get_a_music
from flask import Blueprint, jsonify

admin_bp = Blueprint('user', __name__)
