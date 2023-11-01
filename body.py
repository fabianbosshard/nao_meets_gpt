from flask import Flask, request, jsonify
from naoqi import ALProxy, ALModule, ALBroker
import time


app = Flask(__name__)

nao = True
nao_IP = 'nao.local'
port = 9559
broker = "myBroker"

tts = ALProxy("ALTextToSpeech", nao_IP, port)
audio_recorder = ALProxy("ALAudioRecorder", nao_IP, port)

# define volume of the robot
tts.setVolume(0.5)

@app.route('/talk', methods=['POST'])
def talk():
    print("Received a request to talk")
    message = request.json.get('message')
    tts.say(str(message))
    return jsonify(success=True)

# NAOqi module for capturing audio
class AudioCaptureModule(ALModule):
    """ 
    This is a custom module built on top of NAOqi framework for managing audio capture from NAO's microphones.
    It extends ALModule class from the NAOqi framework and defines methods to to start and stop audio capture, process audio data, and retrieve audio chunks. 
    """
    def __init__(self, name):
        ALModule.__init__(self, name)
        self.audio_device = ALProxy("ALAudioDevice", nao_IP, port)
        self.is_listening = False
        self.buffers = []

    def start_listening(self):
        self.audio_device.setClientPreferences(self.getName(), 16000, 3, 0) # sample rate of 16000 Hz, using 3 (all) available audio channels, and a deinterleaving flag of 0
        self.audio_device.subscribe(self.getName())
        self.is_listening = True

    def stop_listening(self):
        self.audio_device.unsubscribe(self.getName())
        self.is_listening = False

    def processRemote(self, nbOfChannels, nbOfSamplesByChannel, timeStamp, inputBuffer): # callback method that is triggered whenever new audio data is available
        print("received audio data from NAO with the following parameters: nbOfChannels = " + str(nbOfChannels) + ", nbOfSamplesByChannel = " + str(nbOfSamplesByChannel) + ", timeStamp = " + str(timeStamp))
        print("length and type of server buffer", len(self.buffers), type(self.buffers))
        print("length and type inputBuffer:", len(inputBuffer), type(inputBuffer))
        print("first element of inputBuffer:", inputBuffer[0])
        if self.is_listening:
            self.buffers.append(inputBuffer)

    def get_audio_chunk(self):
        if self.buffers:
            return self.buffers.pop(0) # Return the oldest audio chunk
        else:
            print("no audio data available")
            return None

# broker connection: essential for communicating between the module and the NAOqi runtime
try:
    pythonBroker = ALBroker("pythonBroker", "0.0.0.0", 0, nao_IP, port)
    global AudioCapture
    AudioCapture = AudioCaptureModule("AudioCapture") # create an instance of the AudioCaptureModule class
except RuntimeError:
    print("Error initializing broker!")
    exit(1)


@app.route('/start_listening', methods=['POST'])
def start_listening():
    print("Received a request to start listening")
    AudioCapture.start_listening()
    return jsonify(success=True)

@app.route('/stop_listening', methods=['POST'])
def stop_listening():
    print("Received a request to stop listening")
    AudioCapture.stop_listening()
    return jsonify(success=True)

@app.route('/get_audio_chunk', methods=['GET'])
def get_audio_chunk():
    print("Received a request to get an audio chunk")
    audio_data = AudioCapture.get_audio_chunk()
    if audio_data is not None:
        return audio_data  # Send the audio data as a response
    else:
        print("Server buffer is empty, waiting for audio data...")
        while audio_data is None: # Wait until audio data is available
            audio_data = AudioCapture.get_audio_chunk()
            time.sleep(0.025)
        return audio_data

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5004)
