{
  description = "A Nix-flake-based Python development environment";

  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixpkgs-unstable";

  outputs = { self, nixpkgs }:
    let
      supportedSystems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      forEachSupportedSystem = f: nixpkgs.lib.genAttrs supportedSystems (system: f {
        pkgs = import nixpkgs { inherit system; };
      });
    in
    {
      devShells = forEachSupportedSystem ({ pkgs }: {
        default = pkgs.mkShell {
          shellHook = ''
            export PIP_PREFIX=$(pwd)/_build/pip_packages
            export PYTHONPATH="$PIP_PREFIX/${pkgs.python3.sitePackages}:$PYTHONPATH"
            export PATH="$PIP_PREFIX/bin:$PATH"
            export NLTK_DATA=./corpora/
            unset SOURCE_DATE_EPOCH
          '';
          packages = with pkgs; [ python311 virtualenv poetry ] ++
            (with pkgs.python311Packages; [
              pip
              # poetry-core
              llama-index
              # # llama-index-llms-ollama
              # qdrant-client
              # torch
              # transformers
              # (python3.pkgs.buildPythonPackage {
              #   pname = "llama-index-llms-ollama";
              #   version = "";
              #   src = "${repo}/llama-index-integrations/llms/llama-index-llms-ollama";
              #   format = "pyproject";
              #   doCheck = false;
              #   propogatedBuildInputs = [
              #     # llama-hub
              #     mypy
              #     llama-index-core
              #   ];
              # })
            ]);
        };
      });
    };
}
