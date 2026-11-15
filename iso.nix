{ pkgs, modulesPath, lib, ... }:

{
  imports = [
    "${modulesPath}/installer/cd-dvd/installation-cd-minimal.nix"
  ];

  system.nixos.distroName = "Eselanix";
  system.nixos.distroId = "eselanix";

  users.motd = "";
  environment.etc."issue".text = ''
    
    \e[1;35mWelcome to Eselanix.\e[0m
    You are using version 1.0.1 \e[1;35m(stable)\e[0m.
    To start the installation, type "eselanix-install".
  '';

  networking.hostName = "eselanix";

  networking.networkmanager.enable = true;

  environment.systemPackages = with pkgs; [
    python3
    curl
    git
    openssl
  ];

  nixpkgs.config.allowUnfree = true;
  hardware.enableAllFirmware = true;

  environment.etc."os-release".text = ''
    NAME="Eselanix"
    VERSION="1.0.1"
    ID=eselanix
    ID_LIKE=nixos
    PRETTY_NAME="Eselanix 1.0.1"
  '';

  isoImage.isoBaseName = lib.mkForce "Eselanix-1.0.1-x86_64-linux";
  isoImage.volumeID = lib.mkForce "Eselanix-1.0.1-x86_64-linux.iso";
  isoImage.isoName = lib.mkForce "Eselanix-1.0.1-x86_64-linux.iso";

  environment.etc."eselanix-install.py".text = builtins.readFile ./eselanix-install.py;
  environment.etc."branding.nix".text = builtins.readFile ./branding.nix;
  environment.etc."eselanix.txt".text = builtins.readFile ./eselanix.txt;

  environment.shellAliases = {
    eselanix-install = "sudo python3 /etc/eselanix-install.py";
  };

}
