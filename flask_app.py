from flask import Flask, render_template, jsonify, request
import json
import os
import sys


try:
    import world_generation
except ImportError:
    world_generation = None

app = Flask(__name__)

SETTINGS_FILE = 'settings.json'


def load_settings():
    """Default"""
    default_settings = {
        "cols": 35,
        "rows": 40,
        "brick_size": 11,
        "brick_padding": 1,
        "offset_top": 60,
        "drop_chance": 0.02,
        "ball_speed": 6,
        "current_level": 1,
        "current_score": 0
    }

    if not os.path.exists(SETTINGS_FILE):
        save_settings(default_settings)
        return default_settings

    try:
        with open(SETTINGS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
            for key, value in default_settings.items():
                if key not in data:
                    data[key] = value
            return data
    # Error
    except (json.JSONDecodeError, IOError):

        save_settings(default_settings)
        return default_settings


def save_settings(data):
    """Save to JSON"""
    try:
        with open(SETTINGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        print(f"Dosya kaydetme hatası: {e}")


@app.route('/')
def index():
    try:
        return render_template('index.html')
    except Exception as e:
        return f"Hata: 'templates/index.html' bulunamadı! Detay: {str(e)}", 404


@app.route('/game')
def game():
    try:
        return render_template('game.html')
    except Exception as e:
        return f"Hata: 'templates/game.html' bulunamadı! Detay: {str(e)}", 404


@app.route('/settings')
def settings_page():
    try:
        return render_template('settings.html')
    except Exception as e:
        return f"Hata: 'templates/settings.html' bulunamadı! Detay: {str(e)}", 404


@app.route('/get_settings')
def get_settings():
    return jsonify(load_settings())


@app.route('/reset_progress', methods=['POST'])
def reset_progress():
    s = load_settings()
    s['current_level'] = 1
    s['current_score'] = 0
    save_settings(s)
    return jsonify({"status": "reset"})


@app.route('/save_progress', methods=['POST'])
def save_progress():
    data = request.json
    s = load_settings()
    s['current_level'] = data.get('level', s['current_level'])
    s['current_score'] = data.get('score', s['current_score'])
    save_settings(s)
    return jsonify({"status": "saved"})


@app.route('/save_settings', methods=['POST'])
def update_settings():
    new_data = request.json
    save_settings(new_data)
    return jsonify({"status": "success"})


@app.route('/get_world_config/<int:level>')
def get_world_config(level):
    """
    Generating world data using world_generation.py
    """
    if world_generation is None:
        return jsonify({"error": "world_generation module missing"}), 500

    try:
        settings = load_settings()
        world_data = world_generation.generate_world_data(level, settings)
        return jsonify(world_data)
    except Exception as e:
        print(f"Dünya oluşturma hatası: {e}")
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)