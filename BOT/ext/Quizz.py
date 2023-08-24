import datetime
import json
import os
from random import randint as rand
import asyncio
from twitchio.ext import routines
from dotenv import load_dotenv
load_dotenv()


class Quizz():
    def __init__(self) -> None:
        self.IsStarted = False
        self.ActualQuizz = {}
        self.QuizzStats = {}
        self.QuestionsAsked = 0
        self.LoadQuizzData()

    def LoadQuizzData(self):
        'Used to load all Questions/Reponses.'
        with open('DATASTORE/Quizz/quizz.json', 'r') as json_file:
            self.QuizzData = json.load(json_file)

    def StoreQuizzData(self):
        'Used to store all Questions/Reponses.'
        filename = f"Quizz_{datetime.datetime.now().time().strftime('%H_%M_%S_')}{datetime.datetime.now().date().strftime('%d_%m_%Y')}.json"
        with open(f"DATASTORE/Quizz/Old_Data/{filename}", 'w') as json_file:
            json.dump(self.QuizzData,json_file,indent=4)

    def GetQuizz(self):
        'Used to get a new Question/Responses.'
        self.IsStarted = True
        self.QuestionsAsked += 1
        to_return = {"HaveBeenAsked":True}
        while(to_return["HaveBeenAsked"]):
            to_return = self.QuizzData[rand(0,len(self.QuizzData)-1)]
        self.ActualQuizz = to_return
        return to_return
    
    def CheckQuizzReponse(self,Message,Author):
        'Used to check user Reponses.'
        if(Message.lower() in self.ActualQuizz["Response"].lower()):
            self.ActualQuizz["HaveBeenAsked"] = True
            self.ActualQuizz["WhoResponded"] = Author
            self.QuizzData[int(self.ActualQuizz["id"])] = self.ActualQuizz
            return 1
        else:
            return 0
        
    def ClearQuestion(self):
        'Used to throw out current Questions/Reponses.'
        self.ActualQuizz["HaveBeenAsked"] = True
        self.QuizzData[int(self.ActualQuizz["id"])] = self.ActualQuizz

    def GetStats(self):
        'Used to get past quizz\'s best replyer\'s.'
        for File in [Files for Files in os.listdir("DATASTORE/Quizz/Old_Data") if Files.endswith('.json')]:
            path = os.path.join("DATASTORE/Quizz/Old_Data", File)
            with open(path, 'r') as f:
                for question in json.load(f):
                    if(question["WhoResponded"]):
                        try:
                            self.QuizzStats[question["WhoResponded"]] += 1
                        except KeyError:
                            self.QuizzStats[question["WhoResponded"]] = 1
        sorted_results = sorted(self.QuizzStats.items(), key=lambda x: x[1], reverse=True)
        self.QuizzStats = {}
        to_return = ""
        for i, (participant, score) in enumerate(sorted_results[:5], start=1):
            to_return += f"{i}. {participant}: {score} réponses correctes. "
        return to_return
    
    async def StartQuizz(self,bot):
        @routines.routine(seconds=int(os.environ['QUIZZ_DELAY_BETWEEN_QUESTIONS'])+5, iterations=len(self.QuizzData)+1)
        async def quizz_routine():
            channel = bot.get_channel(os.environ['CHANNEL'])
            if(self.QuestionsAsked < len(self.QuizzData)):
                QuizData =  self.GetQuizz()
                Question = QuizData["Question"]
                Response = QuizData["Response"]
                await channel.send(Question)
                await asyncio.sleep(int(os.environ["QUIZZ_RESPONSE_TIME"]))
                if(not QuizData["HaveBeenAsked"]):
                    await channel.send(Response)
                    self.ClearQuestion()
                if(self.QuestionsAsked == len(self.QuizzData)):
                    self.StoreQuizzData()
            else:
                await channel.send("Le quizz est maintenant terminé !")
                await asyncio.sleep(5)
                await channel.send(self.GetStats())
        channel = bot.get_channel(os.environ['CHANNEL'])
        await channel.send("Bienvenue dans le grand Quizz ! Voici les règles : " + self.Rules())
        await asyncio.sleep(15)
        quizz_routine.start()

    def Rules(self):
        return f"Une question est posée, vous avez {os.environ['QUIZZ_RESPONSE_TIME']} secondes pour répondre à cette dernière, à la fin vous pouvez utiliser !quizz_stats pour voir les meilleurs joueurs ;)"
