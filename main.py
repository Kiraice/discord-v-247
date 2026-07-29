import os
import asyncio
import discord
from discord.ext import commands
from http.server import HTTPServer, BaseHTTPRequestHandler
from threading import Thread

# 1. ระบบ Web Server เพื่อตอบรับ Render (ป้องการโดนปิดเพราะ Timeout)
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is active!")

    # ปิดการพิมพ์ Log ขยะลงหน้าจอ
    def log_message(self, format, *args):
        return

def run_web_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    server.serve_forever()

# 2. ตั้งค่า Discord Bot
intents = discord.Intents.default()
intents.voice_states = True
intents.guilds = True

bot = commands.Bot(command_prefix="!", intents=intents)

TOKEN = os.environ.get("DISCORD_TOKEN")
CHANNEL_ID = os.environ.get("VOICE_CHANNEL_ID")

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    
    if CHANNEL_ID:
        channel = bot.get_channel(int(CHANNEL_ID))
        if channel:
            try:
                # เชื่อมต่อห้องเสียง + หูตื่น (self_deaf=True)
                await channel.connect(reconnect=True, self_deaf=True)
                print(f"Connected to voice channel: {channel.name}")
            except Exception as e:
                print(f"Failed to connect: {e}")
        else:
            print("Channel ID not found!")

# 3. รันระบบ
if __name__ == "__main__":
    # เริ่ม Web Server แยก Thread
    Thread(target=run_web_server, daemon=True).start()
    
    # รันบอท
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("Error: DISCORD_TOKEN is missing!")
