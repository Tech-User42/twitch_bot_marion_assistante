import os # for importing env vars for the bot to use
from twitchio.ext import commands
import asyncio
from ext.Quizz import *
from ext.Logs import *
from dotenv import load_dotenv
from threading import Thread
import asyncio
from time import sleep
load_dotenv()

class TwitchBot():
    def __init__(self,UI) -> None:
        self.Quizz_Manager = Quizz()
        with open('DATASTORE/connect.json', 'r') as json_file:
            TOKEN = json.load(json_file)["access_token"]
        self.BOT = Bot(self.Quizz_Manager,TOKEN,UI)
        self.BotThread = Thread(target=self.BOT.run)
        self.BotThread.daemon = True
    def Run(self):
        try:
            self.BotThread.start()
        except:
            pass
    def Stop(self):
        self.BOT.running = False
        self.BotThread.join(0.1)

class Bot(commands.Bot):
    def __init__(self,Quizz_Manager,TOKEN,UI):
        super().__init__(token=TOKEN,client_id=os.environ['CLIENT_ID'],nick=os.environ['BOT_NICK'],prefix=str(os.environ['BOT_PREFIX']), initial_channels=[os.environ['CHANNEL']])
        self.Quizz_Manager = Quizz_Manager
        self.UI = UI
        self.running = True

        self.loop.create_task(self.run_bot())

    async def run_bot(self):
        await self.wait_for_ready()
        
        while self.running:
            await asyncio.sleep(1)

        # await self.close()
        await self._connection._task_cleanup()

    async def event_ready(self):
        'Run when the bot is sucessfully logged in.'
        log(f"{self.nick} is now online to fuck some bitches !")
        self.UI.Log(f"{self.nick} is now online to fuck some bitches !")
        self.UI.home_frame_title.configure(text="Status du bot [EN LIGNE]",text_color="green")
        self.UI.home_start_button.configure(text=f"Arrêter {os.environ['BOT_NICK']}",text_color="red")
        self.UI.ToggleButtonLoading(False)

    async def event_message(self, ctx)-> None:
        'Runs every time a message is sent in chat.'
        if ctx.echo:
            return
        elif ctx.content.startswith("!"):
            log(f"{ctx.author.display_name} à utilisé la commande {ctx.content}.")
            self.UI.Log(f"{ctx.author.display_name} à utilisé la commande {ctx.content}.")
        elif(self.Quizz_Manager.IsStarted):
            if(not self.Quizz_Manager.ActualQuizz["HaveBeenAsked"]):
                if(self.Quizz_Manager.CheckQuizzReponse(ctx.content,ctx.author.display_name)):
                    await ctx.channel.send(f"Bravo {ctx.author.mention}, tu as trouvé la réponse : {self.Quizz_Manager.ActualQuizz['Response']}")
        else:
            log(f"{ctx.author.display_name} à dit {ctx.content}.")
            self.UI.Log(f"{ctx.author.display_name} à dit {ctx.content}.")
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
            await self.Quizz_Manager.StartQuizz(self)
        else:
            await ctx.send("Désolé, cette commande est réservée au modos !")
        return

    @commands.command()
    async def quizz_stats(self, ctx: commands.Context):
       'A command to get the best quizzer\'z.'
       await ctx.send(self.Quizz_Manager.GetStats())