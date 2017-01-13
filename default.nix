#!/usr/bin/env nix-shell

with import <nixpkgs> {};

let
    envname = "py35";
    python = python35;
    pyp = python35Packages;
    pys = with pyp; [
    readline
    numpydoc
    virtualenv
    setuptools
    requests2
  ];
in

stdenv.mkDerivation { 
  name = "${envname}-env";
  propagatedBuildInputs = [
     python
     stdenv
     git
     pys
     zsh
    ];
  src = null;
  # When used as `nix-shell --pure`
  shellHook = ''
  export NIX_ENV="[${envname}] "
  '';
  # used when building environments
  extraCmds = ''
  export NIX_ENV="[${envname}] "
  '';
}

