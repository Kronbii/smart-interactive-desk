import subprocess


def run_in_new_terminal(script_path: str):

    subprocess.Popen(
        ["gnome-terminal", "--", "bash", "-c", f"{script_path}; exec bash"]
    )


def main():
    run_in_new_terminal("../scripts/web.sh")


if __name__ == "__main__":
    main()
