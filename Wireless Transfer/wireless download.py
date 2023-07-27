import os
from flask import Flask, render_template, send_from_directory

app = Flask(__name__)

# The directory path to serve files from
FILES_PATH = os.path("File Path") #replace with file path

@app.route("/")
def index():
    # List all files in the directory
    files = os.listdir(FILES_PATH)
    return render_template("wireless download.html", files=files)


# This route handles file downloads
@app.route("/download/<filename>")
def download(filename):
    # Get the full path to the file
    filepath = os.path.join(FILES_PATH, filename)

    # Check if the file exists and is a file (not a directory)
    if os.path.isfile(filepath):
        # If the file exists, send it as an attachment for download
        return send_from_directory(FILES_PATH, filename, as_attachment=True)
    else:
        # If the file does not exist, return an error message
        return f"File '{filename}' not found."


if __name__ == "__main__":
    # Start the Flask app, listening on all available network interfaces
    app.run(host="0.0.0.0")
