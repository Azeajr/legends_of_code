import asyncio
import random
import time

import httpx

API_URL = "http://localhost:8000"
MAP_SIZE = 10


# Utility Functions
async def fetch_players():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{API_URL}/players/")
            response.raise_for_status()
            data = response.json()

            # Extract players from the "players" key
            players_cleaned = {}
            for player_uuid, player_info in data["players"].items():
                players_cleaned[player_uuid] = player_info

            return players_cleaned
        except httpx.RequestError as e:
            print(f"Error fetching players: {e}")
            return {}


async def add_player():
    name = input("Enter player name: ")
    x = random.randint(0, MAP_SIZE - 1)
    y = random.randint(0, MAP_SIZE - 1)
    player = {"name": name, "position": {"x": x, "y": y}}

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{API_URL}/players/add_player/", json=player)
            response.raise_for_status()
            added_player = response.json()
            print(
                f"Player {added_player["name"]} added with UUID {added_player["uuid"]} at position ({x}, {y}).",
            )
        except httpx.RequestError as e:
            print(f"Error adding player: {e}")


async def move_player(player_name, current_position, direction):
    # Define the movement deltas
    delta_map = {"N": (0, 1), "S": (0, -1), "E": (1, 0), "W": (-1, 0)}

    if direction not in delta_map:
        print("Invalid direction. Use N, S, E, or W.")
        return

    delta_x, delta_y = delta_map[direction]
    delta = {"x": delta_x, "y": delta_y}

    # Prepare the JSON body as required by the API
    move_data = {
        "player": {
            "name": player_name,
            "position": current_position,  # Current position is passed in
        },
        "delta": delta,
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{API_URL}/players/move_player/", json=move_data,
            )
            response.raise_for_status()
            updated_player = response.json()
            print(
                f"Player moved {direction}. New position: {updated_player["position"]}",
            )
        except httpx.RequestError as e:
            print(f"Error moving player: {e}")


async def remove_player():
    uuid = input("Enter player UUID to remove: ")

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                f"{API_URL}/players/remove_player/", json={"uuid": uuid},
            )
            response.raise_for_status()
            print(f"Player with UUID {uuid} removed.")
        except httpx.RequestError as e:
            print(f"Error removing player: {e}")


async def print_map():
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f"{API_URL}/maps/print_map/")
            response.raise_for_status()
            map_data = response.json()
            print("\nCurrent Map Layout:")
            for row, contents in map_data.items():
                print(f"{row}: {contents}")
        except httpx.RequestError as e:
            print(f"Error printing map: {e}")


def display_game_map(players):
    # Initialize empty game map
    game_map = [["." for _ in range(MAP_SIZE)] for _ in range(MAP_SIZE)]

    # Place players on the map
    for player_uuid, player_info in players.items():
        x = player_info["position"]["x"]
        y = player_info["position"]["y"]
        game_map[y][x] = player_info["name"][
            0
        ].upper()  # Use the first letter of player's name

    # Display map
    print("\nGame Map:")
    for row in game_map:
        print(" ".join(row))


async def game_loop(player_name, initial_position):
    print(f"Starting game for {player_name}...")

    current_position = initial_position  # Start with the initial position

    while True:
        # Fetch and display the current state of the map and players
        players = await fetch_players()
        display_game_map(players)

        print("\nCommands: N (North), S (South), E (East), W (West), Q (Quit)")
        action = input("Enter your action: ").upper()

        if action in ["N", "S", "E", "W"]:
            await move_player(player_name, current_position, action)
            # Update current_position based on delta movement
            delta_map = {"N": (0, 1), "S": (0, -1), "E": (1, 0), "W": (-1, 0)}
            delta_x, delta_y = delta_map[action]
            current_position["x"] += delta_x
            current_position["y"] += delta_y
        elif action == "Q":
            print("Exiting the game.")
            break
        else:
            print("Invalid command. Try again.")

        time.sleep(1)  # Pause for a moment before the next action


async def main_menu():
    print("Welcome to the CLI Game!")

    while True:
        print("\nMain Menu:")
        print("1. Add Player")
        print("2. Start Game")
        print("3. Remove Player")
        print("4. Print Map")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            await add_player()
        elif choice == "2":
            players = await fetch_players()
            if not players:
                print("No players available. Add a player first.")
                continue
            print("Available players:")
            for player_uuid, player_info in players.items():
                print(
                    f"UUID: {player_uuid}, Name: {player_info["name"]}, Position: {player_info["position"]}",
                )
            player_uuid = input("Enter the UUID of the player you want to play: ")
            if player_uuid in players:
                player_name = players[player_uuid]["name"]
                initial_position = players[player_uuid]["position"]
                await game_loop(player_name, initial_position)
            else:
                print("Invalid UUID. Try again.")
        elif choice == "3":
            await remove_player()
        elif choice == "4":
            await print_map()
        elif choice == "5":
            print("Exiting game.")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    asyncio.run(main_menu())
