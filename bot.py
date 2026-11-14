import discord
from datetime import datetime
import json
import os
import random
import discord
from discord.ext import commands

# --- THÊM ĐOẠN CẤU HÌNH NÀY ---
DATA_FILE = "level_data.json"
ROLE_REWARDS = {
    2: "npc mới vào",
    5: "npc common(đã chơi 1 tuần)",
    10: "npc sơ cấp (đã vào 1 tháng)",
    20: "npc trung thành ( 3 tháng đồng hành )",
    99:"Nhân viên",
    }


def load_data():
  if os.path.exists(DATA_FILE):
    with open(DATA_FILE, "r", encoding="utf-8") as f:
      return json.load(f)
  return {}


def save_data(data):
  with open(DATA_FILE, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4)

from discord.ext import commands

# 1. Cấu hình Intents (Quyền cho phép bot đọc tin nhắn)
intents = discord.Intents.default()
intents.message_content = True
intents.members = True


# 2. Khởi tạo bot với tiền tố lệnh là dấu '!'
bot = commands.Bot(command_prefix="!", intents=intents)


# 3. Sự kiện khi bot kết nối thành công lên Discord
@bot.event
async def on_ready():
  print(f"Bot đã đăng nhập thành công: {bot.user}")


# 4. Lệnh Slash Command (/ping)
@bot.slash_command(
    name="ping", description="Kiểm tra xem bot có đang hoạt động không!"
)
async def ping(ctx):
  await ctx.respond(f"Pong! Chào {ctx.author.mention}, bot đang chạy mượt mà.")


# 5. Xử lý tin nhắn chat thường (!hello) và chuyển tiếp tiến trình
@bot.event
async def on_message(message):
  # Bỏ qua tin nhắn do chính bot gửi
  if message.author == bot.user:
    return
    data = load_data()
    user_id = str(message.author.id)
    # Lấy ngày hiện tại theo định dạng Năm-Tháng-Ngày (Ví dụ: "2026-11-14")
    hom_nay = datetime.now().strftime("%Y-%m-%d")

    # Nếu là người mới thì tạo dữ liệu (thêm mục last_date để lưu ngày)
    if user_id not in data:
      data[user_id] = {"exp": 0, "level": 1, "last_date": ""}

    # Kiểm tra xem hôm nay người này đã nhận điểm chưa
    if data[user_id].get("last_date") != hom_nay:
      data[user_id]["last_date"] = hom_nay  # Đánh dấu đã nhận điểm hôm nay
      data[user_id]["exp"] += 1  # Cộng đúng 1 điểm

      # Mốc EXP cần để lên cấp (Ví dụ: Cấp 1 cần 2 điểm, Cấp 2 cần 5 điểm... hoặc giữ nguyên level * 100)
      exp_can_thiet = data[user_id]["level"] * 10

      await message.channel.send(
          f"✨ {message.author.mention} đã điểm danh hôm nay và nhận **+1 EXP**"
          f" ({data[user_id]['exp']}/{exp_can_thiet})",
          delete_after=5,
      )

      # Kiểm tra lên cấp
      if data[user_id]["exp"] >= exp_can_thiet:
        data[user_id]["level"] += 1
        data[user_id]["exp"] = 0
        new_level = data[user_id]["level"]

        thong_bao = (
            f"🎉 mãi mới lên à gà thế {message.author.mention} đã thăng lên"
            f" **Cấp {new_level}**!"
        )
        if new_level in ROLE_REWARDS:
          role = discord.utils.get(
              message.guild.roles, name=ROLE_REWARDS[new_level]
          )
          if role:
            try:
              await message.author.add_roles(role)
              thong_bao += f"\n🏅 Bạn đã nhận được vai trò **{role.name}**!"
            except discord.Forbidden:
              thong_bao += "\n⚠️ *(Lỗi: Hãy kéo Role của Bot lên cao hơn!)*"
        await message.channel.send(thong_bao)

      save_data(data)

    if new_level in ROLE_REWARDS:
      role = discord.utils.get(
          message.guild.roles, name=ROLE_REWARDS[new_level]
      )
      if role:
        try:
          await message.author.add_roles(role)
          thong_bao += f"\n🏅 Bạn đã nhận được vai trò **{role.name}**!"
        except discord.Forbidden:
          thong_bao += "\n⚠️ *(Lỗi: Hãy kéo Role của Bot lên cao hơn!)*"
    await message.channel.send(thong_bao)
  data = load_data()
  user_id = str(message.author.id)
  save_data(data)
  # --- KẾT THÚC ĐOẠN CHÈN ---
  # Khai báo biến msg để lưu nội dung tin nhắn dạng chữ thường
  msg = message.content.lower()

  # Kiểm tra lệnh chat ở đây
  if "conyeubovuong" in msg or "chào" in msg or "hi" in msg or "hello" in msg:
    await message.channel.send(
        f"Cút {message.author.mention}! Chỗ Bố Đang Bận Đi Ra Kia Chơi."
    )

  # Bắt buộc phải có dòng này để bot không bị treo khi xử lý lệnh khác
  await bot.process_commands(message)


  # Lệnh chat prefix !hello
  if msg == message.content.lower == (" conyeubovuong in msg    or chào in msg     or hi in msg     or hello in msg"):
    await message.channel.send(
        f"Cút {message.author.mention}! Chỗ Bố Đang Bận Đi Ra Kia Chơi."
    )

  # Bắt buộc phải có dòng này để bot không bị treo khi xử lý lệnh khác
  await bot.process_commands(message)
# Sự kiện tự động chào người mới vào server
@bot.event
async def on_member_join(member):
  for channel in member.guild.text_channels:
    if "chung" in channel.name.lower() or "welcome" in channel.name.lower():
            await channel.send(
          f"🎉 Chào mừng NPC {member.mention} đã đến với server **{member.guild.name}**!"
      )
    break




# 6. Chạy bot (Hãy thay thế đoạn trong ngoặc bằng Token thực tế của bạn)
bot.run("MTU3MDc5NzAzMTUyODU5OTY2Mw.GLQCi1.x146J0feESSES-GVW8P65Ejo9_5i9vzcW19oQg")
