#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os

import utils
from _0_get_top_repos import top_repos_filename
from env import REPO_DIR


def main():
    assert (os.path.exists(top_repos_filename))

    with open(top_repos_filename, "r") as f:
        j = json.load(f)

        if not os.path.exists(REPO_DIR):
            os.makedirs(REPO_DIR)

    for i, repo in enumerate(j["items"]):
        repo_name = repo["name"]
        repo_url = repo["git_url"]
        if not os.path.exists(os.path.join(REPO_DIR, repo_name + ".git")):
            print("({}/{}) Cloning {}...".format(i + 1,
                                                 len(j["items"]),
                                                 repo_name))
            cmd = "git clone --bare {} -q --single-branch".format(repo_url,
                                                                  repo_name)
            utils.run_shell_cmd(cmd, cwd=REPO_DIR)


if __name__ == "__main__":
    main()
