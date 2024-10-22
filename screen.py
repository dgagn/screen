import subprocess


def get_xrandr_output():
    """Run xrandr and return its output as a string."""
    result = subprocess.run(['xrandr'], capture_output=True, text=True)
    return result.stdout


def parse_xrandr_output(output):
    """Parse xrandr output to check if HDMI-1 is connected and to find its resolution."""
    lines = output.splitlines()
    hdmi_connected = False
    hdmi_resolution = None

    for i, line in enumerate(lines):
        if "HDMI-1 connected" in line:
            hdmi_connected = True
            for res_line in lines[i+1:]:
                if "*" in res_line or "+" in res_line:
                    hdmi_resolution = res_line.split()[0]
                    break
            break
    
    return hdmi_connected, hdmi_resolution


def set_hdmi_to_right_of_edp(hdmi_resolution):
    """Set HDMI-1 to the right of eDP-1 with the provided resolution."""
    if hdmi_resolution:
        subprocess.run(['xrandr', '--output', 'HDMI-1', '--mode', hdmi_resolution, '--right-of', 'eDP-1'])
        print(f"HDMI-1 set to {hdmi_resolution} right of eDP-1.")
    else:
        print("HDMI-1 resolution not supported.")


def disable_hdmi_auto():
    """Run xrandr --auto to reset to the default layout when HDMI-1 is disconnected."""
    subprocess.run(['xrandr', '--auto'])
    print("HDMI-1 is disconnected. Running xrandr --auto to reset display layout.")


def main():
    """Main function to handle the display configuration based on HDMI-1 status."""
    xrandr_output = get_xrandr_output()
    hdmi_connected, hdmi_resolution = parse_xrandr_output(xrandr_output)
    
    if hdmi_connected:
        if hdmi_resolution in ["2560x1080", "1920x1080"]:
            set_hdmi_to_right_of_edp(hdmi_resolution)
        else:
            print(f"Resolution {hdmi_resolution} not supported.")
    else:
        disable_hdmi_auto()


if __name__ == "__main__":
    main()
