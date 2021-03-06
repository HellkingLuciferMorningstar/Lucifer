#!/usr/bin/env python
# -*- coding: utf-8 -*-
from telethon import TelegramClient
from tgtk.core.HandleManager import add_handlers
from tgtk.core.getVars import get_val
import logging,asyncio
from tgtk.core.wserver import start_server_async
from tgtk.core.status.auto_delete import del_status
from pyrogram import Client
try:
    from tgtk.functions.rstuff import get_rstuff
except ImportError:pass

from tgtk.ttk_client import tgtkclient

if __name__ == "__main__":

    #logging stuff
    #thread name is just kept for future use
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(threadName)s %(name)s %(message)s"
    )
    logging.getLogger("pyrogram").setLevel(logging.ERROR)
    
    # parallel connections limiter
    queue = asyncio.Queue()
    exqueue = asyncio.Queue()
    
    for i in range(1,4):
        queue.put_nowait(i)

    for i in range(1,5):
        exqueue.put_nowait(i)
    
    # Telethon client creation
    ttkbot = tgtkclient("tgtkbot",get_val("API_ID"),get_val("API_HASH"))
    ttkbot.queue = queue
    ttkbot.exqueue = exqueue
    ttkbot.start(bot_token=get_val("BOT_TOKEN"))
    logging.info("telethon client created.")

    # Pyro Client creation and linking
    pyroclient = Client("pyrosession", api_id=get_val("API_ID"), api_hash=get_val("API_HASH"), bot_token=get_val("BOT_TOKEN"), workers=100)
    pyroclient.start()
    ttkbot.pyro = pyroclient
    logging.info("pyrogram client created.")

    # Associate the handlers
    add_handlers(ttkbot)

    ttkbot.loop.create_task(del_status())

    if get_val("IS_VPS"):
        ttkbot.loop.run_until_complete(start_server_async(get_val("SERVPORT")))
    try:
        ttkbot.loop.run_until_complete(get_rstuff())
    except:pass
    
    logging.info("it's on!")

    ttkbot.run_until_disconnected()