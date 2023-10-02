import logging

def log_debug(name: str,fargs: dict,function=True) -> None:
    output = f"{name}():\n" if function else f"{name}:\n"
    for arg in fargs:
        output += f"{arg}: {fargs[arg]}\n"
    logging.debug(output)