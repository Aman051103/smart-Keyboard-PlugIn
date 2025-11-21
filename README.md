# Smart Keyboard

A smart keyboard application with AI-powered next-word prediction using TensorFlow/Keras. The application features a GUI built with tkinter that provides word recommendations as you type.

**Repository:** https://github.com/Aman051103/smart-Keyboard-PlugIn

## Features

- **Next-word prediction**: AI-powered suggestions based on your typing context
- **Interactive GUI**: Dark-themed keyboard interface with clickable word recommendations
- **Dynamic recommendations**: Real-time word suggestions that update as you type
- **Keyboard shortcuts**: 
  - Space: Shows recommendations after a word
  - Backspace: Updates recommendations dynamically
  - Ctrl+Backspace: Deletes the last word

## Requirements

- Python 3.7 or higher
- TensorFlow 2.x
- NumPy
- tkinter (usually included with Python, but may need `python3-tk` on Linux)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/Aman051103/smart-Keyboard-PlugIn.git
cd smart-keyboard-PlugIn
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Ensure you have the required model files:
   - `nexpree1.keras` - The trained model file
   - `tokenizer.pkl` - The tokenizer file used during training

## Usage

Run the application using:

```bash
python runner.py
```

Or directly:

```bash
python main.py
```

## How It Works

1. Type text in the input field or use the on-screen keyboard
2. After pressing space or typing, the application predicts the next word based on your input
3. Click on any recommended word to insert it into your text
4. The model uses the entire sentence context to provide accurate predictions

## Docker Usage

Build the Docker image:

```bash
docker build -t smart-keyboard .
```

Run the container (requires X11 forwarding on Linux):

```bash
# On Linux with X11
docker run -it --rm -e DISPLAY=$DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix smart-keyboard

# On Windows/Mac, you may need additional setup for GUI applications
```

## Project Structure

```
smart-keyboard/
├── main.py              # Main application code
├── runner.py            # Entry point
├── nexpree1.keras       # Trained model file
├── tokenizer.pkl        # Tokenizer file
├── requirements.txt     # Python dependencies
├── Dockerfile           # Docker configuration
└── README.md           # This file
```

## Notes

- The model expects sequences with a maximum length of 107 tokens
- The application provides the top 4 word predictions
- Make sure both `nexpree1.keras` and `tokenizer.pkl` are in the same directory as the application

## Troubleshooting

- **ImportError for tkinter**: On Linux, install `python3-tk` package
- **Model not found**: Ensure `nexpree1.keras` exists in the project directory
- **Tokenizer not found**: Ensure `tokenizer.pkl` exists in the project directory
- **Docker GUI issues**: For GUI applications in Docker, you may need to set up X11 forwarding or use a virtual display

## License

This project is licensed under the MIT License.
