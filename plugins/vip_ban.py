import random

from pyrogram import *
from pyrogram.types import *

from VIPMUSIC import app
from VIPMUSIC.misc import SUDOERS
from VIPMUSIC.utils.vip_ban import admin_filter

vip_text = [
    "hey please don't disturb me.",
    "who are you",
    "fuck you dude",
    "You don't look like my owner",
    "hey why are you calling my name let me sleep",
    "tell me what is the work",
    "Look, I'm busy right now",
    "hey i am busy",
    "don't you understand what",
    "leave me alone",
    "dude what happend",
]

strict_txt = [
    "i can't restrict against my besties",
    "are you serious i am not restrict to my friends",
    "fuck you guys why should i tell my friends",
    "hey stupid admin ",
    "yes do this first, kill each other's enemies",
    "i can't hi is my closest friend",
    "i love him please don't restict this user try to usertand ",
]


ban = ["ban", "boom"]
unban = [
    "unban",
]
mute = ["mute", "silent", "shut"]
unmute = ["unmute", "speak", "free"]
kick = ["kick", "out", "nikaal", "nikal"]
promote = ["promote", "adminship"]
demote = ["demote", "lelo"]
group = ["group"]
channel = ["channel"]


# ========================================= #


@app.on_message(filters.command(["puki", "hush"], prefixes=["V", "H"]) & admin_filter)
async def restriction_app(app: app, message):
    reply = message.reply_to_message
    chat_id = message.chat.id
    if len(message.text) < 2:
        return await message.reply(random.choice(vip_text))
    bruh = message.text.split(maxsplit=1)[1]
    data = bruh.split(" ")

    if reply:
        user_id = reply.from_user.id
        for banned in data:
            print(f"present {banned}")
            if banned in ban:
                if user_id in SUDOERS:
                    await message.reply(random.choice(strict_txt))
                else:
                    await app.ban_chat_member(chat_id, user_id)
                    await message.reply(
                        "OK, Ban !"
                    )

        for unbanned in data:
            print(f"present {unbanned}")
            if unbanned in unban:
                await app.unban_chat_member(chat_id, user_id)
                await message.reply(f"Ok, aap bolte hai to unban kar diya")

        for kicked in data:
            print(f"present {kicked}")
            if kicked in kick:
                if user_id in SUDOERS:
                    await message.reply(random.choice(strict_txt))

                else:
                    await app.ban_chat_member(chat_id, user_id)
                    await app.unban_chat_member(chat_id, user_id)
                    await message.reply("get lost!")

        for muted in data:
            print(f"present {muted}")
            if muted in mute:
                if user_id in SUDOERS:
                    await message.reply(random.choice(strict_txt))

                else:
                    permissions = ChatPermissions(can_send_messages=False)
                    await message.chat.restrict_member(user_id, permissions)
                    await message.reply(f"muted successfully! Disgusting people.")

        for unmuted in data:
            print(f"present {unmuted}")
            if unmuted in unmute:
                permissions = ChatPermissions(can_send_messages=True)
                await message.chat.restrict_member(user_id, permissions)
                await message.reply(f"Huh, OK, sir!")

        for promoted in data:
            print(f"present {promoted}")
            if promoted in promote:
                await app.promote_chat_member(
                    chat_id,
                    user_id,
                    privileges=ChatPrivileges(
                        can_change_info=False,
                        can_invite_users=True,
                        can_delete_messages=True,
                        can_restrict_members=False,
                        can_pin_messages=True,
                        can_promote_members=False,
                        can_manage_chat=True,
                        can_manage_video_chats=True,
                    ),
                )
                await message.reply("promoted !")

        for demoted in data:
            print(f"present {demoted}")
            if demoted in demote:
                await app.promote_chat_member(
                    chat_id,
                    user_id,
                    privileges=ChatPrivileges(
                        can_change_info=False,
                        can_invite_users=False,
                        can_delete_messages=False,
                        can_restrict_members=False,
                        can_pin_messages=False,
                        can_promote_members=False,
                        can_manage_chat=False,
                        can_manage_video_chats=False,
                    ),
                )
                await message.reply("demoted !")


__MODULE__ = "ꜱᴍᴀʀᴛ-ʙᴀɴ"
__HELP__ = """
- `/puki`: [ʙᴀɴ ᴏʀ ᴜɴʙᴀɴ] ᴜsᴇʀs.
- `/hush`: [ᴍᴜᴛᴇ, ᴋɪᴄᴋ, ᴘʀᴏᴍᴏᴛᴇ, ᴏʀ ᴅᴇᴍᴏᴛᴇ] ᴜsᴇʀs.

ᴇxᴀᴍᴘʟᴇ:- ᴠɪᴘ ʙᴀɴ ᴛʜɪs ᴜsᴇʀ (ʀᴇᴘɪᴇᴅ ʜɪs ᴍᴇssᴀɢᴇ).

ɴᴏᴛᴇ:- ᴜsᴇ ᴡɪᴛʜᴏᴜᴛ ᴄᴏᴍᴍᴀɴᴅ.
"""
