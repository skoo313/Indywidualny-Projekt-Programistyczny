import aubio
import pyaudio
import music21 
import numpy as np
import Queue as queue

pyau = pyaudio.PyAudio()

# Stream. in-dev-index to skad ma brac dzwiek
stream = pyau.open(format=pyaudio.paFloat32,
                channels=1, rate=44100, input=True,
                input_device_index=1, frames_per_buffer=4096)

# Aubio pitch detection.
pDetection = aubio.pitch("default", 2048, 2048//2, 44100)

# Set unit.
pDetection.set_unit("Hz")
pDetection.set_silence(-40)

#do wymiany danych z innymi skryptami
q = queue.Queue()

def get_note(volume_thresh=0.001):

    current_pitch = music21.pitch.Pitch()

    while True:

        data = stream.read(1024, exception_on_overflow=False)
        samples = np.fromstring(data,
                                dtype=aubio.float_type)
        pitch = pDetection(samples)[0]

        # Compute the energy (volume)
        volume = np.sum(samples**2)/len(samples) * 100

        if pitch and volume > volume_thresh:  # adjust with your mic!
            current_pitch.frequency = pitch
        else:
            continue

	q.put({'Note': current_pitch.nameWithOctave, 'Cents': current_pitch.microtone.cents})

        print("Name: {}".format(current_pitch.nameWithOctave))
	print("Frequency: {}".format(current_pitch.frequency))
	print("Volume: {}".format(volume))	
	print("Pitch: {}".format(pitch))	
	print("------")
        
        
if __name__ == '__main__':
    get_note(volume_thresh=0.001)
	
