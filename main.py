import sys
from openmp.openmp import openmp
from mpi.mpi import mpi
import os
from dotenv import load_dotenv

load_dotenv()


def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py <openmp|mpi>")
        sys.exit(1)

    mode = sys.argv[1].lower()

    if mode == "openmp":
        openmp()
    elif mode == "mpi":
        mpi()
    else:
        print("Invalid mode. Use 'openmp' or 'mpi'.")
        sys.exit(1)

if __name__ == "__main__":
    main()