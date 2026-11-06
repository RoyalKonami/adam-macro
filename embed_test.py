import discord_webhook


server_link = "https://www.roblox.com/share?code=5c16c5596ed6714db52e089c8bb7ae17&type=Server"
biome_webhook_url = "https://discord.com/api/webhooks/1567999438780104824/vz1Y7Hyu9RJpS_-cvs8nPy4EKyszOX64HSA5sAYM0SaPpdYtMvczZPUXTN63_tMHFUot"

biome = "snowy"
webhook = discord_webhook.DiscordWebhook(url=biome_webhook_url)


embed = discord_webhook.DiscordEmbed(
    title=f"{biome} started",
    description=f"Server Link: {server_link}",
    color=5814783
)

webhook.add_embed(embed)
webhook.execute()

