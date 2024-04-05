{ pkgs ? import (fetchTarball "https://github.com/NixOS/nixpkgs/tarball/nixos-unstable") { } }:
#{ pkgs ? import (fetchTarball "https://github.com/NixOS/nixpkgs/tarball/nixos-23.11") {} }:

let
  dontCheckPython = drv: drv.overridePythonAttrs (old: { doCheck = false; });
in

pkgs.mkShellNoCC {
  packages = with pkgs; [
    (python3.withPackages (
      ps: with ps; [
        ipdb
        ipython
        pprintpp
        pygments
        textual
        pandas
        numpy
        requests
        absl-py
      ]
    ))
  ];
  PYTHONBREAKPOINT = "ipdb.set_trace";
}
