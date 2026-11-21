"""Validate a saved harness verdict against its specific completed run."""
import os


def accepted_verdict(rc, verdict, executable, tag):
    """Accept only a successful harness result bound to this executable and tag."""
    if rc != 0 or not isinstance(verdict, dict) or verdict.get('pass_') is not True:
        return False
    if not isinstance(executable, str) or not executable or not isinstance(tag, str) or not tag:
        return False
    path = verdict.get('exe')
    if not isinstance(path, str) or not path or verdict.get('tag') != tag:
        return False
    try:
        return os.path.normcase(os.path.abspath(path)) == os.path.normcase(os.path.abspath(executable))
    except (OSError, ValueError, TypeError):
        return False
