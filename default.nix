
with (import <nixpkgs> {});
  let myghc = haskellPackages.ghcWithPackages (pkgs: with pkgs; [ hakyll ]);
  in
stdenv.mkDerivation {
  name = "lambda_site";
  src = ./.;
  buildInputs = [ myghc ];
}
