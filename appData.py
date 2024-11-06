import streamlit as st
import pandas as pd
import csv
from cryptography.fernet import Fernet, InvalidToken, InvalidSignature
import os

# Function to load the encryption key
def load_key():
    try:
        with open('secret.key', 'rb') as file:
            return file.read()
    except FileNotFoundError:
        st.error("Encryption key file ('secret.key') not found. Run the app once to generate it.")
        return None

# Generate and save a random encryption key if it doesn't exist
if not os.path.exists('secret.key'):
    key = Fernet.generate_key()
    with open('secret.key', 'wb') as file:
        file.write(key)
        st.success("Encryption key generated and saved to secret.key")

key = load_key()

if key:
    cipher_suite = Fernet(key)

    st.title("Sales Data Entry and Encryption App")

    # Input fields for product information
    product_name = st.text_input("Product Name")
    quantity = st.number_input("Quantity", min_value=1)
    price = st.number_input("Price (in Saudi Riyal)", min_value=10, step=1, format="%d")

    # Button to save the data
    if st.button("Save"):
        try:
            # Encrypt the data
            data = f"{product_name},{quantity},{price}"
            encrypted_data = cipher_suite.encrypt(data.encode())

            # Save the encrypted data to a CSV file using append mode
            with open('sales_data.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([encrypted_data.decode()])  # Add each new data as a new row
            st.success("Data saved successfully!")
        except Exception as e:
            st.error(f"Error saving data: {e}")

    # Button to read and display data
    if st.button("Read and Display Data"):
        if os.path.exists('sales_data.csv'):
            try:
                df = pd.read_csv('sales_data.csv', header=None)
                decrypted_data = []
                for index, row in df.iterrows():
                    try:
                        decrypted_text = cipher_suite.decrypt(row[0].encode()).decode()
                        decrypted_data.append(decrypted_text.split(','))
                    except (InvalidToken, InvalidSignature) as e:
                        st.error(f"Error decrypting row {index + 1}: {e}. Check your key or data file.")
                        continue
                df_decrypted = pd.DataFrame(decrypted_data, columns=['product', 'quantity', 'price'])
                st.dataframe(df_decrypted)
            except Exception as e:
                st.error(f"An error occurred while reading the data: {e}")
        else:
            st.info("No sales data found.")
