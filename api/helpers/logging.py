import logging
import sys
def log_debug(name: str,fargs: dict,function=True) -> None:
    called_from=sys._getframe().f_back.f_code.co_name
    



    output = f"{name}():\n" if function else f"{name}:\n"
    for arg in fargs:
        output += f"{arg}: {fargs[arg]}\n"
    logging.debug(output)