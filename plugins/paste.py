import asyncio
import os
import re
import socket
from asyncio import get_running_loop, sleep
from functools import partial
from io import BytesIO

import aiofiles
import aiohttp
from aiohttp import ClientSession
from pyrogram import filters

from VIPMUSIC import app


async def make_carbon(code):
    url = "https://carbonara.solopov.dev/api/cook"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json={"code": code}) as resp:
            image = BytesIO(await resp.read())
    image.name = "carbon.png"
    return image


aiohttpsession = ClientSession()

pattern = re.compile(r"^text/|json$|yaml$|xml$|toml$|x-sh$|x-shellscript$")


def _netcat(host, port, content):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.sendall(content.encode())
    s.shutdown(socket.SHUT_WR)
    while True:
        data = s.recv(4096).decode("utf-8").strip("\n\x00")
        if not data:
            break
        return data
    s.close()


async def paste(content):
    loop = get_running_loop()
    link = await loop.run_in_executor(None, partial(_netcat, "ezup.dev", 9999, content))
    return link


async def isPreviewUp(preview: str) -> bool:
    for _ in range(7):
        try:
            async with aiohttpsession.head(preview, timeout=2) as resp:
                status = resp.status
                size = resp.content_length
        except asyncio.TimeoutError:
            return False
        if status == 404 or (status == 200 and size == 0):
            await asyncio.sleep(0.4)
        else:
            return status == 200
    return False


@app.on_message(filters.command("paste"))
async def paste_func(_, message):
    if not message.reply_to_message:
        return await message.reply_text("**ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴍᴇssᴀɢᴇ ᴡɪᴛʜ /paste**")

    m = await message.reply_text("**ᴘᴀsᴛɪɴɢ ᴘʟs ᴡᴀɪᴛ 10 sᴇᴄ....**")

    if message.reply_to_message.text:
        content = str(message.reply_to_message.text)
    elif message.reply_to_message.document:
        document = message.reply_to_message.document
        if document.file_size > 1048576:
            return await m.edit("**ʏᴏᴜ ᴄᴀɴ ᴏɴʟʏ ᴘᴀsᴛᴇ ғɪʟᴇs sᴍᴀʟʟᴇʀ ᴛʜᴀɴ 1ᴍʙ.**")
        if not pattern.search(document.mime_type):
            return await m.edit("**ᴏɴʟʏ ᴛᴇxᴛ ғɪʟᴇs ᴄᴀɴ ʙᴇ ᴘᴀsᴛᴇᴅ.**")

        doc = await message.reply_to_message.download()
        async with aiofiles.open(doc, mode="r") as f:
            lines = await f.readlines()

        os.remove(doc)

        total_lines = len(lines)
        current_line = 0
        page_number = 1

        while current_line < total_lines:
            end_line = min(current_line + 50, total_lines)
            content_chunk = "".join(lines[current_line:end_line])
            carbon = await make_carbon(content_chunk)

            await m.delete()
            text = await message.reply("**✍️ᴘᴀsᴛᴇᴅ ᴏɴ ᴄᴀʀʙᴏɴ ᴘᴀɢᴇ !**")
            await asyncio.sleep(0.4)
            await text.edit("**ᴜᴘʟᴏᴀᴅɪɴɢ ᴜɴᴅᴇʀ 5 sᴇᴄ.**")
            await asyncio.sleep(0.4)
            await text.edit("**ᴜᴘʟᴏᴀᴅɪɴɢ ᴜɴᴅᴇʀ 5 sᴇᴄ....**")
            caption = f"✨ᴛʜɪs ɪs  {page_number} ᴘᴀɢᴇ - {current_line + 1} to {end_line} ʟɪɴᴇs..\n sᴇɴᴅɪɴɢ ᴍᴏʀᴇ ʟɪɴᴇs ɪғ ʜᴀᴠᴇ ᴏɴ ɴᴇxᴛ ᴘᴀɢᴇ ᴘʟᴇᴀsᴇ ᴡᴀɪᴛ..."
            await message.reply_photo(carbon, caption=caption)
            await text.delete()
            carbon.close()

            current_line = end_line
            page_number += 1
            await sleep(
                1
            )  # Optional: Add a sleep to avoid rate limiting or being blocked

    else:
        await m.edit("**Unsupported file type. Only text files can be pasted.**")


