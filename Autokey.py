# 1. SETUP: 32-Character Dictionary
# Using A-Z and 1-6 to fill exactly 5 bits (2^5 = 32)
CHAR_MAP = "ABCDEFGHIJKLMNOPQRSTUVWXYZ123456"
dict1 = {char: i for i, char in enumerate(CHAR_MAP)}
dict2 = {i: char for i, char in enumerate(CHAR_MAP)}

# 2. UTILITY: The Masking Logic
def derive_salt(password):
    """Generates a 5-bit salt (0-31) based on a Master Password."""
    return sum(ord(c) for c in password) % 32

def scramble_key(raw_key_idx, salt):
    """Applies the secret mask to the key index."""
    return (raw_key_idx ^ salt) % 32

# 3. CORE: Encryption Function
def encrypt_message(message, primer, password):
    salt = derive_salt(password)
    ciphertext = ""
    # In Autokey, the key stream is: Primer + Message
    # We strip spaces from the key source but use them in the final output
    key_source = (primer + message).replace(" ", "")
    
    k_idx = 0
    for char in message:
        if char == " ":
            ciphertext += " " # Option 1: Literal space preservation
        else:
            # Step A: Mask the key character
            raw_key_idx = dict1[key_source[k_idx]]
            masked_key = scramble_key(raw_key_idx, salt)
            
            # Step B: XOR Target (Plaintext) with the Masked Key
            target_idx = dict1[char]
            cipher_idx = target_idx ^ masked_key
            
            # Step C: Convert back to character
            ciphertext += dict2[cipher_idx]
            k_idx += 1
    return ciphertext

# 4. CORE: Decryption Function
def decrypt_message(ciphertext, primer, password):
    salt = derive_salt(password)
    decrypted_text = ""
    # Receiver starts with only the primer to begin reconstruction
    current_key_stream = list(primer.replace(" ", ""))
    
    k_idx = 0
    for char in ciphertext:
        if char == " ":
            decrypted_text += " "
        else:
            # Step A: Re-generate the masked key
            raw_key_idx = dict1[current_key_stream[k_idx]]
            masked_key = scramble_key(raw_key_idx, salt)
            
            # Step B: XOR Cipher character with Masked Key to reveal Plaintext
            cipher_idx = dict1[char]
            plain_idx = cipher_idx ^ masked_key
            
            # Step C: Recovery and Feedback Loop
            recovered_char = dict2[plain_idx]
            decrypted_text += recovered_char
            
            # Autokey logic: The recovered char is added to the key for the NEXT step
            current_key_stream.append(recovered_char)
            k_idx += 1
    return decrypted_text

# 5. EXECUTION: Main Flow
def main():
    # User Inputs
    plaintext = "MISSION ACCOMPLISHED 1"
    primer = "OMNI"
    password = "SECURE_PASSWORD_2026"
    
    # Process
    encrypted = encrypt_message(plaintext, primer, password)
    decrypted = decrypt_message(encrypted, primer, password)
    
    # Display Results
    print(f"--- 5-Bit Masked Autokey Cipher ---")
    print(f"Master Password: {password}")
    print(f"Derived Salt:    {derive_salt(password)}")
    print(f"Original Text:   {plaintext}")
    print("-" * 35)
    print(f"Ciphertext:      {encrypted}")
    print(f"Decrypted:       {decrypted}")

if __name__ == "__main__":
    main()
