import logging
from titan.finance.utils import read_pandas, write_arrow
from titan.finance.utils.arrow import create_path
from .worker import worker


logger = logging.getLogger(__name__)


def reporter(params: dict) -> str:
    logger.debug(f"Performing a sequence of reporter")
    input_file = params.get("input")
    output = params.get("output")
    batch_size = params.get("batch_size")
    reformat_string = params.get("reformat_string")

    if input_file is None:
        logger.debug(f"Cannot read the input file: {input_file}")
        raise FileNotFoundError("File not found!")

    operations = params.get("operations")
    df = read_pandas(input_file)
    df = worker(df, operations)

    if output is not None:
        create_path(output)
        write_arrow(df, output, chunk_size=batch_size)
    else:
        raise AttributeError("No output file")

    return "ARROW"
