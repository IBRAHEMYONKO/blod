
import discord
from discord.ext import commands
from discord.ui import Button, View

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user.name}")

# إرسال رسالة تحتوي على زر التذكرة
@bot.command()
@commands.has_permissions(administrator=True)
async def setup_ticket(ctx):
    button = Button(label="🎟️ فتح تذكرة", style=discord.ButtonStyle.green)

    async def button_callback(interaction):
        guild = interaction.guild
        author = interaction.user
        category = discord.utils.get(guild.categories, name="Tickets")
        if not category:
            category = await guild.create_category("Tickets")

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(read_messages=False),
            author: discord.PermissionOverwrite(read_messages=True),
            guild.me: discord.PermissionOverwrite(read_messages=True)
        }

        ticket_channel = await guild.create_text_channel(f"ticket-{author.name}", category=category, overwrites=overwrites)
        await ticket_channel.send(f"{author.mention} شكرًا لفتحك تذكرة. سيتم مساعدتك قريبًا.")
        await interaction.response.send_message(f"✅ تم إنشاء تذكرتك: {ticket_channel.mention}", ephemeral=True)

    button.callback = button_callback

    view = View()
    view.add_item(button)
    await ctx.send("اضغط الزر لفتح تذكرة:", view=view)

# شغل البوت
bot.run("YOUR_BOT_TOKEN")
