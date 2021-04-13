# RazBot Docs

### Languages: Python 3
### Packages Used: Random, Discord, datetime, time, asyncio, os, aiofiles, time, discord_slash (for slash commands)

## The Code:
### How it works: (most important bits only listed here, like starting and defining stuff)
![image](https://user-images.githubusercontent.com/56600481/114587909-05ad7c00-9c7e-11eb-8b1e-a8fbcd92d5ec.png)
![image](https://user-images.githubusercontent.com/56600481/114589809-efa0bb00-9c7f-11eb-90d4-7b51f1d32c94.png)




## Commands:
### Moderation commands:
### "raz!ban [user-ping] [reason", bans the user with the reason if provided. Requires ban permisson role in Discord.
![image](https://user-images.githubusercontent.com/56600481/114583458-81f19080-9c79-11eb-97bf-15d577479cba.png)
#
### "raz!unban [user-ping]", unbans the user. Requieres ban permisson role.
![image](https://user-images.githubusercontent.com/56600481/114584218-54f1ad80-9c7a-11eb-9983-cf8eb65a7cff.png)
#
### "raz!mute [user-ping]", looks for the "Muted" role in the discord server and applies it to the user pinged. Requires the kick members permisson in Discord.
![image](https://user-images.githubusercontent.com/56600481/114584574-ba459e80-9c7a-11eb-905c-fffc0cc3de35.png)
#
### "raz!unmute [user-ping]", looks for the "Muted" role in the discord server and removes it from the user pinged. Requires the kick members permisson in Discord.
![image](https://user-images.githubusercontent.com/56600481/114584992-1a3c4500-9c7b-11eb-997c-75004d98c9cd.png)
#
### "raz!tempmute [user-ping] [Number] [s/m/h/d]", looks for the "Muted" role in the discord server and applies it to the user pinged for the time specified. Requires the kick members permisson in Discord. Important: The space between [Number] and [s/m/h/d] is needed.
![image](https://user-images.githubusercontent.com/56600481/114585133-3cce5e00-9c7b-11eb-9712-2746abd3d6d0.png)
#
### "raz!kick [user-ping]", kicks the user specified from the Discord Server. Requires the kick members permisson in Discord.
![image](https://user-images.githubusercontent.com/56600481/114585352-74d5a100-9c7b-11eb-91c2-3a2b19f9ef38.png)
Also sends a DM to the person that ran the command: ![image](https://user-images.githubusercontent.com/56600481/114585412-83bc5380-9c7b-11eb-90a7-cdea432b9d3f.png)
#
### "raz!clear [number]", clears the number of messages specified. 
No image needed.
#
### "raz!lockdown", puts the channel ran in, in lockdown; meaning people with normal roles (not higher up) cant speak in it. Requires manage_channels permisson.
![image](https://user-images.githubusercontent.com/56600481/114585630-c0884a80-9c7b-11eb-80c1-8c623b0036d0.png)
#
### "raz!unlock", undoes the lockdown command. Requires manage_channels permisson.
![image](https://user-images.githubusercontent.com/56600481/114585661-ca11b280-9c7b-11eb-8dd4-c37f1e1b0a63.png)
#
### "raz!say [message]", says the message as the bot. Requires admin permisson in discord. 
![image](https://user-images.githubusercontent.com/56600481/114586031-24127800-9c7c-11eb-8520-66ad8c2d0e0e.png)
#
### raz!warn [user-ping] [reason]", warns the user specified and saves it to the file for the server. Requires ban_members permisson in discord.
![image](https://user-images.githubusercontent.com/56600481/114586292-6936aa00-9c7c-11eb-9c05-56adef2a0286.png)
#
### "raz!warnings [user-ping]", views the warnings for the user specified from the server file.
![image](https://user-images.githubusercontent.com/56600481/114586364-7b184d00-9c7c-11eb-9047-0895821e9777.png)
#
###
