import random

from triple_des import encrypt_Text

def generate_Dummy_Electricity_Data():
    # generate random total_trade
    total_trades = random.choice(range(0, 15))
    cipher_trade = encrypt_Text(str(total_trades))
    # Generate random energy consumption per hour
    energy_consumption = round(random.uniform(0.1, 50), None)
    cipher_energy = encrypt_Text(str(energy_consumption))
    # Generate random cost consumption per hour
    cost_consumption = round(random.uniform(5,100),None)
    cipher_cost = encrypt_Text(str(cost_consumption))
    # Generate random some other stats value
    other = random.randint(0, 50)
    cipher_other = encrypt_Text(str(other))
    # Generate random access grants
    access_grants = random.randint(0, 50)
    cipher_grants = encrypt_Text(str(access_grants))
    # Generate random access rejected
    access_rejected = random.randint(0, 50)
    cipher_rejected = encrypt_Text(str(access_rejected))

    # Print the data
    # print(f"Total trades: {total_trades}, Energy: {energy_consumption } wh/hour, Cost: {cost_consumption} wh/hour, Other: {other}, Access Grants: {access_grants}, Access rejected: {access_rejected}")

    return cipher_trade, cipher_energy, cipher_cost, cipher_other, cipher_grants, cipher_rejected

        

