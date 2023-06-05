import random

from triple_des import encrypt_Text


def generate_Dummy_Room_Data(user_id):
    # all rooms
    loads = ['Load 1', 'Load 2','Load 3','Load 4','Green Load', 'GTI','Invertor','Grid']

    data = []
    current_total = 0
    power_total = 0
    for a in loads:
        cipher_load_type = encrypt_Text(str(a))
        # Generate random energy consumption per hour for a room
        v = random.randint(225, 235)
        f = random.randint(45, 55)
        pf = round(random.uniform(0.85, 0.95), 1)
        i = random.randint(1,4)
        p = round(v*i*pf, 1)

        current_total += i
        power_total += p

        # encryption of values
        cipher_v = encrypt_Text(str(v)); cipher_f = encrypt_Text(str(f))
        cipher_pf = encrypt_Text(str(pf)); cipher_i = encrypt_Text(str(i))
        cipher_p = encrypt_Text(str(p)); cipher_current_total = encrypt_Text(str(round(current_total, 1)))
        cipher_power_total = encrypt_Text(str(round(power_total, 1)))

        data.append({
            "load_type": cipher_load_type,
            "volt": cipher_v,
            "frequency": cipher_f,
            "power_factor": cipher_pf,
            "current": cipher_i,
            "power": cipher_p,
            "current_total": cipher_current_total,
            "power_total": cipher_power_total,
            "user_id": user_id
        })
        # Print the data
        # print(f"Room: {current_room}, Energy: {a_energy_consumption} wh/hour, Temp: {a_temp} C")

    return data

