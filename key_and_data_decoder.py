import base64

def decode_key_and_data(secret_key_b64, encrypted_data_b64):
    """Decodes base64-encoded key and data."""
    secret_key = base64.b64decode(secret_key_b64)
    encrypted_data = base64.b64decode(encrypted_data_b64)
    return secret_key, encrypted_data

# Example usage (optional - for testing this file independently):
if __name__ == "__main__":
    secret_key_b64 = "tHIyCsPF7a7KaFlWlKud6pqhR4A5ZPmlaSLjb5DiJYc="
    encrypted_data_b64 = "gAAAAABnJKOeon8_hI1Jg17iGztNKnY4AL3PrcPhO5_pPnKQNgxzMn55Peo-dQcuuzqPgw64imPkxTpLBHb1byLdeI_P9B_bhw=="
    secret_key, encrypted_data = decode_key_and_data(secret_key_b64, encrypted_data_b64)
    print(f"Decoded Secret Key: {secret_key}")
    print(f"Decoded Encrypted Data: {encrypted_data}")