import asyncio as a
from pathlib import Path

from aiohttp import ClientSession
from bs4 import BeautifulSoup


async def get_metadata(name, category):
    url = f"https://www.sefaria.org/{name}"
    async with ClientSession() as session, session.get(
        url, cookies={"interfaceLang": "english"}
    ) as r:
        html = await r.text()
    soup = BeautifulSoup(html, features="lxml")
    try:
        meta_text = soup.find_all("div", class_="aboutTextMetadata")[0]
    except IndexError:
        return {"name": name}
    try:
        author, composed = [part.text for part in meta_text]
        _, author = author.split(None, 1)
    except ValueError:
        author = None
        composed = meta_text.text
    try:
        place, time = composed.rsplit(",", 1)
        _, place = place.split(None, 1)
    except ValueError:
        time = composed.split(None, 1)[1]
        place = None
    metadata = {
        "author": author,
        "place": place,
        "time": time,
        "category": category,
        "name": name,
    }
    metadata = {k: v.strip() if v else v for k, v in metadata.items()}
    return metadata


async def main():
    result = await a.gather(
        *(
            get_metadata(p.stem.replace("_", "").replace(" ", "_"), p.parent.stem)
            for p in Path("data/sefaria").rglob("*.txt")
        )
    )
    categories = ("name", "author", "category", "place", "time")
    print(",".join(categories))
    for row in result:
        print(",".join(row.get(key) or "" for key in categories))


if __name__ == "__main__":
    a.run(main())
