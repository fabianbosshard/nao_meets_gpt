# NAO meets GPT

## Overview
This project involves the integration of a NAO robot with an advanced language model (GPT) to enable sophisticated human-robot interactions. The system is divided into two main components: a Python server (`body.py`) that interacts directly with the NAO robot, and a Python client (`brain.py`) that handles speech recognition, communication with GPT, and orchestrates the overall interaction.

### `body.py` - Server Component
This component is responsible for audio capture, text-to-speech functionality, and managing audio data. It uses the `NAOqi` framework for robot operations.

Key Features:
- Audio capture from NAO's microphones
- Text-to-speech functionality for NAO
- Communication with the client component via Flask API

### `brain.py` - Client Component
This component runs separately and is responsible for processing and responding to human speech using GPT. 

Key Features:
- Speech recognition using Google's API
- Communication with OpenAI's GPT for generating responses
- Sending recognized speech to GPT and relaying responses back to the server

## Getting Started

### Requirements
- NAO Robot
- Python 3.x environment (for client component)
- Python 2.7 environment (for server component)
- OpenAI API key for GPT access

### Setup
1. **Install Dependencies**: Ensure all required Python libraries are installed in your environments.
2. **Configure Environment Variables**: Create a `.env` and set your OpenAI API key in the `.env` file.
3. **Turn on NAO**: Turn on the NAO robot and connect it to a router with an Ethernet cable.
4. **Connect to the router**: Connect your machine via Ethernet to the same router as the NAO robot.
5. **Run the Server**: Execute `body.py` in your Python 2.7 environment to start the Flask server. The server will manage audio input/output with the NAO robot.
6. **Run the Client**: Execute `brain.py` in your Python 3.x environment. This script will start listening for speech, process it, and interact with GPT for generating responses.
7. **Talk to the NAO robot**: Speak to the NAO robot. The system will capture your speech, transcribe it, and send it to GPT. The generated response from GPT will be spoken by the NAO robot.

## Conclusion
This project demonstrates an innovative way to enhance human-robot interaction using state-of-the-art AI technology. By leveraging the capabilities of GPT, the NAO robot can engage in more natural and sophisticated conversations.