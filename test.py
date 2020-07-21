from Cogs.Fun._mediaconverter import AudioConverter


AudioConverter.init()
# print(AudioConverter._files_map.get('barney'))
print(AudioConverter.text_to_speech('vox', 'ass', 'ass', 'ass'))
# print(AudioConverter.text_to_speech('barney', 'heybuddy', 'badfeeling').get('output'))


"""
@echo off
FOR /F "tokens=*" %G IN ('dir /b *.wav') DO ffmpeg -i "%G" -acodec mp3 "%~nG.mp3"
"""
