from flask import Flask, request, jsonify
from naoqi import ALProxy, ALModule, ALBroker
import time

app = Flask(__name__)

nao = True
nao_IP = "nao.local"
nao_port = 9559
sleep_time = 0.01

tts = ALProxy("ALTextToSpeech", nao_IP, nao_port)
tts.setVolume(1.0) # define volume of the robot
animatedSpeech = ALProxy("ALAnimatedSpeech", nao_IP, nao_port)
 

class AudioCaptureModule(ALModule): # NAOqi module for capturing audio
    """ 
    This is a custom module built on top of NAOqi framework for managing audio capture from NAO's microphones.
    It extends ALModule class from the NAOqi framework and defines methods to to start and stop audio capture, process audio data, and retrieve audio chunks. 
    """
    def __init__(self, name):
        ALModule.__init__(self, name)
        self.audio_device = ALProxy("ALAudioDevice", nao_IP, nao_port)
        self.is_listening = False
        self.buffers = []

    def start_listening(self):
        self.audio_device.setClientPreferences(self.getName(), 16000, 3, 0) # sample rate of 16000 Hz, channelparam 3 (front channel), and a deinterleaving flag of 0 (only relevant for channelparam 0 (all channels))
        self.audio_device.subscribe(self.getName())
        self.is_listening = True

    def stop_listening(self):
        self.audio_device.unsubscribe(self.getName())
        self.is_listening = False

    def processRemote(self, nbOfChannels, nbOfSamplesByChannel, timeStamp, inputBuffer): # callback method that is triggered whenever new audio data is available
        print("received audio data from NAO with the following parameters: nbOfChannels = " + str(nbOfChannels) + ", nbOfSamplesByChannel = " + str(nbOfSamplesByChannel) + ", timeStamp = " + str(timeStamp[0]) + " sec " + str(timeStamp[1]) + " musec" + ", length of inputBuffer = " + str(len(inputBuffer)))
        if self.is_listening:
            self.buffers.append(inputBuffer)

    def get_audio_chunk(self):
        if self.buffers:
            return self.buffers.pop(0) # return the oldest audio chunk
        else:
            print("no audio data available")
            return None


try:
    pythonBroker = ALBroker("pythonBroker", "0.0.0.0", 0, nao_IP, nao_port) # broker connection: essential for communicating between the module and the NAOqi runtime
    global AudioCapture
    AudioCapture = AudioCaptureModule("AudioCapture") # create an instance of the AudioCaptureModule class
    print("AudioCapture module initialized")
except RuntimeError:
    print("Error initializing broker!")
    exit(1)


# server endpoints ====================================================================================================

@app.route("/talk", methods=["POST"])
def talk():
    print("Received a request to talk")
    message = request.json.get("message")
    animatedSpeech.say(str(message))
    return jsonify(success=True)

@app.route("/start_listening", methods=["POST"])
def start_listening():
    print("Received a request to start listening, current length of server buffer:", len(AudioCapture.buffers))
    AudioCapture.start_listening()
    return jsonify(success=True)

@app.route("/stop_listening", methods=["POST"])
def stop_listening():
    print("Received a request to stop listening, current length of server buffer:", len(AudioCapture.buffers))
    AudioCapture.stop_listening()
    return jsonify(success=True)

@app.route("/get_audio_chunk", methods=["GET"])
def get_audio_chunk():
    print("Received a request to get an audio chunk, current length of server buffer:", len(AudioCapture.buffers))
    audio_data = AudioCapture.get_audio_chunk()
    if audio_data is not None:
        return audio_data  # send the audio data as a response
    else:
        print("Server buffer is empty, waiting for audio data...")
        while audio_data is None: # wait until audio data is available
            audio_data = AudioCapture.get_audio_chunk()
            time.sleep(sleep_time)
        return audio_data
    
@app.route("/get_server_buffer_length", methods=["GET"])
def get_server_buffer_length():
    print("Received a request to print the length of the server buffer, current length of server buffer:", len(AudioCapture.buffers))
    return jsonify(length=len(AudioCapture.buffers))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5004)