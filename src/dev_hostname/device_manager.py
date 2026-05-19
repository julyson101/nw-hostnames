from netmiko import ConnectHandler
import logging

logger = logging.getLogger(__name__)


class DeviceConnectionError(Exception):
    pass


def get_hostname(device):
    """
    Connect to a network device and return hostname.
    Handles Cisco IOS and can be extended for other platforms.
    """

    # ✅ Use name if available, fallback to host
    device_name = device.get("name", device.get("host"))

    try:
        logger.info(f"Connecting to {device_name} ({device['host']})")

        # ✅ Filter only valid Netmiko parameters
        connection_params = {
            key: device[key]
            for key in ["device_type", "host", "username", "password", "secret"]
            if key in device
        }

        with ConnectHandler(**connection_params) as conn:

            command = "show running-config | include hostname"
            output = conn.send_command(command)

            if "hostname" in output:
                hostname = output.split()[1]

                logger.info(f"{device_name} ({device['host']}) hostname: {hostname}")
                return hostname

            logger.warning(f"No hostname found on {device_name} ({device['host']})")
            return None

    except Exception as e:
        logger.error(f"Failed to connect to {device_name} ({device['host']}): {e}")
        raise DeviceConnectionError(f"{device_name} connection failed") from e

