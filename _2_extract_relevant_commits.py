#!/usr/bin/env python
# -*- coding: utf-8 -*-

import datetime
import os
import sys

import utils
from env import REPO_DIR


def list_repos():
    return (os.path.join(REPO_DIR, repo)
            for repo in os.listdir(REPO_DIR))


def get_repo_commit_count(repo):
    cmd = "git --git-dir={} rev-list --all --count".format(repo)
    return int(utils.run_shell_cmd(cmd))


def list_commits(repo):
    cmd = "git --git-dir={} log --pretty=format:\"%h\"".format(repo)
    return utils.run_shell_cmd(cmd).split('\n')


def filter_commit_single_scala_file(repo, commit):
    # check that changes contains only a single scala file
    cmd = "git --git-dir={} show {} --name-only".format(repo, commit)
    out = utils.run_shell_cmd(cmd)
    files = [l.strip()
             for l in out.split('\n')[1:]
             if len(l.strip()) > 0]  # skip header & empty
    scala_files = []
    for f in files:
        _, ext = os.path.splitext(f)
        if ext.lower() == '.scala':
            scala_files.append(f)
    return len(scala_files) == 1


def filter_commit_continuous_single_edit(repo, commit):
    cmd = "git --git-dir={} show {}".format(repo, commit)
    changes = utils.run_shell_cmd(cmd).split('\n')[1:]  # ignore header
    last_head = ' '
    switches = 0
    for line in changes:
        if len(line) < 1:
            continue
        if line.startswith("---"):
            continue
        if line.startswith("+++"):
            continue
        if line[0] not in {' ', '+', '-'}:
            continue
        if line[0] != last_head:
            switches += 1
        last_head = line[0]
    return switches == 3  # (\s -> + -> - -> \s) or (\s -> - -> + -> \s)


def extract_relevant_commits(repo, progress_logger):
    commits = list_commits(repo)
    relevant_commits = []
    for i, c in enumerate(commits):
        progress_logger.print_progress(i)
        if filter_commit_single_scala_file(repo, c) and \
                filter_commit_continuous_single_edit(repo, c):
            relevant_commits.append(c)
    repo_name = repo[::-1].split('/', 1)[0][::-1]
    progress_logger.set_status("{} done (kept {}/{})".format(
        repo_name, len(relevant_commits), len(commits)))
    progress_logger.bump_offset(len(commits))
    # TODO: do something with the commits


class ParsingProgressLogger(object):
    _start_t = None

    def __init__(self, total):
        self.total = total
        self.offset = 0
        self._start_t = datetime.datetime.now()
        self.status = 'Parsing first repo'

    def print_progress(self, i):
        oi = i + self.offset
        if oi % 30 == 1:
            elapsed = (datetime.datetime.now() - self._start_t).total_seconds()
            left = (elapsed * self.total) / float(oi) - elapsed
            left_str = str(datetime.timedelta(seconds=left))
            sys.stdout.write("\rParsing commits %3.2f%% (ETA %s) <> %s" % (
                100 * (oi / float(self.total)), left_str, self.status))
            sys.stdout.flush()

    def bump_offset(self, n):
        self.offset += n

    def set_status(self, s):
        self.status = s


def main():
    assert (os.path.isdir(REPO_DIR))
    total_commits = sum(get_repo_commit_count(r) for r in list_repos())
    progress_logger = ParsingProgressLogger(total_commits)
    for repo in list(list_repos()):
        extract_relevant_commits(repo, progress_logger)
    print()


if __name__ == "__main__":
    main()
