import os # for importing env vars for the bot to use
from twitchio.ext import commands
import asyncio
from ext.Quizz import *
from ext.Logs import *
from dotenv import load_dotenv
load_dotenv()

with open('DATASTORE/connect.json', 'r') as json_file:
    TOKEN = json.load(json_file)["access_token"]
class Bot(commands.Bot):
    def __init__(self):
        super().__init__(token=TOKEN,client_id=os.environ['CLIENT_ID'],nick=os.environ['BOT_NICK'],prefix=str(os.environ['BOT_PREFIX']), initial_channels=[os.environ['CHANNEL']])

    async def event_ready(self):
        'Run when the bot is sucessfully logged in.'
        log(f"{self.nick} is now online to fuck some bitches !")

    async def event_message(self, ctx)-> None:
        'Runs every time a message is sent in chat.'
        if ctx.echo:
            return
        elif ctx.content.startswith("!"):
            log(f"{ctx.author.display_name} à utilisé la commande {ctx.content}.")
        elif(Quizz_Manager.IsStarted):
            if(not Quizz_Manager.ActualQuizz["HaveBeenAsked"]):
                if(Quizz_Manager.CheckQuizzReponse(ctx.content,ctx.author.display_name)):
                    await ctx.channel.send(f"Bravo {ctx.author.mention}, tu as trouvé la réponse : {Quizz_Manager.ActualQuizz['Response']}")
        else:
            log(f"{ctx.author.display_name} à dit {ctx.content}.")
        await self.handle_commands(ctx)

    def CheckIsModo(self,ctx):
        return(ctx.author.is_mod)

    @commands.command()
    async def help(self, ctx: commands.Context):
        'A command to show all the available commands.'
        text = "Voici la liste de commandes disponibles !quizz -> Permet de lancer un quizz sur l'univers d'Elden Ring._____________________________________ !quizz_stats -> Permet de voir les meilleurs joueurs des précédents quizz.___________________"
        await ctx.send(text)

    @commands.command()
    async def quizz(self, ctx: commands.Context):
        'A command to trigger a quizz. (mod only)'
        if(self.CheckIsModo(ctx)):
            await ctx.send(f"Le quizz démarrera dans {str(int(os.environ['QUIZZ_START_DELAY'])/60)} minutes")
            await asyncio.sleep(int(os.environ['QUIZZ_START_DELAY']))
            await Quizz_Manager.StartQuizz(self)
        else:
            await ctx.send("Désolé, cette commande est réservée au modos !")
        return

    @commands.command()
    async def quizz_stats(self, ctx: commands.Context):
       'A command to get the best quizzer\'z.'
       await ctx.send(Quizz_Manager.GetStats())

if __name__ == "__main__":
    Quizz_Manager = Quizz()
    bot = Bot()
    bot.run()
