import random
from encrypt import  encrypt_Text

def generate_Dummy_Room_Data(user_id):
    # all rooms
    rooms = ['Living room', 'Bedroom','Kitchen','Bathroom 1','Bathroom 2']

    data = []

    for a in rooms:
        current_room = encrypt_Text(str(a))
        # Generate random energy consumption per hour for a room
        a_energy_consumption = round(random.uniform(0.1, 50), None)
        cipher_energy = encrypt_Text(str(a_energy_consumption))
        # Generate random temperature for a room
        a_temp = random.randint(1,50)
        cipher_temp = encrypt_Text(str(a_temp))

        data.append({
            "room": current_room,
            "wh_hour": cipher_energy,
            "temp": cipher_temp,
            "user_id": user_id
        })
        # Print the data
        # print(f"Room: {current_room}, Energy: {a_energy_consumption} wh/hour, Temp: {a_temp} C")

    return data

