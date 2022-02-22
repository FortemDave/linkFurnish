import discord
import os
import linkfuncs
from stayin_alive import keep_alive
import asyncio

client = discord.Client()


@client.event
async def on_ready():
	print(f"Hello Discord!,{client.user}")

	await client.wait_until_ready()
	# channel = client.get_channel(id=907842954201288804) # channel_id
	
	channels = linkfuncs.getlivechannels()
	while not client.is_closed():
		classInfo = linkfuncs.periodicClassLink()
		# if classInfo == None:
		# 	await channel.send("No Class Now")
		if classInfo != None and classInfo[2] != None:
			# -------------------------------
			for id_chan in channels:
				channel = client.get_channel(id = id_chan)

				class_link,class_code,class_name = classInfo[0],classInfo[1],classInfo[2]

				link = discord.Embed(
				title=f"{class_name}",
				description=f'[{class_code}]({class_link})',
				color=discord.Color.magenta())
				class_link = class_link + "?pli=1&authuser=1"

				authlink = discord.Embed(
				title=f"{class_name} - Authuser-1",
				description=f'[{class_code}]({class_link})',
				color=discord.Color.dark_gold())

				await channel.send(embed=link)
				await channel.send(embed=authlink)
				await asyncio.sleep(1)

				if class_code == "CS204":
					class_link = "https://meet.google.com/zjb-zkiq-pok"
					link = discord.Embed(
					title=f"{class_name} [SEC A]",
					description=f'[{class_code}]({class_link})',
					color=discord.Color.magenta())

					class_link = class_link + "?pli=1&authuser=1"
					authlink = discord.Embed(
					title=f"{class_name} [SEC A]- Authuser-1",
					description=f'[{class_code}]({class_link})',
					color=discord.Color.dark_gold())

					await asyncio.sleep(1)
					await channel.send(embed=link)
					await asyncio.sleep(0.5)
					await channel.send(embed=authlink)

				await asyncio.sleep(10)
		await asyncio.sleep(14 * 60) # task runs every 60 seconds


