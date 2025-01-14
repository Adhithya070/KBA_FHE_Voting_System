# Fully Homomorphic Voting System

## Overview
A secure and privacy-preserving voting system implemented using Fully Homomorphic Encryption (FHE). This project allows users to cast votes anonymously, ensuring that votes remain encrypted throughout the process. The final results can only be decrypted by the admin, preserving the integrity and confidentiality of the system.

---

## Features
- 🔐 **Secure User Authentication**: User registration and login secured using JWT.
- 🛡️ **Encrypted Voting**: Votes are encrypted using FHE and stored securely.
- 🧑‍💼 **Admin Control**: Results can only be accessed via admin credentials.
- 🗑️ **Automatic Data Clearing**: User data is cleared upon system termination while retaining admin information.

---

## Technologies Used
- 🖥️ **Python 3.12.6**: Programming language.: Programming language.
- 🌐 **Flask**: Backend framework for creating APIs.
- 🧬 **TenSEAL**: Library for implementing Fully Homomorphic Encryption.
- 🔒 **bcrypt**: For secure password hashing.
- 🛠️ **JWT (PyJWT)**: For generating and verifying authentication tokens.
- 📦 **pickle**: For lightweight data storage.

---

## Data Flow
1. 📝 **Registration**: Users register with a username and password.
2. 🔑 **Login**: Users log in using their credentials to obtain a JWT token.
3. 🗳️ **Voting**: Users cast encrypted votes via the `/vote` endpoint.
4. 🧑‍💼 **Admin Results**: The admin logs in to decrypt and view the results.
5. 💾 **Shutdown**: User data (votes and credentials) is cleared when the program stops.

---

## How to Run the Program

### Prerequisites
Ensure the following are installed:
- 🖥️ Python 3.12.6
- 🌐 Flask (`pip install flask`)
- 🔒 bcrypt (`pip install bcrypt`)
- 🛠️ PyJWT (`pip install pyjwt`)
- 🧬 TenSEAL (`pip install tenseal`)

### Steps to Execute
1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Create Admin Credentials**:
   Run the following command to create the `admin.pkl` file:
   ```bash
   python create_admin.py
   ```

4. **Run the Application**:
   ```bash
   python flask_app.py
   ```
   The server will run on `http://127.0.0.1:5000` by default.

5. **Testing**:
   Use Postman or any REST client to test the API endpoints. Refer to the API documentation below.

---

## API Endpoints

### **User Registration**
- **POST** `/register`
- **Payload**:
  ```json
  {
    "username": "example",
    "password": "password123"
  }
  ```
- **Response**: User registration confirmation.

### **User Login**
- **POST** `/login`
- **Payload**:
  ```json
  {
    "username": "example",
    "password": "password123"
  }
  ```
- **Response**: JWT token for authentication.

### **Vote**
- **POST** `/vote`
- **Payload**:
  ```json
  {
    "token": "<JWT_TOKEN>",
    "vote": 1
  }
  ```
- **Response**: Vote confirmation.

### **Results** (Admin Only)
- **POST** `/results`
- **Payload**:
  ```json
  {
    "token": "<JWT_TOKEN>",
    "admin_password": "<admin_password>"
  }
  ```
- **Response**: Voting results.

---

## File Structure
```
project-root
├── create_admin.py      # Script to create admin credentials
├── encryption.py        # FHE implementation functions
├── flask_app.py         # Main application file
├── votes.pkl            # Stores encrypted votes and user credentials
├── admin.pkl            # Stores admin credentials
├── requirements.txt     # List of dependencies
```

---

## Future Scope
- 🌍 **Decentralized Architecture**: Integrate blockchain for immutable vote storage.
- 📈 **Scalability**: Adapt the system for large-scale elections.
- 💻 **User Interface**: Build a user-friendly web or mobile app for better accessibility.
- 📊 **Advanced Analytics**: Implement real-time voting statistics for admins.

---

## Version Compatibility
- 🐍 **Python**: 3.12.6
- 🌐 **Flask**: 2.0+
- 🔒 **bcrypt**: 3.2.2
- 🛠️ **PyJWT**: 2.6.0
- 🧬 **TenSEAL**: 0.4+

---

## Contributing
We welcome contributions! Please fork the repository and submit a pull request.

---

## Contact
For questions or feedback, please reach out to **adhithyasraj7@gmail.com**

