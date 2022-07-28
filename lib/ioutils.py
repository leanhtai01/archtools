# author: Le Anh Tai
# email: leanhtai01@gmail.com
# GitHub: https://github.com/leanhtai01
import subprocess


def inputPath(prompt: str = None) -> str:
    """Read a path from standard input"""
    return subprocess.check_output(
        f'read -e -p "{prompt}" path; echo $path',
        shell=True
    ).decode().strip()
