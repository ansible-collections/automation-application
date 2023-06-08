#! python

"""Scrtch pad for running the application."""


from importlib import resources

import shlex
import subprocess
import os

import sys
import yaml


def _run_playbook(details: dict[str, str | list[str]]):
    """Run the ansible playbook for the given application.

    Parameters
    ----------
    app : str
    """
    # Note: validate the inputs against the input schema prior to running the playbook
    playbook_name = details["name"]
    add_args = details.get("args", [])
    command = [
        "ansible-playbook",
        playbook_name,
        "-i",
        "inventory.yaml",
        "-e",
        "@vars.yaml",
    ]
    command.extend(add_args)
    env = os.environ.copy()

    env["ANSIBLE_COLLECTIONS_PATHS"] = "./collections"
    subprocess.run(args=shlex.join(command), shell=True, check=False, env=env)


def main():
    """Run the application with the given name.

    Parameters
    ----------
    app_name : str
    """
    try:
        app = sys.argv[1]
    except IndexError:
        app = "sample.collection_w_app.hello_world"
    coll, cname, app = app.split(".")

    sys.path.append("./collections")

    package = f"ansible_collections.{coll}.{cname}.applications.{app}"
    filename = "execution.yaml"

    with resources.files(package).joinpath(filename).open(
        "r", encoding="utf-8"
    ) as fhand:
        content = fhand.read()

    exec_config = yaml.load(content, Loader=yaml.SafeLoader)
    for step, details in exec_config["execution"].items():
        if step == "ansible-playbook":
            _run_playbook(details)
        if step == "shell":
            command = details["command"]
            subprocess.run(command, shell=True, check=True)


if __name__ == "__main__":
    main()
