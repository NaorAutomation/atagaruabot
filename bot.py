import discord
from discord.ext import commands
import random
import datetime
import asyncio
import os
from typing import Optional, Callable, Dict, List

class DiscordBot:
    def __init__(self):
        # הגדרות הבוט
        self.DISCORD_TOKEN = os.getenv('DISCORD_TOKEN', 'MTMyOTkxOTgxNzYzNzA0MDI0OA.GfDy49.xVsbR8e5OsdaxfaMqJpLdDjakmwbqIaplVuJ9o')
        self.TEXT_CHANNEL_NAME = 'fifa-20-talks'
        self.VOICE_CHANNELS = ['FIFA 22 PRO CLUB', 'FIFA 22 FUT CHAMPIONS']
        
        # נתיבים לקבצי אודיו
        self.AUDIO_FILES = {
            'kakibuy': os.path.join('static', 'audio', 'kakibuy.m4a'),
            'spyware': os.path.join('static', 'audio', 'spyware.m4a'),
            'elad1267': os.path.join('static', 'audio', 'elad.m4a')
        }
        
        # הודעות מותאמות אישית לשחקנים מיוחדים
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

        # הודעות כלליות למעבר בין ערוצים
        self.CHANNEL_SWITCH_MESSAGES = [
            "🎮 {user} עובר בין ערוצים כמו שהוא עובר בין הפסדים ב-FIFA",
            "⚽ {user} מחליף ערוצים בתקווה שאולי שם המזל ישתנה",
            "🎯 {user} בורח לערוץ אחר... כנראה הפסיד שוב",
            "🤖 {user} מחפש ערוץ שבו ה-AI יותר חלש",
            "🏆 {user} מנסה להתחמק מההיסטוריה שלו בערוץ הקודם"
        ]

        # הודעות כניסה לערוץ קולי
        self.JOIN_MESSAGES = [
            "🎮 {user} נכנס לערוץ! מעניין אם ה-FIFA 25 כבר הוסיפה דרגת קושי מספיק נמוכה בשבילו",
            "⚽ {user} הצטרף! אפילו השחקנים הוירטואליים מתחילים להזיע",
            "🎯 {user} במשחק! EA כבר מכינים פאץ' מיוחד",
            "🤖 הודעת מערכת: {user} התחבר. מפעיל מצב 'עזרה אוטומטית מוגברת'",
            "🏆 {user} הגיע! השרת עובר למצב 'שערים רחבים יותר' באופן אוטומטי"
        ]

        # הודעות יציאה מערוץ קולי
        self.LEAVE_MESSAGES = [
            "👋 {user} יצא מהערוץ. כנראה הלך לראות סרטוני הדרכה ב-YouTube",
            "🎮 {user} עזב אותנו. הולך לתרגל פנדלים... שוב",
            "⚽ {user} נעלם. אולי הלך לשחק משהו יותר קל, כמו Minecraft",
            "🎯 {user} התנתק. EA שולחים לו כבר הודעת עידוד",
            "🤖 {user} יצא מהמשחק. אפילו ה-AI מתגעגע כבר"
        ]

        # סטטיסטיקות
        self.stats = {
            'connected_users': 0,
            'voice_messages': 0,
            'total_actions': 0
        }

        # הגדרת הבוט עם כל ההרשאות הנדרשות
        intents = discord.Intents.all()
        self.bot = commands.Bot(command_prefix='!', intents=intents)
        
        # הגדרת האירועים
        self.setup_events()

    def setup_events(self):
        @self.bot.event
        async def on_ready():
            await self.log_message(f'הבוט {self.bot.user} מוכן!')
            for guild in self.bot.guilds:
                await self.log_message(f'מחובר לשרת: {guild.name}')
                self.stats['connected_users'] = len([m for m in guild.members if not m.bot])
                await self.update_stats()

        @self.bot.event
        async def on_voice_state_update(member, before, after):
            if member.bot:
                return

            await self.log_message(f'==== אירוע חדש ====')
            await self.log_message(f'משתמש: {member.name} ({member.display_name})')
            
            text_channel = discord.utils.get(member.guild.text_channels, name=self.TEXT_CHANNEL_NAME)
            if not text_channel:
                return

            # עדכון סטטיסטיקות
            self.stats['total_actions'] += 1
            await self.update_stats()

            # מעבר בין ערוצים
            if before.channel and after.channel and before.channel != after.channel:
                message = random.choice(self.CHANNEL_SWITCH_MESSAGES).format(user=member.name)
                await text_channel.send(message)
                
            # כניסה לערוץ חדש
            elif after.channel and after.channel.name in self.VOICE_CHANNELS:
                await self.handle_voice_channel_join(member, after.channel)
            
            # יציאה מערוץ
            elif before.channel and not after.channel:
                await self.handle_voice_channel_leave(member, before.channel)

        @self.bot.command(name='yalla')
        async def yalla(ctx):
            if not ctx.author.voice:
                await ctx.send("אתה חייב להיות בערוץ קולי!")
                return

            player = random.choice(list(self.AUDIO_FILES.keys()))
            audio_file = self.AUDIO_FILES[player]
            
            await self.log_message(f'הפעלת אודיו מפקודת yalla')
            await self.log_message(f'שחקן נבחר: {player}')
            
            await self.play_audio(ctx.author.voice.channel, audio_file)
            self.stats['voice_messages'] += 1
            self.stats['total_actions'] += 1
            await self.update_stats()

        @self.bot.command(name='roast')
        async def roast(ctx, target: Optional[discord.Member] = None):
            """פקודה להקנטת שחקן"""
            if not target:
                await ctx.send("אתה חייב לציין שחקן! לדוגמה: !roast @spyware")
                return

            # בדיקה אם יש הודעות מותאמות אישית לשחקן
            if target.name in self.CUSTOM_MESSAGES:
                roast = random.choice(self.CUSTOM_MESSAGES[target.name])
            else:
                roast = random.choice([
                    f"🎮 {target.name} כל כך גרוע שאפילו ה-AI של 2025 מרגיש רחמים",
                    f"⚽ שמעתם? {target.name} חושב שoffside זה סוג של אוכל",
                    f"🎯 {target.name} הוא ההוכחה שגם ב-2025 עדיין אפשר להיות גרוע ב-FIFA",
                    f"🤖 EA הוסיפו את הסטטיסטיקות של {target.name} כדוגמה למה לא לעשות"
                ])

            await ctx.send(roast)
            self.stats['total_actions'] += 1
            await self.update_stats()

    async def handle_voice_channel_join(self, member: discord.Member, channel: discord.VoiceChannel):
        """טיפול בכניסת משתמש לערוץ קולי"""
        text_channel = discord.utils.get(member.guild.text_channels, name=self.TEXT_CHANNEL_NAME)
        if not text_channel:
            return

        # שליחת הודעה מותאמת אישית או הודעת ברירת מחדל
        if member.name in self.CUSTOM_MESSAGES:
            message = random.choice(self.CUSTOM_MESSAGES[member.name])
        else:
            message = random.choice(self.JOIN_MESSAGES).format(user=member.name)
        
        await text_channel.send(message)

        # השמעת אודיו אם קיים
        if member.name in self.AUDIO_FILES:
            await self.play_audio(channel, self.AUDIO_FILES[member.name])
            self.stats['voice_messages'] += 1
            await self.update_stats()

    async def handle_voice_channel_leave(self, member: discord.Member, channel: discord.VoiceChannel):
        """טיפול ביציאת משתמש מערוץ קולי"""
        text_channel = discord.utils.get(member.guild.text_channels, name=self.TEXT_CHANNEL_NAME)
        if text_channel:
            message = random.choice(self.LEAVE_MESSAGES).format(user=member.name)
            await text_channel.send(message)

    async def play_audio(self, voice_channel: discord.VoiceChannel, audio_file: str):
        """השמעת קובץ אודיו בערוץ קולי"""
        try:
            if not os.path.exists(audio_file):
                await self.log_message(f'קובץ אודיו לא נמצא: {audio_file}')
                return

            await self.log_message(f'מנסה להתחבר לערוץ קולי: {voice_channel.name}')
            voice_client = await voice_channel.connect()
            await self.log_message(f'התחבר בהצלחה לערוץ קולי')

            await self.log_message(f'מתחיל להשמיע קובץ: {audio_file}')
            voice_client.play(discord.FFmpegPCMAudio(audio_file))
            
            while voice_client.is_playing():
                await asyncio.sleep(1)
            
            await self.log_message('סיום השמעת אודיו')
            await voice_client.disconnect()
            await self.log_message('התנתק מהערוץ הקולי')

        except Exception as e:
            await self.log_message(f'שגיאה בהשמעת האודיו: {str(e)}')
            try:
                if voice_client and voice_client.is_connected():
                    await voice_client.disconnect()
            except:
                pass

    async def log_message(self, message: str):
        """רישום הודעת לוג"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")
        
        # שליחה לממשק הווב אם קיים
        if hasattr(self, 'broadcast_log'):
            await self.broadcast_log(message)

    async def update_stats(self):
        """עדכון סטטיסטיקות בממשק הווב"""
        if hasattr(self, 'broadcast_stats'):
            await self.broadcast_stats(self.stats)

    async def start(self):
        """הפעלת הבוט"""
        try:
            await self.log_message('מתחיל להריץ את הבוט...')
            await self.bot.start(self.DISCORD_TOKEN)
        except Exception as e:
            await self.log_message(f'שגיאה בהפעלת הבוט: {str(e)}')

# יצירת אובייקט הבוט
bot = DiscordBot()
