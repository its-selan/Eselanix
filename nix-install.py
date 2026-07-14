import getpass
import os
import sys
import subprocess

def clear_screen():
    os.system("clear")


# Welcome

def step_1_welcome():
    clear_screen()
    print("Welcome to Nix-install")
    input("Press any key to continue...")

def step_2_language():
    while True:
        clear_screen()
        print("System language")
        print("1. English")
        print("2. Russian")
        
        choice = input("\nEnter the number of the appropriate option:\n").strip()
        
        if choice == "1":
            return "en_US.UTF-8"
        elif choice == "2":
            return "ru_RU.UTF-8"
        else:
            print("\nError. Press Enter to try again.")
            input()

def step_3_disks():
    while True:
        clear_screen()
        print("Disks and partitions")
        print("Available drives on your system:\n")
        
        subprocess.run(['lsblk', '-d', '-o', 'NAME,SIZE'])
        
        disk_input = input("\nEnter the name of the drive (e.g., sda or nvme0n1):\n").strip()
        
        if disk_input:

            full_disk_path = f"/dev/{disk_input}"
            
            if "nvme" in disk_input:
                boot_partition = f"/dev/{disk_input}p1"
                root_partition = f"/dev/{disk_input}p2"
            else:
                boot_partition = f"/dev/{disk_input}1"
                root_partition = f"/dev/{disk_input}2"
            
            while True:
                zram_input = input("\nEnable zramSwap for better performance? (true/false): ").strip().lower()
                if zram_input == "true":
                    zram = "true"
                    break
                elif zram_input == "false":
                    zram = "false"
                    break
                else:
                    print("Error. Please enter 'true' or 'false'.")
                
            return full_disk_path, boot_partition, root_partition, zram
        else:
            print("\nError: Drive name cannot be empty. Press Enter to try again.")
            input()

def step_4_network():
    while True:
        clear_screen()
        print("Checking internet connection...")
        
        result = subprocess.run(['ping', '-c', '1', '-W', '2', '1.1.1.1'], 
                                stdout=subprocess.DEVNULL, 
                                stderr=subprocess.DEVNULL)
        
        if result.returncode == 0:
            print("\n[OK] Internet connection is active!")
            input("\nPress Enter to continue...")
            return True
        else:
            clear_screen()
            print("Internet connection error.")
            print("Connect to the Internet to continue the system installation..")
            print("\nPress Enter to retry...")
            input()

            cmd = input("\nEselanix-sh $ ").strip()

            if cmd:
                print(f"\nRunning: {cmd}\n")
                subprocess.run(cmd, shell=True)


def step_5_timezone():
    while True:
        clear_screen()
        print("Timezone settings")
        print("Select your timezone:")
        print("1. Europe/Moscow")
        print("2. America/New_York")
        print("3. Enter manually")
        
        choice = input("\nEnter the number of your option:\n").strip()
        
        if choice == "1":
            return "Europe/Moscow"
        elif choice == "2":
            return "America/New_York"
        elif choice == "3":
            clear_screen()
            print("Manual Timezone Input")
            print("Example: Europe/London or America/New_York")
            tz_input = input("\nEnter timezone: ").strip()

            zoneinfo_path = f"/usr/share/zoneinfo/{tz_input}"
            
            if tz_input and os.path.exists(zoneinfo_path) and os.path.isfile(zoneinfo_path):
                return tz_input
            else:
                print(f"\nError: '{tz_input}' is not a valid timezone in this system.")
                print("Syntax error. Press Enter to try again.")
                input()
        else:
            print("\nError. Press Enter to try again.")
            input()

def step_6_user():
    while True:
        clear_screen()
        print("User Creation")
        username = input("Enter username for the new user:\n").strip().lower()
        
        if not username or username == "root":
            print("\nError: Invalid username. Press Enter to try again.")
            input()
            continue
            
        print(f"\nEnter password for user '{username}':")
        user_password = getpass.getpass("Password: ")
        user_password_confirm = getpass.getpass("Confirm password: ")
        
        if user_password != user_password_confirm:
            print("\nError: User passwords do not match! Press Enter to try again.")
            input()
            continue
            
        return username, user_password


