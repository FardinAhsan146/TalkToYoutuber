# Talk To Youtuber
There's a youtuber whose videos I quite like named [japaneat](https://www.youtube.com/@japaneat). I'm going to visit Japan soon and I want to know what his reccomended (suchi, karage, ramen, udon, ...) restaurants are. However, its not like he has a nicely labelled and curated blog or Wiki. Everything he ever said is scrattered among YouTube shorts. 

There are API bindings out there that let you download Google autogenerated and owner uploaded transcripts. Why not just fetch all video data and chuck them into an LLM with RAG? 

For the LLM part I will just use openai embeddings and `gpt4-o`. 

This produce a chatbot with the knowledge of a given youtuber and I can talk and ask questions. 

This project prioritizes simplicity and ease of development over all else. I should be able to finish it in 2-3 days. The choice of packages and architecture is primarily geared for that. If the project ever grows to something larger than I will use personally, it will require a significant refactor. 

# Databases
* [Sqlite3](https://sqlite.org/) : For storing app data. Anything more is overkill. 
* [ChromaDB](https://www.trychroma.com/) : A simple enough vector DB for the job. I really wanted to use a vector extension for sqlite but the main one is still in development and I don't want to handle changes to api continously. Chroma is simple, works on windows and gets the job done. Something like postgres with pgvector would have allowed me to get away with one database but its overkill for the volume of data. This combination of databases makes the project significantly more portable. 

# Packages used 
I might probably have to refactor these to use the Youtube API in the future anyways to not have to depend on two different dependencies and make the code more extensible and legible. However, these are simple enough wrappers that don't need any credientials and abstract away the rough edges of Googles APIs which tend to be quite tedious to work with even for seemingly simple functionality.  

* [scrapetube](https://scrapetube.readthedocs.io/en/latest/) : Get youtube video data with Youtube API 
* [youtube-transcript-api](https://pypi.org/project/youtube-transcript-api/) : Get video transcript data with Youtube API 
