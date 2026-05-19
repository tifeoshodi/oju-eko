import carla

def main():
    try:
        client = carla.Client('localhost', 2000)
        client.set_timeout(10.0)
        print(f"Connected to CARLA version: {client.get_server_version()}")
        print(f"Client version: {client.get_client_version()}")
        
        world = client.get_world()
        print(f"Current map: {world.get_map().name}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    main()
