import json
import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

logging.basicConfig(level=logging.INFO)

DATA_FILE = "players.json"

def load_players():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_players(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

def score_player(rank, iq, tactical, speed, confidence):
    return (rank * 0.35) + (iq * 0.20) + (tactical * 0.20) + (speed * 0.15) + (confidence * 0.10)

def parse_players(text):
    players = load_players()
    lines = text.strip().split("\n")

    for line in lines:
        parts = [x.strip() for x in line.split(",")]

        name = parts[0]
        rank = float(parts[1])
        iq = float(parts[2])
        tac = float(parts[3])
        speed = float(parts[4])
        conf = float(parts[5])
        pos = parts[6] if len(parts) > 6 else "Unknown"

        score = score_player(rank, iq, tac, speed, conf)

        players[name] = {
            "rank": rank,
            "iq": iq,
            "tactical": tac,
            "speed": speed,
            "confidence": conf,
            "position": pos,
            "score": score,
        }

    save_players(players)
    return players

def make_teams(players):
    sorted_players = sorted(players.items(), key=lambda x: x[1]["score"], reverse=True)

    teamA, teamB, teamC = [], [], []

    for index, item in enumerate(sorted_players):
        if index % 3 == 0:
            teamA.append(item)
        elif index % 3 == 1:
            teamB.append(item)
        else:
            teamC.append(item)

    return teamA, teamB, teamC

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⚽ Send players using this format:\n\n"
        "`Name, Rank, IQ, Tactical, Speed, Confidence, Position`\n\n"
        "Example:\n"
        "`Ali, 8, 7, 6, 8, 9, Forward`\n"
        "`Reza, 9, 6, 6, 7, 7, Defender`\n"
        "`Sam, 7, 9, 8, 6, 8, Midfield`\n\n"
        "Then send: /decide"
    )

async def decide(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.replace("/decide", "").strip()
    players = parse_players(text)

    teamA, teamB, teamC = make_teams(players)

    def fmt(team, name):
        s = f"🔥 {name}:\n"
        for p, info in team:
            s += f"- {p} ({info['score']:.2f}) [{info['position']}]\n"
        return s + "\n"

    reply = (
        "🏆 **INDOOR SOCCER TEAMS (3 × 6)** 🏆\n\n"
        + fmt(teamA, "Team A")
        + fmt(teamB, "Team B")
        + fmt(teamC, "Team C")
    )

    await update.message.reply_text(reply)

async def leaderboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    players = load_players()
    sorted_players = sorted(players.items(), key=lambda x: x[1]["score"], reverse=True)

    msg = "🏅 **PLAYER LEADERBOARD** 🏅\n\n"
    for name, info in sorted_players:
        msg += f"{name}: {info['score']:.2f}\n"

    await update.message.reply_text(msg)

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    players = load_players()
    msg = "📊 **PLAYER STATS** 📊\n\n"

    for name, info in players.items():
        msg += (
            f"{name}:\n"
            f"  Rank: {info['rank']}\n"
            f"  IQ: {info['iq']}\n"
            f"  Tactical: {info['tactical']}\n"
            f"  Speed: {info['speed']}\n"
            f"  Confidence: {info['confidence']}\n"
            f"  Position: {info['position']}\n"
            f"  Score: {info['score']:.2f}\n\n"
        )

    await update.message.reply_text(msg)

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if os.path.exists(DATA_FILE):
        os.remove(DATA_FILE)
    await update.message.reply_text("🔄 All player data has been reset.")

async def main():
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("decide", decide))
    app.add_handler(CommandHandler("leaderboard", leaderboard))
    app.add_handler(CommandHandler("stats", stats))
    app.add_handler(CommandHandler("reset", reset))

    print("Bot is running...")
    await app.run_polling()

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
