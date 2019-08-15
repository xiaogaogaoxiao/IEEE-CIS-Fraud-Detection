import argparse
import glob

from pathlib import Path

from .google_drive_toolkits import upload


PACKAGE_PATH = Path(__file__).resolve().parent


def add_bool_arg(parser, name, default=False, help_comment=""):
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        "--" + name, dest=name, action="store_true", help=help_comment
    )
    group.add_argument(
        "--no-" + name, dest=name, action="store_false", help=help_comment
    )
    parser.set_defaults(**{name: default})


def main():
    parser = argparse.ArgumentParser(
        description="IEEE-CIS Fraud Detection competition solution builder."
    )
    parser.add_argument(
        "action",
        type=str,
        choices=["upload"]
    )
    parser.add_argument(
        "--datadir-path",
        type=lambda path: Path(path).resolve(),
        help="Path to the directory where kaggle dataset is downloaded."
    )
    parser.add_argument(
        "--client-secrets-path",
        type=lambda path: Path(path).resolve(),
        help=(
            "Path to 'client_secrets.json' file for Google Drive "
            "authorization using PyDrive package."
        )
    )
    add_bool_arg(
        parser=parser,
        name="credentials",
        help_comment="Save credentials for future authorization"
    )

    args = parser.parse_args()

    kaggle_files_paths = glob.glob(str(args.datadir_path.joinpath("*.csv")))

    actions = {
        "upload": {
            "function": upload,
            "params": {
                "client_secrets_path": args.client_secrets_path,
                "files_paths": kaggle_files_paths,
                "credentials_path": str(PACKAGE_PATH.joinpath("mycreds.json")),
                "save_credentials": True
            }
        }
    }

    if args.action == "upload":
        if args.datadir_path is None or args.client_secrets_path is None:
            parser.error(
                "Action: 'download' requires --client-secrets-path and "
                "--datadir-path specified."
            )

    # Call the specified function.
    func = actions[args.action]["function"]
    params = actions[args.action]["params"]

    func(**params)


if __name__ == "__main__":
    main()
