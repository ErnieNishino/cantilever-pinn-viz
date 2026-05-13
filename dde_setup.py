import os

# Ensure DeepXDE uses PyTorch backend before importing deepxde.
os.environ.setdefault("DDE_BACKEND", "pytorch")
