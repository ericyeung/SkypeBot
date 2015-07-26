from pyteaser import SummarizeUrl
from goose import Goose
sentences_per_summary = 3
 
def cmd_tldr(Message):
    msg = Message.Body.lower()
    body = Message.Body
    Message.Chat.SendMessage(">> Summarizing your article...")
    splitMessage = body.strip().split(" ") # splits the message into command and argument
    url = splitMessage[1] 
    summaries = SummarizeUrl(url)  
    g = Goose()
    if summaries:
        for summary in summaries:
            Message.Chat.SendMessage(summary.encode("utf-8"))
        article = g.extract(url)
        Message.Chat.SendMessage(">> The article title is" + " \""+ article.title + "\"")
    else:
        Message.Chat.SendMessage(">> The article is too powerful... Cannot summarize.")
