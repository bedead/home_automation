from names import get_full_name
import random
from triple_des import encrypt_Text

def generate_Dummy_Trade_History():
    # Generate random full name
    full_name = get_full_name()
    cipher_name = encrypt_Text(full_name)

    # Generate random email
    random_email_provider  = ['@example.com', '@gmail.com','@yahoo.com','@abc.com','@hotmail.com']
    email = full_name.replace(" ", "").lower() + random.choice(random_email_provider)
    cipher_email = encrypt_Text(email)
    # Generate random energy consumption
    energy_consumption = round(random.uniform(0.1, 50), None)
    cipher_energy = encrypt_Text(str(energy_consumption))
    # Print the data
    # print(f"Full Name: {full_name}, Email: {email}, Energy Consumption: {energy_consumption} wh/hour")

    return cipher_name, cipher_email, cipher_energy
    

        

