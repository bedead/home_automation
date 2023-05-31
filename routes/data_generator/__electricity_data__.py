import random

def generate_Dummy_Electricity_Data():
    # generate random total_trade
    total_trades = random.choice(range(0, 15))
    # Generate random energy consumption per hour
    energy_consumption = round(random.uniform(0.1, 50), 2)
    # Generate random cost consumption per hour
    cost_consumption = round(random.uniform(5,100),3)
    # Generate random some other stats value
    other = random.randint(0, 50)
    # Generate random access grants
    access_grants = random.randint(0, 50)
    # Generate random access rejected
    access_rejected = random.randint(0, 50)

    # Print the data
    # print(f"Total trades: {total_trades}, Energy: {energy_consumption} wh/hour, Cost: {cost_consumption} wh/hour, Other: {other}, Access Grants: {access_grants}, Access rejected: {access_rejected}")

    return total_trades, energy_consumption, cost_consumption, other, access_grants, access_rejected

        

