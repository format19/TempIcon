"""Temperature reader module for CPU temperature sensors."""

import os
import glob
import subprocess


class TemperatureReader:
    """Read CPU temperature from system sensors."""

    def __init__(self):
        self.sensor_path = "/sys/class/hwmon/"

    def get_cpu_temperature(self):
        """
        Read average CPU temperature from hwmon sensors.

        Returns:
            float: Average temperature in Celsius, or None if no data available
        """
        temps = []

        try:
            # Try reading from hwmon sysfs interface
            hwmon_dirs = glob.glob(os.path.join(self.sensor_path, "hwmon*"))

            for hwmon_dir in hwmon_dirs:
                # Look for temp*_input files
                temp_files = glob.glob(os.path.join(hwmon_dir, "temp*_input"))

                for temp_file in temp_files:
                    try:
                        with open(temp_file, "r") as f:
                            # Temperature is in millidegrees Celsius
                            temp_milli = int(f.read().strip())
                            temps.append(temp_milli / 1000.0)
                    except (IOError, ValueError):
                        continue

            if temps:
                return sum(temps) / len(temps)

        except Exception:
            pass

        # Fallback: try lm-sensors if available
        try:
            result = subprocess.run(
                ["sensors", "-u"], capture_output=True, text=True, timeout=5
            )

            if result.returncode == 0:
                for line in result.stdout.split("\n"):
                    if "Core" in line or "Package" in line:
                        parts = line.split(":")
                        if len(parts) == 2:
                            try:
                                temp = float(parts[1].strip().split()[0])
                                temps.append(temp)
                            except ValueError:
                                continue

                if temps:
                    return sum(temps) / len(temps)

        except (subprocess.TimeoutExpired, FileNotFoundError):
            pass

        return None

    def get_color_for_temp(self, temp):
        """
        Return RGB color tuple based on temperature.

        Args:
            temp: Temperature in Celsius

        Returns:
            tuple: (red, green, blue) values 0-255
        """
        if temp is None:
            return (128, 128, 128)  # Gray for error/unknown

        if temp < 50:
            # Green: below 50°C
            return (0, 200, 0)
        elif temp < 80:
            # Amber: 50-80°C
            return (255, 165, 0)
        else:
            # Red: 80°C and above
            return (200, 0, 0)

    def get_status_text(self, temp):
        """
        Get status text based on temperature.

        Args:
            temp: Temperature in Celsius

        Returns:
            str: Status description
        """
        if temp is None:
            return "ERROR: No sensor data"

        if temp < 50:
            return "Normal"
        elif temp < 80:
            return "Warm"
        else:
            return "Hot"
