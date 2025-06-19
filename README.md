# Steganography Tool for Image File Hiding (NaveenaCrypt)

## Overview
NaveenaCrypt is a web-based steganography tool that allows users to embed secret messages into image files (PNG and BMP formats) and extract hidden messages from them. The application uses advanced encryption techniques to secure the messages before embedding them into images.

## Features
- **Embed Messages**: Hide text messages within images.
- **Extract Messages**: Retrieve hidden messages from images.
- **Encryption**: Optionally encrypt messages using AES encryption before embedding.
- **User-Friendly Interface**: Simple web interface built with Flask.
- **Image Support**: Supports PNG and BMP image formats.

## Requirements
- Python 3.x
- Flask
- Flask-SocketIO
- Pillow (PIL)
- Cryptography

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/naveenaayyanar/Steganography-Tool-for-Image-File-Hiding.git
   cd Steganography-Tool-for-Image-File-Hiding
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
1. Run the application:
   ```bash
   python app.py
   ```

2. Open your web browser and navigate to `http://127.0.0.1:5000`.

3. Use the following features:
   - **Embed Message**: Go to the "Embed Message" page, upload an image, enter the message, and optionally provide a password for encryption.
   - **Extract Message**: Go to the "Extract Message" page, upload an image containing a hidden message, and provide the password if the message was encrypted.

## Example
1. **Embedding a Message**:
   - Select an image file (PNG or BMP).
   - Enter the message you want to hide.
   - Optionally, enter a password for encryption.
   - Click "Embed" to download the encoded image.

2. **Extracting a Message**:
   - Select an image file that contains a hidden message.
   - Optionally, enter the password used for encryption.
   - Click "Extract" to retrieve the hidden message.

## Directory Structure
```
.
├── app.py                # Main application file
├── requirements.txt      # Python dependencies
├── templates             # HTML templates for the web interface
│   ├── embed.html
│   ├── extract.html
│   ├── home.html
│   └── password.html
└── uploads               # Directory for uploaded images
```

## Contributing
Contributions are welcome! If you have suggestions or improvements, please feel free to submit a pull request or open an issue.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Pillow Documentation](https://pillow.readthedocs.io/en/stable/)
- [Cryptography Documentation](https://cryptography.io/en/latest/)
```
