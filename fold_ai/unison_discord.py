"""UNISON ON DISCORD -- the seed, live in a server.
Design (Maria's): every user message gets a THINKING THREAD attached to it --
the chain of thought and the y/n feedback closure live in the thread, the
clean answer goes to the channel, and the thread self-deletes after 2
minutes so chat stays clear. The engine wakes ONCE at startup; every
exchange learns (the Learning Law), every fact persists."""
import asyncio, re, os, sys, time
import numpy as np
import discord

TOKEN = open(os.path.expanduser("~/.unison_discord_token")).read().strip()

print("waking the seed (one-time read)...", flush=True)
import importlib.util, io, contextlib
spec = importlib.util.spec_from_file_location("uc", os.path.join(os.path.dirname(os.path.abspath(__file__)), "unison_chat.py"))
uc = importlib.util.module_from_spec(spec)
_wake = io.StringIO()
with contextlib.redirect_stdout(_wake):
    spec.loader.exec_module(uc)
print(_wake.getvalue().strip()[-200:], flush=True)
rng = np.random.default_rng()

PENDING = {}   # thread_id -> (user_id, question, answer)

def turn(line):
    """One conversational turn: returns (answer, thought)."""
    is_question = line.endswith("?") or line.lower().startswith(
        ("what","who","how","why","when","where","do ","does","did","can ","is ","are "))
    is_command = bool(re.match(r"(?i)\s*(say|repeat after me|respond with|reply with)\b", line))
    if not is_question and not is_command:
        if not uc.content_words(line):
            return "okay.", "contentless; acknowledged, not held"
        got = uc.learn_fact(line)
        fact = uc.flip_perspective(line if line[-1:] in ".!" else line + ".")
        uc.write_orbits(uc.tok(fact + "\n") * 3)
        uc.hold_sentence(fact, "told")
        return ("Held. " + fact), ("telling held" + (" as a relation fact" if got else " at the prediction state"))
    ans, thought = uc.reply(line, rng)
    return uc.dedup(ans), thought

def apply_feedback(question, answer, fb_text):
    fb = fb_text.strip()
    if fb[:1].lower() == "y":
        uc.write_orbits(uc.tok("Q: " + question + "\nA: " + answer + "\n") * 3)
        uc.hold_sentence(answer, "confirmed")
        with open(uc.FEEDBACK_LOG, "a") as f:
            f.write("CONF\t" + uc.qkey(question) + "\t" + answer + "\n")
        return "consolidated -- this exchange joins the held cycle."
    if fb[:1].lower() == "n":
        uc.REJECTED.add((uc.qkey(question), answer.strip()))
        with open(uc.FEEDBACK_LOG, "a") as f:
            f.write("REJ\t" + uc.qkey(question) + "\t" + answer + "\n")
        # WHATEVER FOLLOWS n IS THE CORRECTED ANSWER -- plain text, no syntax.
        corrected = fb[1:].strip(" :,-")
        if corrected:
            held = uc.record_correction(question, corrected)
            return "held, permanently. Ask me again and I will say: " + held
        return "withheld. Reply `n <the correct answer>` and I will hold it exactly."
    return None

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"UnisonAI is live as {client.user}", flush=True)

@client.event
async def on_message(msg):
    if msg.author.bot:
        return
    # feedback inside a thinking thread
    if isinstance(msg.channel, discord.Thread) and msg.channel.id in PENDING:
        uid, q, a = PENDING[msg.channel.id]
        res = apply_feedback(q, a, msg.content)
        if res:
            await msg.channel.send("⌁ " + res)
        return
    if isinstance(msg.channel, discord.Thread):
        return
    line = msg.content.strip()
    if not line:
        return
    ans, thought = await asyncio.to_thread(turn, line)
    # answer clean in the channel
    await msg.reply(ans[:1900], mention_author=False)
    # thinking thread on the user's message: CoT + feedback closure
    try:
        th = await msg.create_thread(name="⌁ thinking", auto_archive_duration=60)
        PENDING[th.id] = (msg.author.id, line, ans)
        await th.send(f"⌁ {thought[:1800]}\n\nreply `y` or `n <why / say \"the right answer\">` -- this thread folds away in 2 minutes.")
        async def fold_away(t=th):
            await asyncio.sleep(120)
            PENDING.pop(t.id, None)
            try:
                await t.delete()
            except Exception:
                pass
        asyncio.create_task(fold_away())
    except Exception as e:
        print("thread error:", e, flush=True)

client.run(TOKEN)
