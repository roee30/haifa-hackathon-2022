import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from pathlib import Path
from main import non_hebrew as english, clean, compose

pipe = compose(
    (english.sub, ""),
    (clean.sub, ""),
)

clean_path = Path("data/degenerated_arabic")
text = [pipe(file.read_text()) for file in clean_path.rglob("*.txt")]


print("vectorizing")
coun_vect = CountVectorizer()
count_matrix = coun_vect.fit_transform(text)
count_array = count_matrix.toarray()
df = pd.DataFrame(data=count_array, columns=coun_vect.get_feature_names())
print(df)
df.to_csv("out/bag_of_words_degenerated.csv", encoding="utf-8")
print("done")
