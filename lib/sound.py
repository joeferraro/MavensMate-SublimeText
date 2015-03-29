# plays only wav files
try:
    import sublime
    import os
    import sys
    import MavensMate.config as config

    class Sound:
        def __init__( self ):
            self.data = []

        def play( sound ):
            settings = sublime.load_settings( "mavensmate.sublime-settings" )
            if settings != None:
                doPlaySounds = settings.get( "mm_play_sounds", False )
                doPlayGeneralSounds = settings.get( "mm_play_general_sounds", False )
                doPlaySuccessSounds = settings.get( "mm_play_success_sounds", False )
                doPlayFailureSounds = settings.get( "mm_play_failure_sounds", False )
                generalSound = settings.get( "mm_general_sound_path", "" )
                if generalSound == "":
                    generalSound = os.path.join( config.mm_dir, "sounds", "general.wav" )
                successSound = settings.get( "mm_success_sound_path", "" )
                if successSound == "":
                    successSound = os.path.join( config.mm_dir, "sounds", "success.wav" )
                failureSound = settings.get( "mm_failure_sound_path", "" )
                if failureSound == "":
                    failureSound = os.path.join( config.mm_dir, "sounds", "failure.wav" )
                if doPlaySounds:
                    soundFile = ""
                    if sound == "general" and doPlayGeneralSounds == True:
                        soundFile = generalSound
                    elif sound == "success" and doPlaySuccessSounds == True:
                        soundFile = successSound
                    elif sound == "failure" and doPlayFailureSounds == True:
                        soundFile = failureSound
                    if soundFile != "" and os.path.isfile( "%s" % soundFile ) == True:
                        if "linux" in sys.platform:
                            import subprocess
                            subprocess.call(["aplay", soundFile])
                        elif "darwin" in sys.platform:
                            import subprocess
                            subprocess.call(["afplay", soundFile])
                        else:
                            import winsound
                            winsound.PlaySound( "%s" % soundFile, winsound.SND_FILENAME|winsound.SND_ASYNC )
except Exception as e:
    print(e)