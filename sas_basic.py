import numpy as np
import matplotlib.pyplot as plt

def generate_sas_image():
    # --- PARAMETERS ---
    c = 1500  # Speed of sound in water (meters/second)
    f0 = 30000  # Center frequency of sonar pulse (Hz)
    sampling_rate = 1e6  # Sampling rate for signal (samples/second)
    pulse_length = 1e-3  # Length of the sonar pulse (seconds)
    wavelength = c / f0  # Wavelength of the sonar pulse (meters)

    # --- GRID AND SONAR PATH ---
    x_positions = np.linspace(-10, 10, 200)  # Sonar moves along x-axis from -10 to 10 meters (200 positions)
    z = 10  # Sonar altitude above seabed (meters), constant for all positions

    # --- SEABED REFLECTORS (TARGETS) ---
    targets = [(0, 15), (-5, 18), (6, 13)]  # List of (x, z) positions for point reflectors on seabed

    # --- TIME AXIS AND TRANSMIT PULSE ---
    t = np.arange(0, 2 * z / c, 1 / sampling_rate)  # Time axis: covers round-trip time to max depth
    # Generate a windowed sinusoidal pulse (Hanning window reduces sidelobes)
    pulse = np.sin(2 * np.pi * f0 * t) * np.hanning(len(t))

    # --- ECHO SIMULATION ---
    echo_data = []  # Will store simulated echoes for each sonar position
    for x in x_positions:
        echo = np.zeros_like(t)  # Initialize echo signal for this sonar position
        for tx, tz in targets:
            # Calculate distance from sonar (at x, z) to target (tx, tz)
            r = np.sqrt((x - tx)**2 + (z - tz)**2)
            # Calculate round-trip delay in samples
            delay = int((2 * r / c) * sampling_rate)
            if delay < len(t):
                echo[delay] += 1  # Add a delta (impulse) at the delay corresponding to this target
        # Convolve echo with transmit pulse to simulate received signal
        echo_data.append(np.convolve(echo, pulse, mode='same'))
    echo_data = np.array(echo_data)  # Convert list to 2D numpy array: shape (num_positions, num_samples)

    # --- IMAGE RECONSTRUCTION VIA BACKPROJECTION ---
    image_size = 200  # Output image will be 200x200 pixels
    image = np.zeros((image_size, image_size))  # Initialize empty image
    x_grid = np.linspace(-10, 10, image_size)  # X-coordinates for image grid
    z_grid = np.linspace(0, 30, image_size)    # Z-coordinates (depth) for image grid

    # For each pixel in the output image:
    for i, x in enumerate(x_grid):
        for j, zz in enumerate(z_grid):
            # For each sonar position:
            for k, sx in enumerate(x_positions):
                # Calculate distance from sonar position to image pixel
                r = np.sqrt((sx - x)**2 + (z - zz)**2)
                # Calculate round-trip delay in samples
                delay = int((2 * r / c) * sampling_rate)
                # If delay is within the recorded echo, add its value to the image pixel
                if delay < echo_data.shape[1]:
                    image[j, i] += echo_data[k, delay]

    # --- PLOTTING ---
    plt.imshow(
        image,
        extent=[-10, 10, 30, 0],  # X from -10 to 10, Z from 0 (top) to 30 (bottom)
        cmap='inferno'
    )
    plt.title("Synthetic Aperture Sonar Image")
    plt.xlabel("X (meters)")
    plt.ylabel("Z (meters)")
    plt.colorbar(label='Intensity')
    plt.show()

if __name__ == "__main__":
    generate_sas_image()