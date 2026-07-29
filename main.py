import os
import asyncio
import discord
from discord.ext import commands
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread

# 1. รัน Web Server เล็กๆ สำหรับ Render Health Check
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is online!")

    def log_message(self, format, *args):
        return  # ซ่อน Log ไม่ให้รกหน้าจอ

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    server.serve_forever()

# 2. ตั้งค่าบอท Discord
intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

TOKEN = os.environ.get("DISCORD_TOKEN")
CHANNEL_ID = os.environ.get("VOICE_CHANNEL_ID")

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} (ID: {bot.user.id})")
    
    if CHANNEL_ID:
        try:
            channel = bot.get_channel(int(CHANNEL_ID))
            if channel:
                # เชื่อมต่อห้องเสียง
                await channel.connect(reconnect=True, self_deaf=True)
                print(f"Successfully connected to: {channel.name}")
            else:
                print("1092498035369582592")
        except Exception as e:
            print(f"Voice connection error: {e}")
    else:
        print("1092498035369582592")

# 3. เริ่มรันโปรเซส
if __name__ == "__main__":
    # เริ่ม Web Server ใน Background
    Thread(target=run_web_server, daemon=True).start()
    
    # รันบอท
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("MTUzMTk5MzMwMzI5MjE4MjYzOA.Gd23CD.CxP4LlCe4eTsxfkNd2t0IN8q003m_CeRC183u8")
