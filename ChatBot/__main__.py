"""
✘ Commands Available -

• `{i}addai <reply to user/give username/userid>`
   Add a AI ChatBot to reply to that user.

• `{i}remai <reply to user/give username/userid>`
   Remove the AI ChatBot.

• `{i}repai <reply to user/give a message>`
   Reply to the user with a message by an AI.

• `{i}listai`
   List the currently AI added users.
"""
import asyncio
import os
import time
from random import choice

import requests
from pyUltroid import *
from pyUltroid._misc._assistant import asst_cmd, callback, in_pattern
from pyUltroid._misc._decorators import ultroid_cmd
from pyUltroid._misc._wrappers import eod, eor
from pyUltroid.dB import DEVLIST, ULTROID_IMAGES
from pyUltroid.functions.helper import *
from pyUltroid.functions.info import *
from pyUltroid.functions.misc import *
from pyUltroid.functions.tools import *
from pyUltroid.version import __version__, ultroid_version
from telethon import Button, events
from telethon.tl import functions, types
from pyUltroid.functions.tools import get_chatbot_reply

from .string import get_string



@ultroid_cmd(pattern="repai")
async def im_lonely_chat_with_me(event):
    if event.reply_to:
        message = (await event.get_reply_message()).message
    else:
        try:
            message = event.text.split(" ", 1)[1]
        except IndexError:
            return await eod(event, get_string("tban_1"), time=10)
    reply_ = await get_chatbot_reply(message=message)
    await event.eor(reply_)


@ultroid_cmd(pattern="addai")
async def add_chatBot(event):
    await chat_bot_fn(event, type_="add")


@ultroid_cmd(pattern="remai")
async def rem_chatBot(event):
    await chat_bot_fn(event, type_="remov")


@ultroid_cmd(pattern="listai")
async def lister(event):
    key = udB.get_key("CHATBOT_USERS") or {}
    users = key.get(event.chat_id, [])
    if not users:
        return await event.eor(get_string("chab_2"), time=5)
    msg = "**Total List Of AI Enabled Users In This Chat :**\n\n"
    for i in users:
        try:
            user = await event.client.get_entity(int(i))
            user = inline_mention(user)
        except BaseException:
            user = f"`{i}`"
        msg += "• {}\n".format(user)
    await event.eor(msg, link_preview=False)


async def chat_bot_fn(event, type_):
    if event.reply_to:
        user_ = (await event.get_reply_message()).sender
    else:
        temp = event.text.split(maxsplit=1)
        try:
            user_ = await event.client.get_entity(temp[1])
        except BaseException:
            if event.is_private:
                user_ = event.chat
            else:
                return await eod(
                    event,
                    get_string("chab_1"),
                )
    key = udB.get_key("CHATBOT_USERS") or {}
    chat = event.chat_id
    user = user_.id
    if type_ == "add":
        if key.get(chat):
            if user not in key[chat]:
                key[chat].append(user)
        else:
            key.update({chat: [user]})
    elif type_ == "remov":
        if key.get(chat):
            if user in key[chat]:
                key[chat].remove(user)
            if chat in key and not key[chat]:
                del key[chat]
    udB.set_key("CHATBOT_USERS", str(key))
    await event.eor(f"**ChatBot:**\n{type_}ed {inline_mention(user_)}")
