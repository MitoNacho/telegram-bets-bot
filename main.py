from telegram import (
    Update,
    ReplyKeyboardMarkup,
    
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
)
import os
import sqlite3
import logging


# =========================
# LOGS
# =========================

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# =========================
# CONFIG
# =========================

TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# =========================
# BASE DE DATOS
# =========================

conn = sqlite3.connect("/data/bets.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS bets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    apuesta TEXT,
    cuota REAL,
    resultado TEXT DEFAULT 'pendiente',
    visible INTEGER DEFAULT 1
)
""")

conn.commit()

# =========================
# COMANDO /start
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    keyboard = [

        ["📋 Bets", "📈 Estadísticas"],

        ["📜 Historial"]

    ]

    reply_markup = ReplyKeyboardMarkup(
        keyboard,
        resize_keyboard=True
    )

    await update.message.reply_photo(
    photo="https://github.com/MitoNacho/telegram-bets-bot/blob/28a1f528f5a93037ec0098f0e3d1958cd8efe470/banner.jpeg",

    caption=(
        "📊 Bot de Bebeto activo\n\n"
        "🔥 Picks diarios\n"
        "⚽ FUTBOL\n"
        "🥊 UFC\n"
        "📈 Estadísticas reales\n"
        "⚡ Combinadas premium"
    ),

    reply_markup=reply_markup
)

# =========================
# MENU FIJO
# =========================

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    if text == "📋 Bets":

        await bets(update, context)

    elif text == "📈 Estadísticas":

        await estadisticas(update, context)

    elif text == "📜 Historial":

        await historial(update, context)

# =========================
# BOTONES
# =========================

async def botones(update: Update, context: ContextTypes.DEFAULT_TYPE):

    query = update.callback_query

    await query.answer()

    if query.data == "bets":

        await bets(update, context)

    elif query.data == "historial":

        await historial(update, context)

    elif query.data == "stats":

        await estadisticas(update, context)

# =========================
# COMANDO /apuesta
# =========================

async def apuesta(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    texto = " ".join(context.args)

    if "@" not in texto:

        await update.message.reply_text(
            "Formato:\n"
            "/apuesta Madrid gana @1.80 + Over 2.5 @1.70"
        )

        return

    partes = texto.split("+")

    apuestas = []

    cuota_total = 1

    try:

        for parte in partes:

            parte = parte.strip()

            apuesta_texto, cuota = parte.rsplit("@", 1)

            apuesta_texto = apuesta_texto.strip()

            cuota = float(cuota.strip())

            apuestas.append(
                f"📌 {apuesta_texto} ({cuota})"
            )

            cuota_total *= cuota

    except:

        await update.message.reply_text(
            "❌ Formato incorrecto"
        )

        return

    cuota_total = round(cuota_total, 2)

    apuesta_final = "\n".join(apuestas)

    cursor.execute(
        "INSERT INTO bets (apuesta, cuota) VALUES (?, ?)",
        (apuesta_final, cuota_total)
    )

    conn.commit()

    bet_id = cursor.lastrowid

    await update.message.reply_text(
        f"✅ Apuesta #{bet_id} guardada\n\n"
        f"{apuesta_final}\n\n"
        f"💰 Cuota: {cuota_total}"
    )

# =========================
# COMANDO /resultado
# =========================

async def resultado(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    if len(context.args) != 2:
        await update.message.reply_text(
            "Formato:\n"
            "/resultado 1 win"
        )
        return

    bet_id = context.args[0]
    result = context.args[1].lower()

    if result not in ["win", "lose"]:
        await update.message.reply_text(
            "Resultado debe ser: win o lose"
        )
        return

    cursor.execute(
        "UPDATE bets SET resultado = ? WHERE id = ?",
        (result, bet_id)
    )

    conn.commit()

    await update.message.reply_text(
        f"✅ Resultado de apuesta #{bet_id} actualizado a {result}"
    )

# =========================
# COMANDO /estadisticas
# =========================

async def estadisticas(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message = update.message or update.callback_query.message
    cursor.execute("SELECT COUNT(*) FROM bets")
    total = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM bets WHERE resultado = 'win'"
    )
    wins = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM bets WHERE resultado = 'lose'"
    )
    loses = cursor.fetchone()[0]

    winrate = 0

    if (wins + loses) > 0:
        winrate = round((wins / (wins + loses)) * 100, 2)

    mensaje = (
        "📊 Estadísticas\n\n"
        f"📌 Total apuestas: {total}\n"
        f"✅ Aciertos: {wins}\n"
        f"❌ Fallos: {loses}\n"
        f"📈 Winrate: {winrate}%"
    )

    await message.reply_text(mensaje)

# =========================
# COMANDO /bets
# =========================

async def bets(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message = update.message or update.callback_query.message
    cursor.execute("""
        SELECT id, apuesta, cuota, resultado
        FROM bets
        WHERE resultado = 'pendiente'
        ORDER BY id DESC
        LIMIT 10
    """)

    apuestas = cursor.fetchall()

    if not apuestas:
        await message.reply_text(
            "❌ No hay apuestas registradas"
        )
        return

    mensaje = "📋 Últimas apuestas\n\n"

    for bet in apuestas:

        bet_id = bet[0]
        apuesta_texto = bet[1]
        cuota = bet[2]
        resultado = bet[3]

        emoji = "⏳"

        if resultado == "win":
            emoji = "✅"

        elif resultado == "lose":
            emoji = "❌"

        mensaje += (
            f"{emoji} #{bet_id}\n"
            f" {apuesta_texto}\n"
            f"💰 Cuota: {cuota}\n"
            f"📊 Resultado: {resultado}\n\n"
        )

    await message.reply_text(mensaje)

# =========================
# COMANDO /reset
# =========================

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):

    if update.effective_user.id != ADMIN_ID:
        return

    cursor.execute("DELETE FROM bets")
    cursor.execute("DELETE FROM sqlite_sequence WHERE name='bets'")

    conn.commit()

    await update.message.reply_text(
        "🗑️ Todas las apuestas fueron eliminadas"
    )

# =========================
# COMANDO /stats (historial)
# =========================

async def historial(update: Update, context: ContextTypes.DEFAULT_TYPE):

    message = update.message or update.callback_query.message
    cursor.execute("""
        SELECT id, apuesta, cuota, resultado
        FROM bets
        WHERE resultado != 'pendiente'
        ORDER BY id DESC
        LIMIT 10
    """)

    apuestas = cursor.fetchall()

    if not apuestas:

        await message.reply_text(
            "No hay apuestas finalizadas"
        )

        return

    mensaje = "📜 Historial\n\n"

    for bet in apuestas:

        emoji = "✅" if bet[3] == "win" else "❌"

        mensaje += (
            f"{emoji} #{bet[0]}\n"
            f"📌 {bet[1]}\n"
            f"💰 {bet[2]}\n\n"
        )

    await message.reply_text(mensaje)

# =========================
# MAIN
# =========================

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("apuesta", apuesta))
app.add_handler(CommandHandler("resultado", resultado))
app.add_handler(CommandHandler("estadisticas", estadisticas))
app.add_handler(CommandHandler("bets", bets))
app.add_handler(CommandHandler("reset", reset))
app.add_handler(CommandHandler("recientes", historial))
app.add_handler(CallbackQueryHandler(botones))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,menu_handler))
print("Bot iniciado...")

app.run_polling()





































