{ pkgs, modulesPath, lib, ... }:

{
  imports = [
    "${modulesPath}/installer/cd-dvd/installation-cd-minimal.nix"

    ./branding.nix
  ];

  users.motd = "";
  environment.etc."issue".text = ''
    To start the installation, type nixinstall.
  '';

  networking.hostName = "eselanix";

  networking.networkmanager.enable = true;

  environment.systemPackages = with pkgs; [
    python3
    networkmanager
    curl
    git
  ];

  nixpkgs.config.allowUnfree = true;
  hardware.enableAllFirmware = true;


  environment.etc."nixinstall.py".text = builtins.readFile ./nix-install.py;
  environment.etc."branding.nix".text = builtins.readFile ./branding.nix;
  environment.etc."eselanix.txt".text = builtins.readFile ./eselanix.txt;

  environment.shellAliases = {
    nixinstall = "sudo python3 /etc/nixinstall.py";
  };
}