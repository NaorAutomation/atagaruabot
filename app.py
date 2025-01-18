import discord
from discord.ext import commands
import random
import datetime
import asyncio
import os
from typing import Optional

class DiscordBot:
    def __init__(self):
        # הגדרות הבוט
        self.DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
        print(f"Token value: {self.DISCORD_TOKEN}")
        print(f"Token length: {len(self.DISCORD_TOKEN) if self.DISCORD_TOKEN else 'None'}")
        self.TEXT_CHANNEL_NAME = 'fifa-20-talks'
        self.VOICE_CHANNELS = ['FIFA 22 PRO CLUB', 'FIFA 22 FUT CHAMPIONS']
        
        # נתיבים לקבצי אודיו
        self.AUDIO_FILES = {
            'kakibuy': os.path.join('static', 'audio', 'kakibuy.m4a'),
            'spyware': os.path.join('static', 'audio', 'spyware.m4a'),
            'elad1267': os.path.join('static', 'audio', 'elad.m4a')
        }
        
        # הודעות מותאמות אישית לשחקנים
        self.CUSTOM_MESSAGES = {
            'kakibuy': [
                "🎮 שמעתם על ה-AI החדש של FIFA 25? הוא סירב לשחק נגד kakibuy כי זה היה 'נגד חוקי האתיקה של בינה מלאכותית'",
                "🤖 Breaking: EA Sports הוסיפו דרגת קושי חדשה - 'kakibuy mode'. המשחק פשוט מוחק את עצמו מהמחשב",
                "⚽ kakibuy נכנס למשחק! אפילו ה-VAR ביקש חופשה...",
                "🎯 הודעת מערכת: kakibuy התחבר. השרת עובר אוטומטית למצב 'הנחות מרחמים'"
            ],
            'spyware': [
                "🏆 EA הודיעו: בזכות spyware, הם מוסיפים ל-FIFA 25 מצב משחק חדש - 'איך להפסיד ב-30 דרכים שונות'",
                "🎮 ברוך הבא spyware! השחקן היחיד שהצליח להפסיד במצב Practice... נגד שער ריק",
                "⚽ התראת מערכת: spyware נכנס למשחק. הבוט מפעיל אוטומטית מצב 'עידוד לתחילת הדרך'",
                "🤣 שמעתם? spyware ניסה לקנות שחקן ב-FUT... השחקן ביקש להישאר חופשי"
            ],
            'elad1267': [
                "🎯 elad1267 הצטרף! EA שוקלים להוסיף את הסטטיסטיקות שלו כ'מצב קושי בלתי אפשרי'",
                "⚽ הודעת מערכת: elad1267 התחבר. מפעיל מצב 'שערים רחבים פי שלוש' אוטומטית",
                "🎮 Breaking: elad1267 במשחק! אפילו ה-AI של FIFA 25 מרגיש יותר בטוח בעצמו",
                "🤖 שמעתם? elad1267 כל כך גרוע שה-ChatGPT של 2025 מסרב לנתח את המשחק שלו"
            ]
        }

        # הגדרת הבוט
        intents = discord.Intents.all()
        self.bot = commands.Bot(command_prefix='!', intents=intents)
        self.setup_events()

    def setup_events(self):
        @self.bot.event
        async def on_ready():
            print(f'הבוט {self.bot.user} מוכן!')
            for guild in self.bot.guilds:
                print(f'מחובר לשרת: {guild.name}')

        @self.bot.event
        async def on_voice_state_update(member, before, after):
            if member.bot:
                return

            text_channel = discord.utils.get(member.guild.text_channels, name=self.TEXT_CHANNEL_NAME)
            if not text_channel:
                return

            # מעבר בין ערוצים
            if before.channel and after.channel and before.channel != after.channel:
                message = f"🎮 {member.name} עובר בין ערוצים כמו שהוא עובר בין הפסדים ב-FIFA"
                await text_channel.send(message)
                
            # כניסה לערוץ חדש
            elif after.channel and after.channel.name in self.VOICE_CHANNELS:
                await self.handle_voice_channel_join(member, after.channel, text_channel)
            
            # יציאה מערוץ
            elif before.channel and not after.channel:
                message = f"👋 {member.name} יצא מהערוץ. כנראה הלך לראות סרטוני הדרכה ב-YouTube"
                await text_channel.send(message)

        @self.bot.command(name='yalla')
        async def yalla(ctx):
            if not ctx.author.voice:
                await ctx.send("אתה חייב להיות בערוץ קולי!")
                return

            player = random.choice(list(self.AUDIO_FILES.keys()))
            audio_file = self.AUDIO_FILES[player]
            await self.play_audio(ctx.author.voice.channel, audio_file)

        @self.bot.command(name='roast')
        async def roast(ctx, target: Optional[discord.Member] = None):
            if not target:
                await ctx.send("אתה חייב לציין שחקן! לדוגמה: !roast @spyware")
                return

            if target.name in self.CUSTOM_MESSAGES:
                roast = random.choice(self.CUSTOM_MESSAGES[target.name])
            else:
                roast = f"🎮 {target.name} כל כך גרוע שאפילו ה-AI של 2025 מרגיש רחמים"
            await ctx.send(roast)

    async def handle_voice_channel_join(self, member, channel, text_channel):
        if member.name in self.CUSTOM_MESSAGES:
            message = random.choice(self.CUSTOM_MESSAGES[member.name])
        else:
            message = f"🎮 {member.name} נכנס לערוץ! מעניין אם ה-FIFA 25 כבר הוסיפה דרגת קושי מספיק נמוכה בשבילו"
        
        await text_channel.send(message)

        if member.name in self.AUDIO_FILES:
            await self.play_audio(channel, self.AUDIO_FILES[member.name])

    async def play_audio(self, voice_channel, audio_file):
        try:
            if not os.path.exists(audio_file):
                print(f'קובץ אודיו לא נמצא: {audio_file}')
                return

            voice_client = await voice_channel.connect()
            voice_client.play(discord.FFmpegPCMAudio(audio_file))
            
            while voice_client.is_playing():
                await asyncio.sleep(1)
            
            await voice_client.disconnect()

        except Exception as e:
            print(f'שגיאה בהשמעת האודיו: {str(e)}')
            try:
                if voice_client and voice_client.is_connected():
                    await voice_client.disconnect()
            except:
                pass

    async def start(self):
        try:
            print('מתחיל להריץ את הבוט...')
            if not self.DISCORD_TOKEN:
                raise ValueError("Token is missing! Please check your environment variables.")
            await self.bot.start(self.DISCORD_TOKEN)
        except Exception as e:
            print(f'שגיאה בהפעלת הבוט: {str(e)}')

if __name__ == "__main__":
    bot = DiscordBot()
    asyncio.run(bot.start()) 
