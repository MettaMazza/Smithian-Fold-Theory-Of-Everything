"""UNISON'S DISCORD FACE -- an interface ONLY. The engine is unison_chat.py;
this module carries messages across the server boundary and nothing else.
It is launched automatically by `python3 unison_chat.py` (the unified
system: one engine, one live memory, many faces) and shares that process's
orbits directly. Design (Maria's): every user message gets a THINKING
THREAD attached to it -- the chain of thought and the y/n feedback closure
live in the thread, the clean answer goes to the channel, and the thread
self-deletes after 2 minutes so chat stays clear."""
import asyncio, os

TOKEN_PATH = os.path.expanduser("~/.unison_discord_token")
CHANNEL = 1523685773998555227   # Unison listens ONLY here (plus its own
                                # thinking threads), never the whole server

def run(uc, rng=None):
    """Run the Discord face on an already-awake engine module `uc`."""
    import numpy as np
    import discord
    if rng is None:
        rng = np.random.default_rng()
    token = open(TOKEN_PATH).read().strip()

    intents = discord.Intents.default()
    intents.message_content = True
    client = discord.Client(intents=intents)
    PENDING = {}   # thread_id -> [user_id, question, answer, awaiting_correction]

    @client.event
    async def on_ready():
        uc.log("DISCORD", "live as " + str(client.user))
        print(f"UnisonAI is live on Discord as {client.user}", flush=True)

    @client.event
    async def on_message(msg):
        if msg.author.bot:
            return
        # feedback inside a thinking thread
        if isinstance(msg.channel, discord.Thread) and msg.channel.id in PENDING:
            entry = PENDING[msg.channel.id]
            uid, q, a, awaiting = entry
            text = msg.content.strip()
            if awaiting and text[:1].lower() != "y":
                # whatever she types now IS the corrected answer
                held = uc.record_correction(q, text.lstrip("nN ").strip(" :,-") if text[:1].lower() == "n" else text)
                entry[3] = False
                await msg.channel.send("⌁ held, permanently. Ask me again and I will say: " + held)
                return
            res = uc.apply_feedback(q, a, text, interface="discord")
            if res is None:          # bare n: ask for the correction in-thread
                entry[3] = True
                await msg.channel.send("⌁ withheld. What should I have said? Your next message here is held exactly.")
            elif res:
                await msg.channel.send("⌁ " + res)
            return
        if isinstance(msg.channel, discord.Thread):
            return
        if msg.channel.id != CHANNEL:     # locked: this channel only
            return
        line = msg.content.strip()
        if not line:
            return
        if line.startswith("/"):
            t = uc.toggle(line)
            await msg.reply(t or "commands: /auto /teach /selfplay", mention_author=False)
            return
        ans, thought = await asyncio.to_thread(uc.turn, line, rng, "discord")
        # answer clean in the channel
        await msg.reply(ans[:1900], mention_author=False)
        # thinking thread on the user's message: CoT + feedback closure
        try:
            th = await msg.create_thread(name="⌁ thinking", auto_archive_duration=60)
            PENDING[th.id] = [msg.author.id, line, ans, False]
            await th.send(f"⌁ {thought[:1800]}\n\nreply `y` or `n <the correct answer>` -- this thread folds away in 2 minutes.")
            async def fold_away(t=th):
                await asyncio.sleep(120)
                PENDING.pop(t.id, None)
                try:
                    await t.delete()
                except Exception:
                    pass
            asyncio.create_task(fold_away())
        except Exception as e:
            uc.log("DISCORD", "thread error: " + str(e))

    asyncio.run(client.start(token))

if __name__ == "__main__":
    # standalone fallback: wake the engine here, then run the face on it.
    # The primary launch is `python3 unison_chat.py`, which starts this
    # face automatically on its own live memory.
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "uc", os.path.join(os.path.dirname(os.path.abspath(__file__)), "unison_chat.py"))
    uc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(uc)
    run(uc)
