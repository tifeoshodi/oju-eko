import carla
import multiprocessing
import os
import time
import numpy as np
import csv
from datetime import datetime

# Configuration as per PRD
CAM_CONFIG = {
    # 'front_long': {'fov': 60, 'res': (640, 480), 'pos': carla.Transform(carla.Location(x=2.0, z=1.5))},
    'front_wide': {'fov': 120, 'res': (640, 480), 'pos': carla.Transform(carla.Location(x=2.1, z=1.5))},
    # 'rear': {'fov': 100, 'res': (640, 480), 'pos': carla.Transform(carla.Location(x=-2.0, z=1.5), carla.Rotation(yaw=180))}
}

def img_saver_process(queue, name, out_dir):
    """Sub-process dedicated to saving images for a specific camera."""
    while True:
        data = queue.get()
        if data is None: break  # Poison pill
        
        timestamp, image_raw = data
        filename = os.path.join(out_dir, f"{name}/{timestamp}.png")
        
        # In a real rig, we'd use hardware encoding. 
        # Here we simulate the I/O load.
        image_raw.save_to_disk(filename)

def telemetry_saver_process(queue, out_dir):
    """Sub-process for logging GPS and IMU data to CSV."""
    csv_path = os.path.join(out_dir, "telemetry.csv")
    with open(csv_path, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "lat", "lon", "alt", "accel_x", "accel_y", "accel_z", "gyro_x", "gyro_y", "gyro_z"])
        
        while True:
            data = queue.get()
            if data is None: break
            writer.writerow(data)

def main():
    out_dir = "out"
    os.makedirs(out_dir, exist_ok=True)
    for cam in CAM_CONFIG: os.makedirs(os.path.join(out_dir, cam), exist_ok=True)

    # Initialize Queues and Processes
    queues = {name: multiprocessing.Queue() for name in CAM_CONFIG}
    tel_queue = multiprocessing.Queue()
    
    processes = []
    for name in CAM_CONFIG:
        p = multiprocessing.Process(target=img_saver_process, args=(queues[name], name, out_dir))
        p.start()
        processes.append(p)
    
    tp = multiprocessing.Process(target=telemetry_saver_process, args=(tel_queue, out_dir))
    tp.start()
    processes.append(tp)

    try:
        client = carla.Client('localhost', 2000)
        client.set_timeout(10.0)
        world = client.get_world()
        blueprint_library = world.get_blueprint_library()

        # Spawn ego vehicle
        ego_bp = blueprint_library.find('vehicle.tesla.model3')
        spawn_point = world.get_map().get_spawn_points()[0]
        ego_vehicle = world.spawn_actor(ego_bp, spawn_point)
        ego_vehicle.set_autopilot(True)

        # Attach Cameras
        actors = [ego_vehicle]
        for name, cfg in CAM_CONFIG.items():
            bp = blueprint_library.find('sensor.camera.rgb')
            bp.set_attribute('image_size_x', str(cfg['res'][0]))
            bp.set_attribute('image_size_y', str(cfg['res'][1]))
            bp.set_attribute('fov', str(cfg['fov']))
            bp.set_attribute('sensor_tick', '0.033') # ~30 FPS
            
            cam = world.spawn_actor(bp, cfg['pos'], attach_to=ego_vehicle)
            # Use a lambda to capture the queue and name
            cam.listen(lambda image, q=queues[name]: q.put((image.timestamp, image)))
            actors.append(cam)

        # Attach IMU & GPS
        imu_bp = blueprint_library.find('sensor.other.imu')
        gps_bp = blueprint_library.find('sensor.other.gnss')
        
        imu = world.spawn_actor(imu_bp, carla.Transform(), attach_to=ego_vehicle)
        gps = world.spawn_actor(gps_bp, carla.Transform(), attach_to=ego_vehicle)
        
        # State tracking for sync (Simplified for Phase 1)
        curr_tel = {}

        def imu_cb(data):
            curr_tel['accel'] = (data.accelerometer.x, data.accelerometer.y, data.accelerometer.z)
            curr_tel['gyro'] = (data.gyroscope.x, data.gyroscope.y, data.gyroscope.z)

        def gps_cb(data):
            if 'accel' in curr_tel:
                tel_queue.put((
                    data.timestamp, data.latitude, data.longitude, data.altitude,
                    *curr_tel['accel'], *curr_tel['gyro']
                ))

        imu.listen(imu_cb)
        gps.listen(gps_cb)
        actors.extend([imu, gps])

        print("Logging started. Press Ctrl+C to stop.")
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nStopping...")
    finally:
        # Cleanup
        for q in queues.values(): q.put(None)
        tel_queue.put(None)
        for p in processes: p.join()
        for actor in actors: actor.destroy()
        print("Cleanup complete.")

if __name__ == '__main__':
    main()