def step_7_format_and_mount(drive, boot_part, root_part):
    while True:
        clear_screen()
        print("Disk partitioning and formatting")
        print(f"WARNING: Drive '{drive}' will be formatted.")

        confirm = input("\nTo confirm, type 'yes'  or 'n' to abort:\n").strip()
        
        if confirm == "n" or confirm == "N":
            print("\nInstallation aborted by user. Exiting...")
            sys.exit(0)
        elif confirm == "yes":
            clear_screen()
            print("Processing disks...")
            
            commands = [
                f"parted -s {drive} mklabel gpt",
                f"parted -s {drive} mkpart ESP fat32 1MiB 513MiB",
                f"parted -s {drive} set 1 esp on",
                f"parted -s {drive} mkpart primary ext4 513MiB 100%",
                f"udevadm settle",
                f"mkfs.vfat -F 32 {boot_part}",
                f"mkfs.ext4 -F {root_part}",
                f"mount {root_part} /mnt",
                "mkdir -p /mnt/boot",
                f"mount {boot_part} /mnt/boot"
            ]
            
            for cmd in commands:
                    print(f"[REAL] Running: {cmd}")
                    result = subprocess.run(cmd, shell=True)
                    if result.returncode != 0:
                        print(f"\n[ERROR] Command failed: {cmd}")
                        input("\nPress Enter to exit.")
                        sys.exit(1)
            
            print("\n[OK] Disk formatting and mounting completed.")
            input("\nPress Enter to continue.")
            return True
        else:
            print("\nError: You must type 'yes' exactly to confirm. Press Enter to try again.")
            input()


def step_8_install(lang, tz, username, user_password, zram):
    clear_screen()
    print("Generating configuration & installation.")
    
    config_dir = "/mnt/etc/nixos"
    config_file = f"{config_dir}/configuration.nix"
    

    nix_config_content = f"""

{{ config, pkgs, ... }}:

{{
  imports = [ ./hardware-configuration.nix
              ./branding.nix
            ];

  boot.loader.systemd-boot.enable = true;
  boot.loader.efi.canTouchEfiVariables = true;


  zramSwap.enable = {zram};
  zramSwap.memoryPercent = 50;
  zramSwap.algorithm = "zstd";

  networking.hostName = "eselanix";
  networking.networkmanager.enable = true;

  time.timeZone = "{tz}";

  i18n.defaultLocale = "{lang}";

  users.users.{username} = {{
    isNormalUser = true;
    description = "{username}";
    extraGroups = [ "networkmanager" "wheel" ];
    initialPassword = "{user_password}";
  }};


  environment.systemPackages = with pkgs; [
    python3
    networkmanager
  ];

  nixpkgs.config.allowUnfree = true;
  hardware.enableAllFirmware = true;

  system.stateVersion = "24.05";
}}
"""

    try:
        os.makedirs(config_dir, exist_ok=True)

        subprocess.run("cp /etc/branding.nix /mnt/etc/nixos/branding.nix", shell=True, check=True)
        subprocess.run("cp /etc/eselanix.txt /mnt/etc/nixos/eselanix.txt", shell=True, check=True)
        
        print("Generating hardware configuration...")
        subprocess.run("nixos-generate-config --root /mnt", shell=True, check=True)
            
        print("Writing configuration.nix...")
        with open(config_file, "w") as f:
             f.write(nix_config_content)
            
        print("Installing ... This will take some time.")
        subprocess.run("nixos-install", shell=True, check=True)
        
        print("\n[SUCCESS] Eselanix has been installed successfully")
        print("You can reboot into the installed system.")
    except Exception as e:
        print(f"\n[ERROR] Installation failed: {e}")
        sys.exit(1)


def main():
    step_1_welcome()

    LANG = step_2_language()
    
    DRIVE, BOOT_PART, ROOT_PART, ZRAM = step_3_disks()

    IS_CONNECTED = step_4_network()

    TZ = step_5_timezone()

    USERNAME, USER_PASSWORD = step_6_user()

    step_7_format_and_mount(DRIVE, BOOT_PART, ROOT_PART)

    step_8_install(LANG, TZ, USERNAME, USER_PASSWORD, ZRAM)
    
    clear_screen()
    input("Press Enter to continue.")

if __name__ == "__main__":
    main()