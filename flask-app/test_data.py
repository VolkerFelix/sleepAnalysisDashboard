from datetime import datetime, timedelta
import random
import math
import uuid

def create_test_sleep_data(duration_hours=8, quality="good", sampling_rate=1):
    """
    Generate synthetic sleep data for testing.
    Based on the test data creation function in the original codebase.
    """
    samples = []
    now = datetime.utcnow()
    start_time = now - timedelta(hours=duration_hours)

    # Total samples
    total_samples = int(duration_hours * 3600 * sampling_rate)

    # Generate accelerometer data
    for i in range(total_samples):
        if i % 300 != 0:  # Only process every 300th sample to reduce data size
            continue
        
        timestamp = start_time + timedelta(seconds=i / sampling_rate)

        # Create sleep cycle pattern (roughly 90 minutes per cycle)
        cycle_duration = 90 * 60  # 90 minutes in seconds
        cycle_progress = (i % (cycle_duration * sampling_rate)) / (cycle_duration * sampling_rate)

        # Determine which sleep stage we're simulating
        if quality == "good":
            # Good sleep has clear cycles and lower movement
            if cycle_progress < 0.1:  # Initial falling asleep or transitioning between cycles
                movement_intensity = 0.2 + 0.15 * random.random()  # Moderate movement
                hr = 70 + 10 * random.random()  # Slightly elevated HR
                is_awake = i < (20 * 60 * sampling_rate)  # Awake only in first 20 min
            elif cycle_progress < 0.4:  # Light sleep
                movement_intensity = 0.1 + 0.1 * random.random()
                hr = 65 + 8 * random.random()
                is_awake = False
            elif cycle_progress < 0.7:  # Deep sleep - make very distinct
                movement_intensity = 0.05 + 0.03 * random.random()  # Very low movement
                hr = 55 + 3 * random.random()  # Lower HR with less variability
                is_awake = False
            else:  # REM sleep
                movement_intensity = 0.1 + 0.15 * random.random()  # More variable movement
                hr = 65 + 15 * random.random()  # More variable HR
                is_awake = False
        elif quality == "poor":
            # Poor sleep has fragmented patterns and more movement
            if cycle_progress < 0.2:  # More time falling asleep or transitioning
                movement_intensity = 0.3 + 0.2 * random.random()
                hr = 75 + 15 * random.random()
                is_awake = i < (45 * 60 * sampling_rate) or random.random() < 0.3  # Awake more often
            elif cycle_progress < 0.6:  # More light sleep, less deep
                movement_intensity = 0.15 + 0.15 * random.random()
                hr = 70 + 10 * random.random()
                is_awake = random.random() < 0.05  # Occasional awakening
            elif cycle_progress < 0.75:  # Less deep sleep
                movement_intensity = 0.1 + 0.1 * random.random()
                hr = 60 + 8 * random.random()
                is_awake = random.random() < 0.01  # Rare awakening during deep sleep
            else:  # REM sleep
                movement_intensity = 0.15 + 0.2 * random.random()
                hr = 70 + 15 * random.random()
                is_awake = random.random() < 0.1  # More likely to wake from REM
        else:  # Default moderate quality
            if cycle_progress < 0.15:
                movement_intensity = 0.25 + 0.15 * random.random()
                hr = 72 + 10 * random.random()
                is_awake = i < (30 * 60 * sampling_rate)
            elif cycle_progress < 0.5:
                movement_intensity = 0.12 + 0.12 * random.random()
                hr = 68 + 8 * random.random()
                is_awake = False
            elif cycle_progress < 0.7:
                movement_intensity = 0.08 + 0.07 * random.random()
                hr = 58 + 7 * random.random()
                is_awake = False
            else:
                movement_intensity = 0.12 + 0.18 * random.random()
                hr = 68 + 12 * random.random()
                is_awake = False

        # Calculate accelerometer values
        if is_awake:
            # More movement when awake
            x = 0.3 * math.sin(i / 50) + movement_intensity * (random.random() - 0.5)
            y = 0.3 * math.cos(i / 70) + movement_intensity * (random.random() - 0.5)
            z = 0.9 + 0.2 * math.sin(i / 100) + movement_intensity * (random.random() - 0.5)
        else:
            # Less movement during sleep
            x = 0.1 * math.sin(i / 200) + movement_intensity * (random.random() - 0.5)
            y = 0.1 * math.cos(i / 250) + movement_intensity * (random.random() - 0.5)
            z = 0.95 + 0.05 * math.sin(i / 300) + movement_intensity * (random.random() - 0.5)

        # Add accelerometer sample
        acc_sample = {
            "timestamp": timestamp.isoformat(),
            "sensor_type": "accelerometer",
            "values": {
                "x": x,
                "y": y,
                "z": z,
                "movement_intensity": movement_intensity,
            },
        }
        samples.append(acc_sample)

        # Add heart rate sample every 5 minutes
        if i % (300 * sampling_rate) == 0:
            hr_sample = {
                "timestamp": timestamp.isoformat(),
                "sensor_type": "heart_rate",
                "values": {"bpm": hr},
            }
            samples.append(hr_sample)

            # Also add a respiration sample
            resp_rate = 12 + 4 * random.random()
            if is_awake:
                resp_rate += 2  # Slightly higher respiration when awake

            resp_sample = {
                "timestamp": timestamp.isoformat(),
                "sensor_type": "respiration",
                "values": {"rate": resp_rate},
            }
            samples.append(resp_sample)

    # Create a simplified SleepData object (dict for JSON serialization)
    return type('SleepData', (), {
        'json': lambda: json.dumps({
            "data_type": "sleep_monitoring",
            "device_info": {"device_type": "test", "model": "integration-test"},
            "sampling_rate_hz": 1/300,  # 1 sample per 5 minutes
            "start_time": start_time.isoformat(),
            "end_time": now.isoformat(),
            "samples": samples,
            "id": f"test-data-{uuid.uuid4()}",
        })
    })()