__MODULE__ = "ᴘᴀꜱᴛᴇ"
__HELP__ = """
**ᴘᴀsᴛᴇ ᴄᴏᴍᴍᴀɴᴅ**

ᴛʜɪs ᴄᴏᴍᴍᴀɴᴅ ᴀʟʟᴏᴡs ᴜsᴇʀs ᴛᴏ ᴘᴀsᴛᴇ ᴛᴇxᴛ ᴏʀ ᴛᴇxᴛ ғɪʟᴇs ᴛᴏ ᴀɴ ᴏɴʟɪɴᴇ sᴇʀᴠɪᴄᴇ ᴀɴᴅ ɢᴇɴᴇʀᴀᴛᴇ ᴄᴀʀʙᴏɴ ɪᴍᴀɢᴇs ғʀᴏᴍ ᴛʜᴇ ᴄᴏɴᴛᴇɴᴛ.

ғᴇᴀᴛᴜʀᴇs:
- ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴛᴇxᴛ ᴍᴇssᴀɢᴇ ᴏʀ ᴀ ᴛᴇxᴛ ғɪʟᴇ ᴛᴏ ᴘᴀsᴛᴇ ᴛʜᴇ ᴄᴏɴᴛᴇɴᴛ ᴛᴏ ᴀɴ ᴏɴʟɪɴᴇ sᴇʀᴠɪᴄᴇ ᴀɴᴅ ɢᴇɴᴇʀᴀᴛᴇ ᴀ ᴄᴀʀʙᴏɴ ɪᴍᴀɢᴇ.
- sᴜᴘᴘᴏʀᴛs ᴘᴀsᴛɪɴɢ ʙᴏᴛʜ ᴘᴀɪɴ ᴛᴇxᴛ ᴀɴᴅ ᴛᴇxᴛ ғɪᴇs.
- ᴀᴜᴛᴏᴍᴀᴛɪᴄʟʏ sᴘʟɪᴛs ʟᴀʀɢᴇ ᴛᴇxᴛ ғɪᴇs ɪɴᴛᴏ ᴍᴜʟᴛɪᴘʟᴇ ᴘᴀɢᴇs ɪғ ɴᴇᴇᴅᴇᴅ.
- ᴜᴘʟᴏᴀᴅs ᴛʜᴇ ɢᴇɴᴇʀᴀᴛᴇᴅ ᴄᴀʀʙᴏɴ ɪᴍᴀɢᴇs ᴀs ʀᴇᴘʟɪᴇs ᴛᴏ ᴛʜᴇ ᴏʀɪɢɪɴᴀʟ ᴍᴇssᴀɢᴇ.
- ᴅɪsᴘʟᴀʏs ᴀ ᴘʀᴏᴄᴇssɪɴɢ ᴍᴇssᴀɢᴇ ᴡʜɪʟᴇ ᴘᴀsᴛɪɴɢ ᴀɴᴅ ᴜᴘʟᴏᴀᴅɪɴɢ ᴛʜᴇ ᴄᴏɴᴛᴇɴᴛ.

ᴄᴏᴍᴍᴀɴᴅs:
- /paste: ʀᴇᴘʟʏ ᴛᴏ ᴀ ᴛᴇxᴛ ᴍᴇssᴀɢᴇ ᴏʀ ᴀ ᴛᴇxᴛ ғɪʟᴇ ᴛᴏ ɢᴇɴᴇʀᴀᴛᴇ ᴄᴀʀʙᴏɴ ɪᴍᴀɢᴇs ғʀᴏᴍ ᴛʜᴇ ᴄᴏɴᴛᴇɴᴛ.

ɴᴏᴛᴇ: ᴏɴʟʏ ᴛᴇxᴛ ғɪʟᴇs sᴍᴀʟᴇʀ ᴛʜᴀɴ 1MB ᴄᴀɴ ʙᴇ ᴘᴀsᴛᴇᴅ. ᴜɴsᴜᴘᴘᴏʀᴛᴇᴅ ғɪʟᴇ ᴛʏᴘᴇs ᴘʀᴏᴍᴘᴛ ᴀ ᴍᴇssᴀɢᴇ ɪɴᴅɪᴄᴀᴛɪɴɢ ᴛʜᴀᴛ ᴏɴʟʏ ᴛᴇxᴛ ғɪʟᴇs ᴄᴀɴ ʙᴇ ᴘᴀsᴛᴇᴅ.
"""
