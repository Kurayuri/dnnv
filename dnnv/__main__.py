"""
"""
import argparse
import time

from typing import List, Optional

from . import cli
from . import logging
from . import nn
from . import properties
from . import utils


def main(args: argparse.Namespace, extra_args: Optional[List[str]] = None):
    logger = logging.initialize(__package__, args)
    utils.set_random_seed(args.seed)

    logger.debug("Parsing network (%s)", args.network)
    dnn = nn.parse(args.network)

    # TODO: the following is just being used for testing
    dnn.pprint()

    phi = properties.parse(args.property, args=extra_args)
    print("Verifying property:")
    print(phi)

    for verifier in args.verifiers:
        start_t = time.time()
        try:
            verifier_args, extra_args = getattr(
                verifier, "parse_args", lambda x: (argparse.Namespace(), extra_args)
            )(extra_args)
            kwargs = vars(verifier_args)
            result = verifier.verify(dnn, phi, **kwargs)
        except Exception as e:
            result = f"{type(e).__name__}({e})"
        end_t = time.time()
        print(f"{verifier.__name__}")
        print(f"  result: {result}")
        print(f"  time: {(end_t - start_t):.4f}")

    if extra_args is not None and len(extra_args) > 0:
        logger.warning("Unused arguments: %r", extra_args)


def _main():
    main(*cli.parse_args())


if __name__ == "__main__":
    _main()
