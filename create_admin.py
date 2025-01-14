import pickle
import bcrypt

def create_admin_pkl():
    admin_username = input("Enter admin username: ")
    admin_password = input("Enter admin password: ").encode()

    # Hash the admin password
    hashed_password = bcrypt.hashpw(admin_password, bcrypt.gensalt())

    # Save admin credentials in a dictionary
    admin_credentials = {
        "username": admin_username,
        "password": hashed_password
    }

    # Save the admin credentials to admin.pkl
    with open("admin.pkl", "wb") as f:
        pickle.dump(admin_credentials, f)

    print("admin.pkl file created successfully!")

if __name__ == "__main__":
    create_admin_pkl()
