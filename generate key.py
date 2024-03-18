from cryptography.fernet import Fernet

# Generate an encryption key
key = Fernet.generate_key()
print("Generated Encryption Key:", key)
