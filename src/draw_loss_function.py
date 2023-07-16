import matplotlib.pyplot as plt
import os
import pathlib
import json


data = [
{'loss': 1.4153, 'learning_rate': 2.9999999999999997e-05, 'epoch': 6.67},
{'loss': 1.3955, 'learning_rate': 5.9999999999999995e-05, 'epoch': 13.33},
{'loss': 1.3266, 'learning_rate': 8.999999999999999e-05, 'epoch': 20.0},
{'loss': 1.211, 'learning_rate': 0.00011999999999999999, 'epoch': 26.67},
{'loss': 1.1373, 'learning_rate': 0.00015, 'epoch': 33.33},
{'loss': 1.0875, 'learning_rate': 0.00017999999999999998, 'epoch': 40.0},
{'loss': 1.0102, 'learning_rate': 0.00020999999999999998, 'epoch': 46.67},
{'loss': 0.874, 'learning_rate': 0.00023999999999999998, 'epoch': 53.33},
{'loss': 0.7375, 'learning_rate': 0.00027, 'epoch': 60.0},
{'loss': 0.5561, 'learning_rate': 0.0003, 'epoch': 66.67},
{'loss': 0.3376, 'learning_rate': 0.00027, 'epoch': 73.33},
{'loss': 0.1605, 'learning_rate': 0.00023999999999999998, 'epoch': 80.0},
{'loss': 0.0559, 'learning_rate': 0.00020999999999999998, 'epoch': 86.67},
{'loss': 0.0202, 'learning_rate': 0.00017999999999999998, 'epoch': 93.33},
{'loss': 0.0108, 'learning_rate': 0.00015, 'epoch': 100.0},
{'loss': 0.008, 'learning_rate': 0.00011999999999999999, 'epoch': 106.67},
{'loss': 0.0069, 'learning_rate': 8.999999999999999e-05, 'epoch': 113.33},
{'loss': 0.0065, 'learning_rate': 5.9999999999999995e-05, 'epoch': 120.0},
{'loss': 0.0062, 'learning_rate': 2.9999999999999997e-05, 'epoch': 126.67},
{'loss': 0.0062, 'learning_rate': 0.0, 'epoch': 133.33},
]

# split the data
epochs = [item['epoch'] for item in data]
losses = [item['loss'] for item in data]
learning_rates = [item['learning_rate'] for item in data]

# plot loss against epoch
plt.figure(figsize=(10, 5))
plt.plot(epochs, losses, 'o-')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Loss over Epochs')


IMAGE_DIR = pathlib.Path(__file__).parent.parent / "data" / "images"
IMAGE_FILE = IMAGE_DIR / "loss_function.png"

os.makedirs(IMAGE_DIR, exist_ok=True)

# save the figure into the 'data' directory
plt.savefig(IMAGE_FILE)