import random
import time
import csv
from datetime import datetime

# Electricity tariff in ₹ per kWh
TARIFF = 6.50

# Total energy consumed
total_energy_kwh = 0.0

CSV_FILE = "energy_data.csv"


def read_sensor_data():
    """
    Simulate voltage and current sensor readings.

    For a real project, replace this function with
    readings from suitable voltage/current measurement hardware.
    """

    voltage = random.uniform(220, 240)
    current = random.uniform(1, 15)

    return voltage, current


def calculate_power(voltage, current):
    """Calculate approximate power in watts."""
    return voltage * current


def calculate_energy(power, elapsed_seconds):
    """Calculate energy consumed in kWh."""
    return (power * elapsed_seconds) / 3_600_000


def calculate_cost(energy):
    """Calculate estimated electricity cost."""
    return energy * TARIFF


def initialize_csv():
    """Create CSV file with column headers."""

    try:
        with open(CSV_FILE, "x", newline="") as file:
            writer = csv.writer(file)

            writer.writerow([
                "Timestamp",
                "Voltage_V",
                "Current_A",
                "Power_W",
                "Energy_kWh",
                "Cost_Rs"
            ])

    except FileExistsError:
        pass


def save_data(timestamp, voltage, current, power, energy, cost):
    """Save energy data to CSV."""

    with open(CSV_FILE, "a", newline="") as file:
        writer = csv.writer(file)

        writer.writerow([
            timestamp,
            round(voltage, 2),
            round(current, 2),
            round(power, 2),
            round(energy, 6),
            round(cost, 2)
        ])


def main():
    global total_energy_kwh

    initialize_csv()

    previous_time = time.time()

    print("=" * 65)
    print("             HOME ENERGY MONITORING SYSTEM")
    print("=" * 65)

    try:
        while True:

            voltage, current = read_sensor_data()

            power = calculate_power(voltage, current)

            current_time = time.time()
            elapsed_seconds = current_time - previous_time
            previous_time = current_time

            energy = calculate_energy(
                power,
                elapsed_seconds
            )

            total_energy_kwh += energy

            cost = calculate_cost(total_energy_kwh)

            timestamp = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )

            save_data(
                timestamp,
                voltage,
                current,
                power,
                total_energy_kwh,
                cost
            )

            print("\n----------------------------------------")
            print(f"Time        : {timestamp}")
            print(f"Voltage     : {voltage:.2f} V")
            print(f"Current     : {current:.2f} A")
            print(f"Power       : {power:.2f} W")
            print(f"Energy      : {total_energy_kwh:.6f} kWh")
            print(f"Cost        : ₹{cost:.2f}")
            print("----------------------------------------")

            time.sleep(5)

    except KeyboardInterrupt:

        print("\nMonitoring stopped.")
        print(
            f"Total Energy: {total_energy_kwh:.6f} kWh"
        )
        print(
            f"Estimated Cost: ₹{cost:.2f}"
        )


if __name__ == "__main__":
    main()
