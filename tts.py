import os
import pygame
from gtts import gTTS

def text_to_speech(text, filename="temp_speech.mp3", language='vi'):
    try:
        base_name = filename
        attempt = 0
        while os.path.exists(filename):
            try:
                os.remove(filename)
                break
            except PermissionError:
                attempt += 1
                filename = f"{os.path.splitext(base_name)[0]}_{attempt}.mp3"
        tts = gTTS(text=text, lang=language, slow=False)
        tts.save(filename)
        pygame.mixer.music.load(filename)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        return True
    except Exception as e:
        return False
    
if __name__ == '__main__':
    text_to_speech("alo alo 1 2 3 4")