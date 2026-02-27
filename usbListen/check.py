import pickle
import numpy as np

# Load the scaler
with open('scaler.pkl', 'rb') as f:
    scaler = pickle.load(f)

# Get parameters
mean = scaler.mean_
scale = scaler.scale_  # This is 1/std, so std = 1/scale

print("Scaler mean:")
print(", ".join([f"{x:.6f}" for x in mean]))

print("\nScaler std (1/scale):")
print(", ".join([f"{x:.6f}" for x in 1/scale]))
