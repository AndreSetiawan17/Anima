from bs4 import BeautifulSoup
import requests
import time

class MyAnimeList:

    @staticmethod
    def request(link:str,soup:bool=True) -> any:
        req = requests.get(link)
        if req.status_code != 200:        
            raise ConnectionError(req.status_code)

        if soup:
            return BeautifulSoup(req.text,"html.parser")
        return req.text

    @staticmethod
    def page(link:str) -> dict:
        soup     = MyAnimeList.request(link)
        title    = soup.find("h1","title-name h1_bold_none").strong.text
        score    = soup.find("div",{"class":"fl-l score","data-title":"score"}).text

        filter   = [
            "Synonyms","Japanese","English","Type",
            "Episodes","Aired","Premiered",
            "Studios","Source","Genres","Themes"
        ]
        replace = ["genres","themes"]

        data = {
            k.lower(): v.replace(" ","") if k.lower() in replace else v.strip()
            for k,v in [
                i.strip().split(":")
                for i in [
                    j.text.replace("\n","").strip()
                    for j in soup.find_all("div","spaceit_pad")
                ] if i.strip().split(":")[0] in filter
            ]
        }
        return {
            **{
                "title":title,
            }, **{
                k:[i.replace(i,i[:len(i)//2]) for i in v.split(",")] if k in replace else v 
                for k,v in data.items()
            }, **{
                "score":score,
                "last":time.strftime("%Y,%m,%d,%z"),
                "link":link
            }
        }

    @staticmethod
    def search(keyword:str) -> list:
        """Return: Title, Type, Episode, Rating, Link"""
        soup = MyAnimeList.request(f"https://myanimelist.net/anime.php?q={keyword}&cat=anime")

        #!! optimize later
        ls      = soup.find_all("a","hoverinfo_trigger fw-b fl-l")
        title   = [i.find("strong").text for i in ls]
        link    = [i["href"] for i in ls]
        type_   = [i.text.replace("\n","").strip() for i in soup.find_all("td",{"class":"borderClass ac bgColor0","width":45})]
        episode = [i.text.replace("\n","").strip() for i in soup.find_all("td",{"class":"borderClass ac bgColor0","width":40})]
        rating  = [i.text.replace("\n","").strip() for i in soup.find_all("td",{"class":"borderClass ac bgColor0","width":50})]

        return [{
            "title":i[0],
            "type":i[1],
            "episode":i[2],
            "rating":i[3],
            "link":i[4]
        } for i in zip(title,type_,episode,rating,link)]

class View:

    @staticmethod
    def page(data:dict) -> None: 
        len_max = max([len(i) for i in data.keys()])
        for key,value in data.items():
            print(f"{key.capitalize().ljust(len_max+1)}: ",end="")

            if isinstance(value,list):
                for i in value:
                    print(i,end=",")
                print()
                continue

            print(value)
    
    @staticmethod
    def search(data:list) -> None:
        for i,kv in enumerate(data):
            print(f"- {i+1:02d}.{kv['title']} - {kv['type']} - {kv['episode']} - {kv['rating']} - {kv['link']}")