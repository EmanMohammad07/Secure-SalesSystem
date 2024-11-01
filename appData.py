import streamlit as st
import pandas as pd
import csv #Import the csv module
from cryptography.fernet import Fernet, InvalidToken, InvalidSignature
import os #Import the os module for file handling


# Function to load the encryption key (Handles file not found)
def load_key():
    try:
        with open('secret.key', 'rb') as file:
            return file.read()
    except FileNotFoundError:
        st.error("Encryption key file ('secret.key') not found.  Run the app once to generate it.")
        return None

# Generate and save a random encryption key (only if it doesn't exist)
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
    price = st.number_input("Price", min_value=10)

    # Button to save the data
    if st.button("Save"):
        try:
            # Encrypt the data
            data = f"{product_name},{quantity},{price}"
            encrypted_data = cipher_suite.encrypt(data.encode())

            # Save the encrypted data to a CSV file using the csv module
            with open('sales_data.csv', 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([encrypted_data.decode()])
            st.success("Data saved successfully!")
        except Exception as e:
            st.error(f"Error saving data: {e}")


    if st.button("Read and Display Data"):
        try:
            df = pd.read_csv('sales_data.csv', header=None)
            decrypted_data = []
            for index, row in df.iterrows(): #More efficient iteration
                try:
                    decrypted_text = cipher_suite.decrypt(row[0].encode()).decode()
                    decrypted_data.append(decrypted_text.split(','))
                except (InvalidToken, InvalidSignature) as e:
                    st.error(f"Error decrypting row {index + 1}: {e}. Check your key or data file.")
                    continue
            df_decrypted = pd.DataFrame(decrypted_data, columns=['product', 'quantity', 'price'])
            st.dataframe(df_decrypted)
        except FileNotFoundError:
            st.info("No sales data found.")
        except Exception as e:
            st.error(f"An error occurred: {e}")
