# NAO Meets GPT

## Overview
![Alt text](image.png)
This project involves the integration of a NAO robot with an advanced language model (GPT) to enable sophisticated human-robot interactions. The system is divided into two main components: a Python server (`body.py`) that interacts directly with the NAO robot, and a Python client (`brain.py`) that handles speech-to-text processing, communication with GPT, and orchestrates the overall interaction by making requests to the server.

### `body.py`: Server Component
This component is responsible for interacting with NAO, i.e., text-to-speech,audio capture, and sending audio chunks to `brain.py` for speech-to-text processing. It uses the `NAOqi` framework for robot operations.

### `brain.py`: Client Component
This component runs separately and is responsible for speech recognition from the audio chunks as well as processing the recognized text using GPT. It sends the generated response from GPT to the server component for text-to-speech.

## Getting Started

### Requirements
- NAO Robot
- NAO Python SDK
- Python 3.x environment (for client component)
- Python 2.7 environment (for server component)
- OpenAI API key for GPT access

### Setup
1. **Install the NAO Python SDK**: Follow the instructions [here](https://support.aldebaran.com/support/solutions/articles/80001017327-python-sdk-installation-guide) to install the NAO Python SDK.
2. **Python Environments**: Create two separate Python environments, one for the server component and one for the client component. The server component requires Python 2.7, while the client component requires Python 3.x.
3. **Install Dependencies**: Ensure all required Python libraries are installed in your environments.
4. **Configure Environment Variables**: Create a `.env` file and set your OpenAI API key in this file.
5. **Turn on the NAO Robot**: Turn on the NAO robot and connect it to a router with an Ethernet cable.
6. **Connect to the Router**: Connect your machine to the router via Ethernet.
7. **Run the Server**: Run `body.py` in your Python 2.7 environment to start the Flask server. The server will manage audio input/output with the NAO robot.
8. **Run the Client**: Run `brain.py` in your Python 3.x environment. This script will start listening for speech, process it, and interact with GPT for generating responses.
9. **Talk to the NAO Robot**: Speak to the NAO robot. The system will capture your speech, transcribe it, and send it to GPT. The generated response from GPT will be spoken by the NAO robot.

## Conclusion
This project demonstrates an innovative way to enhance human-robot interaction using a state-of-the-art AI technology. By leveraging the capabilities of GPT, the NAO robot can engage in more natural and sophisticated conversations.
