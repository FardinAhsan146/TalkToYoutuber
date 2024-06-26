# Talk To Youtuber

![gif](https://github.com/FardinAhsan146/TalkToYoutuber/blob/master/docs/talk_to_youtuber-Trim-Trimonline-video-cutter.com-ezgif.com-video-to-gif-converter.gif)

[Video Demo/Initialization](https://www.youtube.com/watch?v=pXZzIsO9ZGA)

*The app works much faster than the demo, I've optimized it since I've recorded the gif and video* 

There's a youtuber whose videos I quite like named [japaneat](https://www.youtube.com/@japaneat). I'm going to visit Japan soon and I want to know what his reccomended (suchi, karage, ramen, udon, ...) restaurants are. However, its not like he has a nicely labelled and curated blog or Wiki. Everything he ever said is scrattered among YouTube shorts.

So why not download all of his videos, add it to a database and semantic search it, and hook that up to an LLM as well? 

Using this tool, I've been able to actually add a bunch of places to my itenarary! Often gpt isn't the most helpful even with added context, but the semantic search nevertheless points me in the right direction. 

### How to use? 

Its really simple, just type in the name of the youtuber you want to talk to. 

# Stack 

### Databases

So that you can come back and continue talk to your youtubers of choice! 

* [Sqlite3](https://sqlite.org/) : For storing app data. Anything more is overkill. 
* [ChromaDB](https://www.trychroma.com/) : A simple enough vector DB for the job. I really wanted to use a vector extension for sqlite but the main one is still in development and I don't want to handle changes to api continously. Chroma is simple, works on windows and gets the job done. Something like postgres with pgvector would have allowed me to get away with one database but its overkill for the volume of data. This combination of databases makes the project significantly more portable. 

### Youtube API 

You don't need credentials! 

I might probably have to refactor these to use the Youtube API in the future anyways to not have to depend on two different dependencies and make the code more extensible and legible. However, these are simple enough wrappers that don't need any credientials and abstract away the rough edges of Googles APIs which tend to be quite tedious to work with even for seemingly simple functionality.  

* [scrapetube](https://scrapetube.readthedocs.io/en/latest/) : Get youtube video data with Youtube API 
* [youtube-transcript-api](https://pypi.org/project/youtube-transcript-api/) : Get video transcript data with Youtube API 

----

# How to run. 

This project is designed to be maximally portable and easy to run. 

1. Install dependencies. You can use the `requirements.txt` this will install ALL of the dependencies. There will be a few additional ones that are a result of the tooling I used to develop, you might not need those. Else you can install the afforementioned YouTube API wrappers and chromaDB. 
2. Create a `.env` file in the `/llm` directory and populate it with your `OPENAI_API_KEY`. 
3. Run the `main.py` file. That's it really. 
4. The script will ask you for which youtubers you want to talk to. Just type in the youtubers name. Make sure its EXACTLY like it is in their channel (look at the channel URL). It will download their videos and once done, you can talk to GPT with their video transcripts semantically injected into the context of the chat. 
5. If you want to nuke the databases you can run the `clean_databases.ps1` script. Converting it to bash is trivial as well. Just delete the sqlite file and the chroma directory. You probably won't have to do this, unless your db gets currupted in some way. If you run into an error during the initial download (OpenAI timing out or Database connection closiing, rare but can happen), then nuke the databases. 

More instructions coming soon.

# Immediate attention 

None ATM. Project is pretty stable, clean and optimized. 

# Future

* I want to refactor the code and make it database, api and interface agnostic for the most part. 
* I want to add in fuzz and regression testing.
* I want to add a feature where the user can pass in query params to the vector db in their message. This will allow for even better context fetching. For example, I might what to know japaneats favorite sushi restaurant in Tokyo. The match might not be a restaurant in tokyo. I can pass in a query param like `{"$includes":"tokyo"}` so I get context that has certain keywords. This will be a nice to have, but I will do this after I handle the major performance improvements.
* Switch out chat model for 'Claude 3.5 Sonnet' - I think it will be better than gpt4o.