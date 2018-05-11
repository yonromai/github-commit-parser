#!/usr/bin/env python
# -*- coding: utf-8 -*-

import hashlib
import os
import utils
from env import DATA_DIR

_min_stars = 1000
_language = "Scala"
_query = "stars%3A%3E{}+language%3A{}".format(_min_stars, _language)
_h = hashlib.md5(_query).hexdigest()[:12]
top_repos_filename = os.path.join(DATA_DIR, "gh_search_{}.json".format(_h))


def main():
    if os.path.exists(top_repos_filename):
        print("Reusing existing github seach.")
        return top_repos_filename

    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    url = "https://api.github.com/search/repositories?" \
          "q={}&" \
          "sort=stars&" \
          "order=desc&" \
          "per_page=100".format(_query)

    cmd = "curl \"{}\" -o {}".format(url, top_repos_filename)
    utils.run_shell_cmd(cmd)
    return top_repos_filename


if __name__ == "__main__":
    main()
