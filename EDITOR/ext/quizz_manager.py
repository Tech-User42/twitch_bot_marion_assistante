import json

class QuizzManager():
    def __init__(self) -> None:
        with open('../BOT/DATASTORE/Quizz/quizz.json', 'r') as json_file:
            self.QuizzData = json.load(json_file)

    def AddQuestion(self,Question,Response):
        NewQuestion = {
            "id": len(self.QuizzData),
            "HaveBeenAsked": False,
            "WhoResponded": False,
            "Question": Question,
            "Response": Response
        }
        self.QuizzData.append(NewQuestion)
        self.WriteChanges()

    def DeleteQuestion(self,id):
        for i in range(id,len(self.QuizzData)):
            temp = int(self.QuizzData[i]["id"]) - 1
            self.QuizzData[i]["id"] = temp
        self.QuizzData.pop(id)
        self.WriteChanges()

    def WriteChanges(self):
        with open("../BOT/DATASTORE/Quizz/quizz.json", 'w') as json_file:
            json.dump(self.QuizzData,json_file,indent=4)