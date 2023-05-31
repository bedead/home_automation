from names import get_full_name
import random

def generate_Dummy_Trade_History():
    # Generate random full name
    full_name = get_full_name()

    # Generate random email
    random_email_provider  = ['@example.com', '@gmail.com','@yahoo.com','@abc.com','@hotmail.com']
    email = full_name.replace(" ", "").lower() + random.choice(random_email_provider)

    # Generate random energy consumption
    energy_consumption = round(random.uniform(0.1, 50), 2)

    # Print the data
    # print(f"Full Name: {full_name}, Email: {email}, Energy Consumption: {energy_consumption} wh/hour")

    return full_name, email, energy_consumption
    

        

