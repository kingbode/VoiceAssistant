getAudioID.py

this spt gets you the id of your mic device to be used in the main script in command

            with sr.Microphone(device_index=10) as source:
                r.adjust_for_ambient_noise(source, duration=1)
                audio = r.listen(source)
