**Frontend Logics Used in Your Repository**

 **1. Navigation Logic**
- **Purpose**: Allow users to navigate between different sections of the application (home, embed, extract).
- **Implementation**:
  - The navigation links in `home.html` provide access to the embed and extract functionalities.
  - Example:
    ```html
    <nav>
      <a href="{{ url_for('embed') }}">Embed Message</a> |
      <a href="{{ url_for('extract') }}">Extract Message</a>
    </nav>
    ```

 **2. Form Submission Logic**
- **Purpose**: Submit the image and message data to the backend without refreshing the page.
- **Implementation**:
  - The forms in `embed.html` and `extract.html` use the POST method to send data to the Flask backend.
  - Example for embedding a message:
    ```html
    <form action="{{ url_for('embed') }}" method="POST" enctype="multipart/form-data">
        <input type="file" name="image" accept=".png, .bmp" required>
        <textarea name="message_text" placeholder="Enter your message" required></textarea>
        <input type="password" name="password" placeholder="Optional: Enter password for encryption">
        <button type="submit">Embed Message</button>
    </form>
    ```

 **3. Input Validation Logic**
- **Purpose**: Ensure that user inputs are valid before submission, such as checking for empty fields or valid file types.
- **Implementation**:
  - Basic validation can be done using HTML attributes like `required` and `accept` in the form inputs.
  - Example:
    ```html
    <input type="file" name="image" accept=".png, .bmp" required>
    ```

 **4. Flash Messages Logic**
- **Purpose**: Provide feedback to users about the success or failure of their actions (e.g., successful embedding or errors).
- **Implementation**:
  - Flask's `flash` function is used to send messages to the frontend, which can be displayed in the templates.
  - Example in `extract.html`:
    ```html
    {% with messages = get_flashed_messages() %}
      {% if messages %}
        <ul>
          {% for message in messages %}
            <li>{{ message }}</li>
          {% endfor %}
        </ul>
      {% endif %}
    {% endwith %}
    ```

 **5. Displaying Extracted Messages Logic**
- **Purpose**: Show the extracted message from the image after decoding.
- **Implementation**:
  - The extracted message is displayed conditionally based on whether it was successfully retrieved.
  - Example in `extract.html`:
    ```html
    {% if extracted_message %}
      <h2>Extracted Message:</h2>
      <p>{{ extracted_message }}</p>
    {% endif %}
    ```

 **6. Responsive UI Updates**
- **Purpose**: Improve user experience by providing visual feedback during processing (e.g., loading indicators).
- **Implementation**:
  - While not explicitly shown in the provided code, you can implement loading indicators using JavaScript or CSS to show that the application is processing the request.

 **7. Encryption Logic (Optional)**
- **Purpose**: Allow users to encrypt their messages before embedding them in the image.
- **Implementation**:
  - The password input field in the embed form allows users to provide a password for encryption.
  - The backend handles the encryption using AESGCM before embedding the message in the image.

**Conclusion**
The frontend logic in your repository is designed to create an interactive and user-friendly experience for your steganography web application. 
It handles user inputs, manages form submissions, provides visual feedback, and communicates effectively with the backend. 
