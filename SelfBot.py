import asyncio
import discord
import time
client = discord.Client()
whitelist_ids = [814114292383088650, 854770475178655764, 806178036915240960, 1166145962083885177, 1260367684047077386, 860187841212317756, 933789771451465758, 1236742440011038811, 1192115932454211605]  # Integers


# 1
async def clear_chats():
    private_channels = client.private_channels
    for channel in private_channels:
        if channel.id not in whitelist_ids:
            messages = channel.history(limit=None)
            async for message in messages:
                if message.author.id == client.user.id:
                    try:
                        await message.delete()
                    except Exception:
                        print("                                                   Error occured, going to next message")
                    print(f"                                                   Deleted message with ID: {message.id}")
                    time.sleep(2)

    print("Finished Clearing All Chats")


# 2
async def create_channel():
    server_id = int(input("Enter Server's ID: ").strip())
    category_id = int(input("Enter Category's ID (Enter 0 If None): ").strip())
    channel_name = input("Enter Channel Name: ").strip()
    channel_type = input("Enter Desired Channel Type (Text/Voice): ").strip().lower()
    permissions = input("Enter Channel Permissions (Comma-Seperated): ").strip().split(',')
    allowed_permissions = [perm.strip() for perm in permissions if perm]

    guild = client.get_guild(server_id)
    if not guild:
        print("Server not found.")
        return

    if channel_type == 'text':
        channel_type = discord.ChannelType.text
    elif channel_type == 'voice':
        channel_type = discord.ChannelType.voice
    else:
        print("Invalid Channel Type. Choose 'Text' Or 'Voice'.")
        return

    category = None
    if category_id != 0:
        category = discord.utils.get(guild.categories, id=category_id)
        if not category:
            print("Category Not Found.")
            return

    overwrites = {
        guild.default_role: discord.PermissionOverwrite()
    }
    for perm in allowed_permissions:
        if hasattr(discord.Permissions, perm):
            overwrites[guild.default_role].update(**{perm: True})

    try:
        if category:
            await guild.create_text_channel(channel_name, category=category,overwrites=overwrites) if channel_type == discord.ChannelType.text else await guild.create_voice_channel(

                channel_name, category=category, overwrites=overwrites)
        else:
            await guild.create_text_channel(channel_name,
                                            overwrites=overwrites) if channel_type == discord.ChannelType.text else await guild.create_voice_channel(
                channel_name, overwrites=overwrites)

        print(f"Channel '{channel_name}' Created Successfully.")
    except Exception as e:
        print(f"Error occurred: {e}")
    await client.close()


# 3
async def create_role():
    server_id = int(input("Enter Server's ID: ").strip())
    role_name = input("Enter Role's Name: ").strip()

    # Input and process the color
    role_color_hex = input("Enter Role's Color (Hexadecimal, e.g., 0x1ABC9C or #FF0000): ").strip()
    if role_color_hex.startswith("#"):
        role_color = int(role_color_hex[1:], 16)
    else:
        role_color = int(role_color_hex, 16)

    permissions = input("Enter Role's Permissions (Comma-Separated, e.g., send_messages,view_channel): ").strip().split(',')

    guild = client.get_guild(server_id)
    if not guild:
        print("Server not found.")
        return

    # Create permissions object
    role_permissions = discord.Permissions()
    for perm in permissions:
        if hasattr(discord.Permissions, perm):
            setattr(role_permissions, perm.strip(), True)
        else:
            print(f"Permission '{perm}' is not valid.")

    try:
        # Create the role
        await guild.create_role(
            name=role_name,
            color=discord.Color(role_color),
            permissions=role_permissions
        )
        print(f"Role '{role_name}' created successfully.")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        await client.close()


@client.event
async def on_ready():
    art = """                                                                                          
     _______   ________  _______   _______  __      __         ______   ________  __        ________        _______    ______  ________ 
    |       \ |        \|       \ |       \ |  \    /  \       /      \ |        \|  \      |        \      |       \  /      \|        \\
    | $$$$$$$\| $$$$$$$$| $$$$$$$\| $$$$$$$\ \$$\  /  $$      |  $$$$$$\| $$$$$$$$| $$      | $$$$$$$$      | $$$$$$$\|  $$$$$$\\$$$$$$$$
    | $$__/ $$| $$__    | $$__| $$| $$__| $$ \$$\/  $$       | $$___\$$| $$__    | $$      | $$__          | $$__/ $$| $$  | $$  | $$   
    | $$    $$| $$  \   | $$    $$| $$    $$  \$$  $$         \$$    \ | $$  \   | $$      | $$  \         | $$    $$| $$  | $$  | $$   
    | $$$$$$$ | $$$$$   | $$$$$$$\| $$$$$$$\   \$$$$          _\$$$$$$\| $$$$$   | $$      | $$$$$         | $$$$$$$\| $$  | $$  | $$   
    | $$      | $$_____ | $$  | $$| $$  | $$   | $$          |  \__| $$| $$_____ | $$_____ | $$            | $$__/ $$| $$__/ $$  | $$   
    | $$      | $$     \| $$  | $$| $$  | $$   | $$           \$$    $$| $$     \| $$     \| $$            | $$    $$ \$$    $$  | $$   
     \$$       \$$$$$$$$ \$$   \$$ \$$   \$$    \$$            \$$$$$$  \$$$$$$$$ \$$$$$$$$ \$$             \$$$$$$$   \$$$$$$    \$$ 
    """

    print(art)

    while True:
        print("                                                   1 - Clearing Chats")
        print("                                                   2 - Create Channel")
        print("                                                   3 - Create Role")
        print("                                                   4 - Exit Menu")
        choose = input("                                                   Choose An Option: ").strip()
        print("")
        if choose == '1':
            print("                                               Deleting All Messages From DMs...")
            await clear_chats()
        elif choose == '2':
            await create_channel()
        elif choose == '3':
            await create_role()
        elif choose == '4':
            print("Exiting...")
            await client.close()
            break
        else:
            print("Invalid Choice")


async def run_bot():
    await client.start("DISCORD-TOKEN")


if __name__ == "__main__":
    asyncio.run(run_bot())
