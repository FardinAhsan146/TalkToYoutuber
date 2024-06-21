greeting_message = """

-----------------------------------------------

Hey Welcome to Talk to Youtuber. 

Talk to Youtuber is a tool that allows you to talk to your favorite youtuber.
We do this by downloading all the videos of the youtuber, extracting the transcripts and then embedding them into a vector database. Then we get gpt4o to generate responses to your questions.

Your conversations will be saved in the database for future reference. So that you can continue your conversation with the youtuber.

The first time you talk to a youtuber, it will take a while to download all the videos and embed them into the vector database.

However the later times will be faster, initial load up will be a bit slow because we will check for new videos and content.

-----------------------------------------------

"""

llm_message = """

-----------------------------------------------

All the needed data is in place! 

You can now begin talking to GPT with your youtubers knowledge. 

Instructions: 
* You can talk to gpt as it is.
* If you want to ask the youtuber a question, please end the question with '??' at the end. 
* Just keyboard interupt if you want to exit the conversation.

Do understand that once you have asked a ?? question. The content of the video will be present in the context window of the conversation. 

You can continue asking about questions with the context of the video.

If you want to carry out another interception from another video, simple ask a ?? question again.

-----------------------------------------------

"""

def print_greeting_message() -> None:
    print(greeting_message.strip())

def print_llm_message() -> None:
    print(llm_message.strip())

def print_intercepting_message(content: str, video_id: str, video_title: str) -> None:
    intercept_message = f"""
-----------------------------------------------
Interceptting your query with additional context from the video.

>> {video_title} << 
You can find the video at: https://www.youtube.com/watch?v={video_id.split('_')[0]}

Context is: 
{content}

-----------------------------------------------

"""
    print(intercept_message.strip()) 
 
def intercept_string(user_input: str, content: str) -> str:
    intercept_message = f"""
-----------------------------------------------
Some additional information:

{content}
-----------------------------------------------
"""
    return user_input + intercept_message.strip()