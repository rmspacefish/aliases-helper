#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Python utility to set up common and useful aliases
"""
import os
import sys
import getpass
from os import linesep
from shutil import which

# Configuration
TEST_MODE = False
CONFIGURE_GIT = True
DEFAULT_GIT_CRED_CACHE = 900
TEST_FILENAME = "test_aliases.txt"
ALIASES_FILENAME = ".bash_aliases"
# This mode will store the current alias file, discard any entries in the new alias buffer which
# are already contained in the former alias file and then append the aliases at the end
DISCARD_APPEND_MODE = True

GENERIC_ALIASES = \
    f"alias gits='git status'{linesep}" \
    f"alias gita='git add'{linesep}" \
    f"alias gitaa='git add .'{linesep}" \
    f"alias gitc='git commit'{linesep}" \
    f"alias gitd='git diff'{linesep}" \
    f"alias gitds='git diff --staged'{linesep}" \
    f"alias gitm='git merge'{linesep}" \
    f"alias gitpl='git pull'{linesep}" \
    f"alias gitl='git log'{linesep}" \
    f"alias gitpu='git push'\n" \
    f"alias gitrmu='git remote update --prune'{linesep}{linesep}" \
    f"alias ..='cd ..'{linesep}" \
    f"alias ...='cd ../..'{linesep}" \
    f"alias ....='cd ../../..'{linesep}"
SOURCE_ALIAS = f"alias salias='cd ~ && source {ALIASES_FILENAME}'{linesep}"
SHORTCUT_ALIAS_INCOMP = f"alias shortcut='cd ~ && "
EDITOR_SELECTION = {
    0: "gedit",
    1: "vim",
    2: "nano",
    3: "custom"
}

UNIX_APT_UPDATE_ALIAS = f"alias updatesys=\"sudo apt-get update && sudo apt-get upgrade\"{linesep}"
UNIX_PAC_UPDATE_ALIAS = f"alias updatesys=\"sudo pacman -Syu\"{linesep}"

WIN_MSYS2_CMD = "msys2_shell.cmd"
WIN_MINGW64_ARGS = "-mingw64 -c"
WIN_MINGW64_UPDATE_ALIAS = f"alias updatesys=\"pacman -Syu\"{linesep}"
WIN_MINGW64_CMD = f"{WIN_MSYS2_CMD} {WIN_MINGW64_ARGS}"


def main():
    print("-- Python alias file creator utility --")
    if sys.platform.startswith("win32"):
        print("Detected Windows platform")
        generate_windows_aliases()
    elif sys.platform.startswith("linux"):
        print("Detected Linux platform")
        generate_unix_aliases()
    else:
        print("Not implemented for this OS.")
    print("-- Alias helper finished --")


def generate_windows_aliases():
    aliases_string_buf = GENERIC_ALIASES
    notepad_alias = "alias notepad=\"/c/Program\ Files\ \(x86\)/Notepad++/notepad++.exe\"\n"
    aliases_string_buf += linesep + notepad_alias
    shortcut_alias = SHORTCUT_ALIAS_INCOMP + f"notepad {ALIASES_FILENAME}'{linesep}"
    aliases_string_buf += shortcut_alias
    aliases_string_buf += SOURCE_ALIAS

    which_result = which("git")
    if which_result is not None:
        print("Setting up aliases for git..")
        # This is the path for git
        os.chdir(os.getenv('userprofile'))
        if os.path.isfile(".bash_aliases") and not TEST_MODE:
            print(f"{ALIASES_FILENAME} file already exists")
            sys.exit(0)
        target_file = file_writer(ALIASES_FILENAME, aliases_string_buf)
        print(f"Generated {target_file} in {os.getcwd()} for git")
    else:
        print("git not found, might not be installed, not creating alias file..")

    which_result = which(WIN_MSYS2_CMD)
    if which_result is not None:
        # This is the path for MinGW64
        username = getpass.getuser()
        os.chdir(f"C:/msys64/home/{username}")
        target_file = file_writer(ALIASES_FILENAME, aliases_string_buf)
        print(f"Generated {target_file} in {os.getcwd()} for MinGW64")
    else:
        print("MinGW64 not found, might not be installed, not creating alias file..")


def generate_unix_aliases():
    print("Generting Unix aliases..")
    os.chdir(os.getenv("HOME"))
    current_file_string_bug = ""
    if os.path.isfile(".bash_aliases"):
        print(f"{ALIASES_FILENAME} file already exists")
        if DISCARD_APPEND_MODE:
            with open(ALIASES_FILENAME, "r") as file:
                current_file_string_buf = file.read()
        elif not TEST_MODE:
            sys.exit(0)
    aliases_string_buf = GENERIC_ALIASES
    unix_editor = prompt_unix_editor()
    shortcut_alias = SHORTCUT_ALIAS_INCOMP + f"{unix_editor} {ALIASES_FILENAME}'{linesep}"
    aliases_string_buf += shortcut_alias
    aliases_string_buf += SOURCE_ALIAS
    if DISCARD_APPEND_MODE and current_file_string_bug != "":
        aliases_list = aliases_string_buf.splitlines()
        aliases_string_buf = ""
        print("Discarding any aliases already contained in former aliases list..")
        for new_alias in aliases_list:
            if new_alias in current_file_string_buf:
                print(f"Discarding: {new_alias}")
            else:
                aliases_string_buf += f"{new_alias}{linesep}"
        print("Aliases buffer which will be appended to former alias file: ")
        print(aliases_string_buf)
        print("End of appended alias list")
        aliases_string_buf += linesep
        aliases_string_buf += current_file_string_buf
    which_result = which("apt-get")
    if which_result is not None:
        aliases_string_buf += UNIX_APT_UPDATE_ALIAS
    if os.path.isdir("/mnt/c/"):
        notepad_alias = "alias notepad=\"/mnt/c/Program\ Files\ \(x86\)/Notepad++/notepad++.exe\"\n"
        confirm = input("Detected Linux platform might be WSL. Generate notepad++ alias? [y/n]: ")
        if confirm in ["y", "yes", "1"]:
            aliases_string_buf += notepad_alias
    target_file = file_writer(ALIASES_FILENAME, aliases_string_buf)
    print(f"Generated {target_file} in {os.getcwd()}")
    print(f"Sourcing {target_file}..")
    if(os.path.isfile(".bash_aliases")):
        os.system("/bin/bash -c \"source .bash_aliases\"")


def prompt_unix_editor() -> str:
    print("Please enter editor by ID: ")
    while True:
        for key, value in EDITOR_SELECTION.items():
            print(f"{key}: {value}")
        editor_id = input("Please enter editor by ID: ")
        if not editor_id.isdigit():
            continue
        editor_id = int(editor_id)
        if editor_id == 3:
            custom_editor = input("Enter custom editor")
            confirm = input(f"Confirm selection: {custom_editor}")
            if confirm in ["y", "yes", "1"]:
                return custom_editor
        elif 0 < editor_id < 3:
            return EDITOR_SELECTION[editor_id]


def file_writer(target_filename, alias_buffer: str) -> str:
    if not TEST_MODE:
        target_file = target_filename
        with open(target_file, "w") as file:
            file.write(alias_buffer)
    else:
        target_file = TEST_FILENAME
        with open(target_file, "w") as file:
            file.write(alias_buffer)
    return target_file


if __name__ == "__main__":
    main()