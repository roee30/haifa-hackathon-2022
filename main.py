import re
from dataclasses import dataclass
from functools import reduce
from operator import lshift
from pathlib import Path

from datargs import parse, arg
from fn import F


@dataclass
class Args:
    input: Path = arg(positional=True)
    out_dir: Path = Path("out")


clean = re.compile(r"([^\w\s])")
whitespace = re.compile(r"\s+")
niqqud = re.compile(r"[\u0590-\u05bd]")
non_hebrew = re.compile(r"[a-zA-Z0-9]")


def compose(*fns):
    return reduce(lshift, fns, F())


pipe = compose(
    (clean.sub, ""),
    (niqqud.sub, ""),
    (non_hebrew.sub, ""),
    (whitespace.sub, " "),
)


def main():
    args = parse(Args)
    for file in args.input.rglob("*.txt"):
        text = pipe(file.read_text())
        out_path = args.out_dir / file.relative_to(args.input)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(text)
        print(f"{file} -> {out_path}")
    print("done")


if __name__ == "__main__":
    main()
