import functools
from . import config
from . import ds4
from . import web
from . import manual
from . import auto
from .utils import log


def main():
    if config.ds4_control:
        ds4.main()
    elif config.web_control:
        web.main()
    elif config.manual_control:
        manual.main()
    elif config.auto_control:
        auto.main()


if __name__ == "__main__":
    main()
