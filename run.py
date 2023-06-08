"""Scrtch pad for running the application."""


from importlib import resources

import subprocess
import os

import sys
import yaml


def _run_playbook(playbook_name: str):
    """Run the ansible playbook for the given application.

    Parameters
    ----------
    app : str
    """
    # Note: validate the inputs against the input schema prior to running the playbook
    command = f"ansible-playbook -i inventory.yaml {playbook_name} -e @vars.yaml"
    env = os.environ.copy()

    env["ANSIBLE_COLLECTIONS_PATHS"] = "./collections"
    subprocess.run(command, shell=True, check=False, env=env)


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
    print(content)

    exec_config = yaml.load(content, Loader=yaml.SafeLoader)
    for step, details in exec_config["execution"].items():
        if step == "ansible-playbook":
            playbook = details["name"]
            _run_playbook(playbook)
        print(step)


if __name__ == "__main__":
    main()
