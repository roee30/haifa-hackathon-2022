from pathlib import Path

from camel_tools.tokenizers.word import simple_word_tokenize
from camel_tools.disambig.mle import MLEDisambiguator
from openiti.helper.ara import denoise
from tqdm import tqdm

path_ = "data/openITI_clean_text/0595IbnRushdHafid.MaqalaFiBudhur.DARE00016-ara1.txt"
# in_dir = Path("data/openITI_clean_text")
in_dir = Path("data/degenerated_arabic")
out_dir = Path("out")
out2 = Path("out2")


def translate(path: Path):
    out_path = out_dir / path.relative_to("data")
    if out_path.exists():
        print(f"skipping: {out_path}")
        return out_path
    print(f"processing: {path}")
    text = path.read_text()

    mle = MLEDisambiguator.pretrained()

    # The disambiguator expects pre-tokenized text
    sentence = simple_word_tokenize(text)

    disambig = mle.disambiguate(sentence)

    # For each disambiguated word d in disambig, d.analyses is a list of analyses
    # sorted from most likely to least likely. Therefore, d.analyses[0] would
    # be the most likely analysis for a given word. Below we extract different
    # features from the top analysis of each disambiguated word into seperate lists.
    ana = [d.analyses[0].analysis for d in disambig]
    words = [(a["diac"], a["lex"], a["pos"]) for a in ana]
    print(f"writing: {path} -> {out_path}")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w") as f:
        for diac, lex, part_of_speech in words:
            if part_of_speech not in ["punc", "digit"]:
                f.write(f"{denoise(lex)} ")
    return out_path


def denoise_(path: Path):
    out_path = out2 / path.relative_to(out_dir)
    if out_path.exists():
        print(f"skipping denoise: {out_path}")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(denoise(path.read_text()))
    print(f"denoised: {out_path}")


def main():
    for file in tqdm(list(in_dir.rglob("*.txt"))):
        translate(file)


if __name__ == "__main__":
    main()
