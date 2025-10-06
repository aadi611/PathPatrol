"""Test path construction"""
from pathlib import Path
from config.settings import DATABASE_DIR, UPLOAD_DIR

# Simulate what storage_service does
upload_dir = UPLOAD_DIR
relative_path = "uploads/pothole_20251006_001711_d6a978ea.jpg"

# Method in storage_service
path_method_1 = upload_dir.parent / relative_path
print(f"Storage Service Method:")
print(f"  upload_dir.parent: {upload_dir.parent}")
print(f"  relative_path: {relative_path}")
print(f"  Result: {path_method_1}")
print(f"  Exists: {path_method_1.exists()}")
print()

# Alternative methods
path_method_2 = DATABASE_DIR / relative_path
print(f"Alternative Method (DATABASE_DIR):")
print(f"  DATABASE_DIR: {DATABASE_DIR}")
print(f"  Result: {path_method_2}")
print(f"  Exists: {path_method_2.exists()}")
print()

path_method_3 = UPLOAD_DIR / Path(relative_path).name
print(f"Alternative Method (filename only):")
print(f"  UPLOAD_DIR: {UPLOAD_DIR}")
print(f"  Filename: {Path(relative_path).name}")
print(f"  Result: {path_method_3}")
print(f"  Exists: {path_method_3.exists()}")
