{
  description = "WCA competition announcement email notifications";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};

        python = pkgs.python3.withPackages (ps: with ps; [
          pandas
          openpyxl
          requests
          python-dotenv
          pytz
        ]);

        competition-notifications = pkgs.stdenvNoCC.mkDerivation {
          pname = "competition-notifications";
          version = "0.1.0";
          src = pkgs.lib.fileset.toSource {
            root = ./.;
            fileset = pkgs.lib.fileset.fileFilter (f: f.hasExt "py") ./.;
          };

          nativeBuildInputs = [ pkgs.makeWrapper ];

          installPhase = ''
            runHook preInstall
            mkdir -p $out/share/competition-notifications $out/bin
            cp *.py $out/share/competition-notifications/
            makeWrapper ${python}/bin/python $out/bin/competition-notifications \
              --add-flags $out/share/competition-notifications/main.py
            runHook postInstall
          '';

          meta.mainProgram = "competition-notifications";
        };
      in
      {
        packages.default = competition-notifications;

        apps.default = flake-utils.lib.mkApp { drv = competition-notifications; };

        devShells.default = pkgs.mkShell {
          packages = [ python ];
        };
      });
}