@client.event
async def on_message(message):
	if message.author == client.user:
		return

	if message.content.startswith("|"):
		if message.content[1:] == "table":
			time_lst = linkfuncs.todaySchedule()
			msg = ""
			if time_lst == None:
				msg = msg + "Its's a holiday dumbass."
				link = discord.Embed(
					title	=	f"\t\tToday's Time Table",
					description=msg,
					color	=	discord.Color.dark_gold())

				await message.channel.send(embed=link)
			else:
				for val in time_lst:
					cls = val[0]
					time = val[1]
					if time // 12 >= 1:
						time = time - 12
						if time != 0:
							time = f"{time}:P.M."
						else:
							time = f"12:P.M."
					else:
						time = f"{time}:A.M."

					x = 40 - len(cls)
					msg = msg + "\n" + f'{cls}'
					for iter in range(x):
						msg = msg + "-"
					msg = msg + f"{time}"

				msg = "```" + msg + "```";

				link = discord.Embed(
					title	=	f"\t\tToday's Time Table",
					description=msg,
					color	=	discord.Color.dark_gold())

				await message.channel.send(embed=link)
		elif message.content[1:7] == "update":
			msg_parts = message.content.split()
			if len(msg_parts) == 3:
				val = linkfuncs.updateLink(msg_parts[1],str(msg_parts[2]))
				if val == 1:
					link = discord.Embed(
					title	=	f"\tLink Updated!",
					color	=	discord.Color.red())
					await message.channel.send(embed=link)
				else:
					link = discord.Embed(
					title	=	f"\t\tToday's Time Table",
					description=f"{msg_parts[1]} is an invalid class Code",
					color	=	discord.Color.green())
					await message.channel.send(embed=link)
					
		elif message.content[1:4] == "ink":

			subject_string = message.content[4:]
			if len(subject_string) > 0:
				subject_string = subject_string.lower().strip()
				print(subject_string)
				class_link,class_name,class_code = linkfuncs.nameToLink(subject_string)

				if class_link == None:
					await message.channel.send(f"\
					Use the following codes below:\n \
					**la** - Linear Algebra\n \
					**toc**  - Theory Of Computation\n \
					**os**   - Operating System\n \
					**se**   - Software Engineering\n \
					**dbms**  - Database Management Systems\n \
					**et**  - Ethics")
				elif class_link != None:

					link = discord.Embed(
					title=f"{class_name}",
					description=f'[{class_code}]({class_link})',
					color=discord.Color.magenta())

					class_link = class_link + "?pli=1&authuser=1"
					authlink = discord.Embed(
					title=f"{class_name} - Authuser-1",
					description=f'[{class_code}]({class_link})',
					color=discord.Color.dark_gold())
					

					await message.channel.send(embed=link)
					await message.channel.send(embed=authlink)

					# secALink(message,class_code,class_name)
					if class_code == "CS204":
						class_link = "https://meet.google.com/zjb-zkiq-pok"
						link = discord.Embed(
						title=f"{class_name} [SEC A]",
						description=f'[{class_code}]({class_link})',
						color=discord.Color.magenta())

						class_link = class_link + "?pli=1&authuser=1"
						authlink = discord.Embed(
						title=f"{class_name} [SEC A]- Authuser-1",
						description=f'[{class_code}]({class_link})',
						color=discord.Color.dark_gold())
						

						await message.channel.send(embed=link)
						await message.channel.send(embed=authlink)

			else:
				await message.channel.send(f"Usage: |ink all [for all codes]")

		elif message.content[1:7] == "check":
			linkfuncs.checkCHannel()
			channels = linkfuncs.getlivechannels()
			for id_chan in channels:
				channel = client.get_channel(id = id_chan)
				await channel.send("This Channel IS ACTIVE")

		elif message.content[1:14] == "prateektable":

			link = discord.Embed(
				title = "Prateek's Timetable",
				description='[Github Link](https://prateekin.github.io/timetable/)',
				color=discord.Color.blue()
			)
			await message.channel.send(embed=link)

		elif message.content[1:7] == "daily":
			channel_id = message.channel.id
			check = linkfuncs.channelsupdate(channel_id)
			if check == 1:
				await message.channel.send("""You will now be recieving CSE Links before the class [5-15 minutes
				prior]. To disable this feature"""
				+ """ reuse the previous command""")
			else:
				await message.channel.send("Feature disabled. To re-enable it, retype the command again.")
			
		elif message.content[1:5] == "ive":

			class_link,class_code,class_name = linkfuncs.liveClassCodeLink()
			# print(class_link)
			if class_link == None:
				await message.channel.send("No class right now bruh.")
			elif class_link != None:
				

				link = discord.Embed(
				title=f"{class_name}",
				description=f'[{class_code}]({class_link})',
				color=discord.Color.magenta())

				class_link = class_link + "?pli=1&authuser=1"
				authlink = discord.Embed(
				title=f"{class_name} - Authuser-1",
				description=f'[{class_code}]({class_link})',
				color=discord.Color.dark_gold())
				

				await message.channel.send(embed=link)
				await message.channel.send(embed=authlink)

				# secALink(message,class_code,class_name)
				if class_code == "CS204":
					class_link = "https://meet.google.com/zjb-zkiq-pok"
					link = discord.Embed(
					title=f"{class_name} [SEC A]",
					description=f'[{class_code}]({class_link})',
					color=discord.Color.magenta())

					class_link = class_link + "?pli=1&authuser=1"
					authlink = discord.Embed(
					title=f"{class_name} [SEC A]- Authuser-1",
					description=f'[{class_code}]({class_link})',
					color=discord.Color.dark_gold())
					

					await message.channel.send(embed=link)
					await message.channel.send(embed=authlink)
					

		
		else:
			msg = """Type:
					|table -> Today's Time Table

					|ive   -> Link of the Current/Next Class
							(in case the link gets lost in 
							 the comments.)

					|ink [subject_code] -> Grants you the link
					Eg. |ink et
					(type an incorrect code to get the code list)

					|daily -> Use this command in a channel to
					recieve the links of the classes before it
					commences everytime

					|prateektable -> Link to the Timetable created by Prateek,Includes CSE+ECE Timetable along with other information.

					Website Owner and Manager: Prateek


					Bot Creator: FortemDave

					Note:
					*The 'l' is the vertical bar.
					(found with  the 'backward slash' key) 
					*Click on 'trust this domain'
					to avoid repeated confirmations
					in the embeded link"""

			link = discord.Embed(
					title	=	f"\tHelp Box",
					description=msg,
					color	=	discord.Color.dark_gold())

			await message.channel.send(embed=link)


keep_alive()
bot_token = "OTExMTkwODk1MzIyMzM3MzAx.YZdypg.IEWKgOTJ82vtk3RRWcJjTuGEmZs"
client.run(bot_token)



# def secALink(message,class_code,class_name):
# 	if class_code == "CS204":
# 		class_link = "https://meet.google.com/zjb-zkiq-pok"
# 		link = discord.Embed(
# 		title=f"{class_name} [SEC A]",
# 		description=f'[{class_code}]({class_link})',
# 		color=discord.Color.magenta())

# 		class_link = class_link + "?pli=1&authuser=1"
# 		authlink = discord.Embed(
# 		title=f"{class_name} [SEC A]- Multi-Acc Link",
# 		description=f'[{class_code}]({class_link})',
# 		color=discord.Color.dark_gold())
		

# 		await message.channel.send(embed=link)
# 		await message.channel.send(embed=authlink)

# 		pass
# -----------------------------------------------------------
# class_link = str(class_link) + "?pli=1&authuser=1"
# link = discord.Embed(
# title=f"{class_name}",
# description=f'[{class_code}]({class_link})',
# color=discord.Color.teal())

# await message.channel.send(embed=link)