from pydub import AudioSegment

def update_ogg_audio_gain(oggfilepath, gain):

    if gain != 0:
        #load new song 
        song = AudioSegment.from_ogg(oggfilepath)

        # reduce/boost volume by XdB
        new_song = song + gain

        # save new song 
        new_song.export(oggfilepath, format='ogg')
    
    
def update_ogg_audio_speed(oggfilepath, speed=1.0):
    
    
    if speed > 1.0:
        #load new song 
        song = AudioSegment.from_ogg(oggfilepath)
        
        #new_song = song._spawn(song.raw_data, overrides={"frame_rate": int(song.frame_rate * speed)})
        new_song = song.speedup(speed)
        
        # save new song 
        new_song.export(oggfilepath, format='ogg')
    
    elif speed < 1.0:
        print("[ERROR] Lib pydub cannot slow the voice, normal speed used.")