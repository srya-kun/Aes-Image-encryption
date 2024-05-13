# app.py

import os
import uuid
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'  # Set a secure secret key for session management

# MySQL configuration (replace with your actual credentials)
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Svp@0906.me',
    'database': 'aes_project',
}

# Initialize MySQL connection
db_connection = mysql.connector.connect(**db_config)
cur = db_connection.cursor()

# Encryption setup
encryption_key = get_random_bytes(32)

# Upload route
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' in request.files:
            file = request.files['file']
            if file.filename != '':
                filename = secure_filename(file.filename)
                # Save the file (modify this part)
                file.save(os.path.join('uploads', filename))

                # Encrypt the image (modify this part)
                unique_id, encrypted_filename = encrypt_image(filename)

                # Store the encrypted image and key in the database (modify this part)
                insert_image_into_db(unique_id, encrypted_filename, encryption_key)

                return f"File '{filename}' uploaded and encrypted successfully!"
    return render_template('upload.html')

# Encryption logic (modify this part)
def encrypt_image(filename):
    # Read the image data
    with open(os.path.join('uploads', filename), 'rb') as f:
        image_data = f.read()

    # Encrypt the image using AES (for demonstration)
    iv = get_random_bytes(AES.block_size)
    cipher = AES.new(encryption_key, AES.MODE_CBC, iv)
    encrypted_image = cipher.encrypt(pad(image_data, AES.block_size))

    # Generate a unique identifier (UUID)
    unique_id = str(uuid.uuid4())

    # Save the encrypted image with the unique identifier in the filename
    encrypted_filename = f"enc_{unique_id}_{filename}"
    with open(os.path.join('uploads', encrypted_filename), 'wb') as f:
        f.write(encrypted_image)

    return unique_id, encrypted_filename # Return the UUID and encrypted filename

# Insert image and key into the database (modify this part)
def insert_image_into_db(unique_id, encrypted_filename,encryption_key):
    # Implementing MySQL 'insert logic' here:
    print("Inserting into database")
    cur.execute("INSERT INTO test_table(uuid, encrypted_filename, encryption_key) VALUES (%s, %s, %s)", (unique_id, encrypted_filename, encryption_key))
    db_connection.commit()


if __name__ == '__main__':
    app.run(debug=True)
