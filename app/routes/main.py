from flask import Blueprint, redirect

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def main():
    return redirect('/home')
