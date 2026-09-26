import serial
import csv
import time
from pathlib import Path


# ============================================================
# PROJECT PATH
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[1]

DATASET_DIR = BASE_DIR / "dataset"
DATASET_DIR.mkdir(exist_ok=True)

FILE_NAME = DATASET_DIR / "mpu6050_dataset.csv"


# ============================================================
# ESP32 SETTINGS
# ============================================================

PORT = "COM14"          # CHANGE THIS
BAUD_RATE = 115200

SAMPLES = 200


# ============================================================
# HEADER
# ============================================================

print("\n======================================")
print("      MPU6050 DATASET COLLECTOR")
print("======================================")


# ============================================================
# SELECT CLASS
# ============================================================

print("\nSelect the class:")
print("1 - Still")
print("2 - Moving")

choice = input("\nEnter choice: ").strip()

if choice == "1":
    label = "Still"

elif choice == "2":
    label = "Moving"

else:
    print("Invalid choice!")
    raise SystemExit


print("\nSelected class:", label)


# ============================================================
# CONNECT TO ESP32
# ============================================================

try:

    ser = serial.Serial(
        PORT,
        BAUD_RATE,
        timeout=1
    )

except serial.SerialException as error:

    print("\nCould not connect to ESP32.")
    print("Check the COM port.")
    print("Error:", error)

    raise SystemExit


time.sleep(2)

ser.reset_input_buffer()


# ============================================================
# OPEN DATASET
# ============================================================

file_exists = FILE_NAME.exists()
file_empty = not file_exists or FILE_NAME.stat().st_size == 0

file = open(
    FILE_NAME,
    "a",
    newline=""
)

writer = csv.writer(file)


if file_empty:

    writer.writerow([
        "Ax",
        "Ay",
        "Az",
        "Label"
    ])


# ============================================================
# COUNTDOWN
# ============================================================

print("\nGet ready...")

for i in range(3, 0, -1):

    print(i)

    time.sleep(1)


# ============================================================
# COLLECT DATA
# ============================================================

print("\nCollecting data...")
print("Class:", label)

count = 0

try:

    while count < SAMPLES:

        line = ser.readline().decode(
            "utf-8",
            errors="ignore"
        ).strip()

        if not line:
            continue

        # Ignore CSV header
        if line.startswith("Ax"):
            continue

        values = line.split(",")

        if len(values) != 3:
            continue

        try:

            Ax = float(values[0])
            Ay = float(values[1])
            Az = float(values[2])

        except ValueError:

            continue


        writer.writerow([
            Ax,
            Ay,
            Az,
            label
        ])

        count += 1

        print(
            f"{count:03d}/{SAMPLES} | "
            f"Ax={Ax:7.2f} | "
            f"Ay={Ay:7.2f} | "
            f"Az={Az:7.2f} | "
            f"{label}"
        )

except KeyboardInterrupt:

    print("\nCollection stopped by user.")


finally:

    file.close()
    ser.close()


print("\n======================================")
print("       DATA COLLECTION COMPLETE")
print("======================================")

print("\nDataset saved to:")
print(FILE_NAME)