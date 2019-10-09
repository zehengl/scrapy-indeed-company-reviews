#%%
import os
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from wordcloud import WordCloud


company = os.getenv("indeed_company", None)
assert company, "[indeed] company not set"

reviews_file = Path(f"reviews_{company}.json")
assert (
    reviews_file.is_file()
), f"reviews_{company}.json does not exist. Run the scrapy app."

result = Path("result")
result.mkdir(exist_ok=True)

#%%
df = pd.read_json(reviews_file)
df = df.drop_duplicates(["id"])

#%%
plt.clf()
wc_config = {
    "background_color": "white",
    "width": 800,
    "height": 600,
    "max_words": 800,
    "max_font_size": 40,
}
text = "\n".join(df.text)
wc = WordCloud(**wc_config).generate(text)
fig = plt.figure()
plt.imshow(wc, interpolation="bilinear")
plt.axis("off")
fig.savefig(result / f"{company}-wordcloud.png", bbox_inches="tight", dpi=600)

#%%
plt.clf()
ax = sns.countplot(x="rating", data=df)
ax.get_figure().savefig(result / f"{company}-rating-countplot.png")

#%%
df = df.assign(year=df.apply(lambda r: r["date_created"].split(" ")[-1], axis=1))

#%%
plt.clf()
ax = sns.countplot(x="year", data=df)
ax.get_figure().savefig(result / f"{company}-year-countplot.png")

#%%
plt.clf()
ax = sns.countplot(x="year", hue="rating", data=df)
plt.legend(loc="upper left")
ax.get_figure().savefig(result / f"{company}-year-per-rating-countplot.png")

#%%
plt.clf()
ax = sns.countplot(x="rating", hue="year", data=df)
plt.legend(loc="upper left")
ax.get_figure().savefig(result / f"{company}-rating-per-year-countplot.png")
