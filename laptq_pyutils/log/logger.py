def pformat_color(obj):

    from pprint import pformat
    from pygments import highlight
    from pygments.formatters import Terminal256Formatter, TerminalFormatter
    from pygments.lexers import PythonLexer

    return highlight(pformat(obj), PythonLexer(), TerminalFormatter())[:-1]


def load_logger(**kwargs):
    """Logger

    Some functionalities:
        try:
            1/0
        except:
            logger.exception('????')

        @logger.catch
        def f(x):
            1/0

        logger.bind(classname=self.__class__.__name__).info("LapTQ")
    """

    import sys
    from loguru import logger

    list__sink = kwargs.get("list__sink", ["sys.stderr"])
    list__mode__sink = kwargs.get("list__mode__sink", ["std"])
    level = kwargs.get("level", "INFO")
    colorize = kwargs.get("colorize", True)
    color__time = kwargs.get("color__fg__time", "fg 100,100,100")
    color__filepath = kwargs.get("color__filepath", "fg 225,175,0")
    color__name = kwargs.get("color__name", "fg 0,175,225")
    color__classname = kwargs.get("color__classname", "magenta")
    color__function = kwargs.get("color__function", "yellow")
    list__rotation = kwargs.get("list__rotation", [None] * len(list__sink))
    list__retention = kwargs.get("list__retention", [None] * len(list__sink))
    num__newline__before = kwargs.get("num__newline__before", 0)
    num__newline__after = kwargs.get("num__newline__after", 0)

    assert (
        len(list__sink)
        == len(list__mode__sink)
        == len(list__rotation)
        == len(list__retention)
    )

    for mode__sink in list__mode__sink:
        assert mode__sink in ["std", "file"]

    __list__sink = []
    list__kwargs_add = []
    for sink, mode__sink, rotation, retention in zip(
        list__sink, list__mode__sink, list__rotation, list__retention
    ):
        if mode__sink == "std":
            sink = eval(sink)
            kwargs__add = {}
        elif mode__sink == "file":
            kwargs__add = {
                "rotation": rotation,
                "retention": retention,
            }
        __list__sink.append(sink)
        list__kwargs_add.append(kwargs__add)
    list__sink = __list__sink

    def formatter(record):
        return "{}{}{}{}{}{}{}".format(
            "<level>{level: <8}</level>",
            " | <{}>{}</{}>".format(
                color__time, "{time:YYYY-MM-DD HH:mm:ss.SSS}", color__time
            ),
            " | <{}>{}: line {}</{}>\t".format(
                color__filepath, "{file.path}", "{line}", color__filepath
            ),
            " | {}{}{}\t".format(
                "<{}>{}</{}>".format(color__name, "{name}", color__name),
                (
                    " :: <{}>{}</{}>".format(
                        color__classname, "{extra[classname]}", color__classname
                    )
                    if "classname" in record["extra"]
                    else ""
                ),
                (
                    " :: <{}>{}</{}>".format(
                        color__function, "{function}", color__function
                    )
                    if record["function"] != "<module>"
                    else ""
                ),
            ),
            " | {}<level>{}</level>".format("\n" * num__newline__before, "{message}"),
            "\n{exception}",
            "\n" * num__newline__after,
        )

    logger.remove()
    for sink, kwargs__add in zip(list__sink, list__kwargs_add):
        logger.add(
            sink=sink, level=level, colorize=colorize, format=formatter, **kwargs__add
        )

    return logger
