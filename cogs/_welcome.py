from discord import Forbidden
from discord.ext.commands import Cog
from discord.ext.commands import command



class Welcome(Cog):
	def __init__(self, client):
		self.client = client

	#@Cog.listener()
	#async def on_ready(self):
		#if not self.client.ready:
			#self.client.cogs_ready.ready_up("welcome")

	@Cog.listener()
	async def on_member_join(self, ctx):
		await self.client.change_presence(activity=ctx.Activity(type=ctx.ActivityType.watching,name=f'{len(self.client.users)} Members, razbot.uk.to'))
		print("Status updated, user joined.")


def setup(client):
	client.add_cog(Welcome(client))