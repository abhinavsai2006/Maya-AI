import pyaudio

try:
    p = pyaudio.PyAudio()
    device_count = p.get_device_count()
    
    print(f"\n=== Audio Devices Found: {device_count} ===\n")
    
    for i in range(device_count):
        info = p.get_device_info_by_index(i)
        print(f"Device {i}: {info.get('name')}")
        print(f"  Max Input Channels: {info.get('maxInputChannels')}")
        print(f"  Max Output Channels: {info.get('maxOutputChannels')}")
        print(f"  Default Sample Rate: {info.get('defaultSampleRate')}")
        print()
    
    # Try to find default input device
    try:
        default_input = p.get_default_input_device_info()
        print(f"✓ Default Input Device: {default_input['name']}")
    except Exception as e:
        print(f"✗ No default input device found: {e}")
    
    p.terminate()
    print("\n✓ PyAudio is working!")
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    print("\nTroubleshooting:")
    print("1. Check if microphone is connected")
    print("2. Check Windows microphone permissions")
    print("3. Try reinstalling PyAudio: pip install --force-reinstall pyaudio")
