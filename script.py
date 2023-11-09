import time
import gradio as gr
from pathlib import Path
from modules import shared
import pyttsx4
import json

settings_file = 'extensions/win_tts/settings.json'

params = {
    "display_name": "Win TTS",
    "active": True,
    "autoplay": True,
    "show_text": True,
    "live_tts_enabled": False,
    "rate": 165,
    "volume": 0.9,
    "system_voice": "Microsoft Julie - French (France)",
}

def load_settings():
    try:
        with open(settings_file, 'r') as json_file:
            settings = json.load(json_file)
            params.update(settings)
    except FileNotFoundError:
        pass

load_settings()

def clean_text(text):
    cleaned_text = text.replace('&#x27;', "'").replace('&quot;', '"')
    return cleaned_text

def tts(text, output_file):
    cleaned_text = clean_text(text)
    engine = pyttsx4.init()
    engine.setProperty('rate', params['rate'])
    engine.setProperty('volume', params['volume'])

    system_voices = get_system_voices()
    selected_voice = params['system_voice']

    for voice in engine.getProperty('voices'):
        if voice.name == selected_voice:
            engine.setProperty('voice', voice.id)
            break

    engine.save_to_file(cleaned_text, output_file)
    engine.runAndWait()

def speak_live_tts(text):
    cleaned_text = clean_text(text)
    engine = pyttsx4.init()
    engine.setProperty('rate', params['rate'])
    engine.setProperty('volume', params['volume'])

    system_voices = get_system_voices()
    selected_voice = params['system_voice']

    for voice in engine.getProperty('voices'):
        if voice.name == selected_voice:
            engine.setProperty('voice', voice.id)
            break

    engine.say(cleaned_text)
    engine.runAndWait()

def output_modifier(string, state):
    if not params['active']:
        return string

    if params['live_tts_enabled']:
        speak_live_tts(string)
    else:
        if string == '':
            string = '*Empty reply, try regenerating*'
        else:
            output_file = Path(f'extensions/win_tts/outputs/{state["character_menu"]}_{int(time.time())}.wav')
            tts(string, str(output_file))

            shared.processing_message = "*Is typing..."

            autoplay = 'autoplay' if params['autoplay'] else ''
            html_string = f'<audio src="file/{output_file.as_posix()}" controls {autoplay}></audio>'

            if params['show_text']:
                string = f'{html_string}\n\n{string}'
            else:
                string = html_string

    return string

def remove_directory():
    directory = Path('extensions/win_tts/outputs')
    for file in directory.glob('*.wav'):
        file.unlink()

def history_modifier(history):
    if len(history['internal']) > 0:
        history['visible'][-1] = [
            history['visible'][-1][0],
            history['visible'][-1][1].replace('controls autoplay>', 'controls>')
        ]

    return history

def get_system_voices():
    engine = pyttsx4.init()
    voices = engine.getProperty('voices')
    return [voice.name for voice in voices]

def save_settings():
    settings = {
        "active": params["active"],
        "autoplay": params["autoplay"],
        "show_text": params["show_text"],
        "rate": params["rate"],
        "volume": params["volume"],
        "system_voice": params["system_voice"],
        "live_tts_enabled": params["live_tts_enabled"]
    }

    with open(settings_file, 'w') as json_file:
        json.dump(settings, json_file, indent=4)

def ui():
    with gr.Accordion(params["display_name"], open=True):
        activate = gr.Checkbox(value=params['active'], label='Active extension')
        autoplay = gr.Checkbox(value=params['autoplay'], label='Play TTS automatically')
        show_text = gr.Checkbox(value=params['show_text'], label='Show message text under audio player')
        live_tts_checkbox = gr.Checkbox(value=params['live_tts_enabled'], label='Live voice 🎙️')
        
        rate_slider = gr.Slider(minimum=50, maximum=200, label='Speech Rate', value=params['rate'])
        volume_slider = gr.Slider(minimum=0, maximum=1, step=0.1, label='Voice Volume', value=params['volume'])

        system_voices = get_system_voices()
        voice_dropdown = gr.Dropdown(choices=system_voices, label='System Voice', value=params['system_voice'])

        activate.change(lambda x: params.update({'active': x}), activate, None)
        autoplay.change(lambda x: params.update({'autoplay': x}), autoplay, None)
        show_text.change(lambda x: params.update({'show_text': x}), show_text, None)
        rate_slider.change(lambda x: params.update({'rate': x}), rate_slider, None)
        volume_slider.change(lambda x: params.update({'volume': x}), volume_slider, None)
        voice_dropdown.change(lambda x: params.update({'system_voice': x}), voice_dropdown, None)
        live_tts_checkbox.change(lambda x: params.update({'live_tts_enabled': x}), live_tts_checkbox, None)

        save_button = gr.Button("Save Settings")
        save_button.click(save_settings, None)

        remove_directory_button = gr.Button("Remove WAV Directory")
        remove_directory_button.click(remove_directory, None)
