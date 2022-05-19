import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from pathlib import Path
 
data_list = list()
clean_path = Path("TreeOfKnowledge\degenerated_arabic")
 
for ix ,file in enumerate(clean_path.rglob("*.txt")):
    print(ix, file)
    with open(file, mode='r', encoding="utf-8") as f:
        data = f.read()
    data_list.append(data)        
text = data_list
 
 
coun_vect = CountVectorizer()
count_matrix = coun_vect.fit_transform(text)
count_array = count_matrix.toarray()
df = pd.DataFrame(data=count_array,columns = coun_vect.get_feature_names())
print(df)
 
