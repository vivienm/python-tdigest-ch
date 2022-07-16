import argparse
import multiprocessing
from multiprocessing.dummy import Pool
from typing import NoReturn

from tdigest import TDigest as PyTDigest

from tdigest_ch import TDigest as RsTDigest

NUM_ELEMS = 50_000


def rs_worker(worker_id: int) -> NoReturn:
    t = RsTDigest()
    elems = list(range(NUM_ELEMS))
    while True:
        t.update(elems)
        print("Thread {} added {} elements".format(worker_id, NUM_ELEMS))


def py_worker(worker_id: int) -> NoReturn:
    t = PyTDigest()
    elems = list(range(NUM_ELEMS))
    while True:
        t.batch_update(elems)
        print("Thread {} added {} elements".format(worker_id, NUM_ELEMS))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--impl",
        choices=["py", "rs"],
        default="rs",
        help="which t-digest implementation to use",
    )
    parser.add_argument(
        "-j",
        "--num-threads",
        type=int,
        default=multiprocessing.cpu_count(),
        help="number of threads to use",
    )
    args = parser.parse_args()

    print("Starting {} threads...".format(args.num_threads))
    with Pool(args.num_threads) as pool:
        pool.map(
            rs_worker if args.impl == "rs" else py_worker,
            range(args.num_threads),
        )


if __name__ == "__main__":
    main()
