{ config, pkgs, lib, ... }:

{
  users.motd = "";
  environment.etc."issue".text = "";
  services.getty.extraArgs = [ "--nohints" "--nohostname" ];
  
  system.nixos.distroName = "Eselanix";
  system.nixos.distroId = "eselanix";

  environment.interactiveShellInit = lib.mkForce ''
    if [ "$TERM" = "linux" ]; then echo -e "\e[1;35mWelcome to Eselanix.\e[0m"; echo -e "You are using version 1.0.0 \e[1;35m(stable)\e[0m."; echo ""; fi
  '';

  environment.etc."fastfetch/eselanix.txt".text = builtins.readFile ./eselanix.txt;
  environment.etc."fastfetch/config.jsonc".text = ''
    {
      "$schema": "https://github.com/fastfetch-cli/fastfetch/raw/dev/doc/json_schema.json",
      "logo": {
        "source": "/etc/fastfetch/eselanix.txt",
        "color": {
          "1": "#FF8E8E"
        }
      },
      "modules": [
        "title",
        "separator",
        "os",
        "host",
        "kernel",
        "uptime",
        "packages",
        "shell",
        "display",
        "de",
        "wm",
        "wmtheme",
        "theme",
        "icons",
        "font",
        "cursor",
        "terminal",
        "terminalfont",
        "cpu",
        "gpu",
        "memory",
        "swap",
        "disk",
        "localip",
        "battery",
        "poweradapter",
        "locale",
        "break",
        "colors"
      ]
    }
  '';

  environment.etc."os-release".text = ''
    NAME="Eselanix"
    VERSION="1.0.0"
    ID=eselanix
    ID_LIKE=nixos
    PRETTY_NAME="Eselanix 1.0.0"
  '';
}
