
with (import <nixpkgs> {});
let
  myghc = haskellPackages.ghcWithPackages (pkgs: with pkgs; [ hakyll bitarray directory ]);

  mypython3 = python3.withPackages (python-packages: with python-packages; [
    ipython
    numpy
    matplotlib
    pandas
  ]);
in
  stdenv.mkDerivation {
    name = "lambda_site";
    src = ./.;
    buildInputs = [ myghc mypython3 gnuplot ];
  }
