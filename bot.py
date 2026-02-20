"""
Kedai Heula – Telegram Mini App Bot
Bot ini membuka web app Kalkulator HPP langsung dari Telegram.
Data tersimpan di browser user (localStorage), tidak perlu database.
"""

import logging
from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    WebAppInfo,
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)

# ─── KONFIGURASI — isi dua baris ini ────────────────────────────────────────
import os
BOT_TOKEN = "8243503971:AAGzGIjjBaW2CIZKQD9BrwnLXnRdpWS26tE"
APP_URL   = "https://0xDuraku.github.io/kedai-heula-bot/kedai-heula-hpp.html"
# ────────────────────────────────────────────────────────────────────────────

logging.basicConfig(
    format="%(asctime)s | %(levelname)s | %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


# ── Keyboard helpers ─────────────────────────────────────────────────────────

def kb_main():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🍱  Buka Kalkulator HPP", web_app=WebAppInfo(url=APP_URL))],
        [
            InlineKeyboardButton("📖 Cara Pakai", callback_data="help"),
            InlineKeyboardButton("ℹ️ Tentang",    callback_data="about"),
        ],
        [InlineKeyboardButton("📌 Semua Fitur",   callback_data="fitur")],
    ])


def kb_fitur():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🧮 Hitung HPP",       web_app=WebAppInfo(url=APP_URL))],
        [InlineKeyboardButton("📋 Ringkasan Menu",   web_app=WebAppInfo(url=APP_URL))],
        [InlineKeyboardButton("🏷️ Kalkulator Promo", web_app=WebAppInfo(url=APP_URL))],
        [InlineKeyboardButton("📖 Panduan",          web_app=WebAppInfo(url=APP_URL))],
        [InlineKeyboardButton("← Kembali",           callback_data="back_main")],
    ])


def kb_back():
    return InlineKeyboardMarkup([[
        InlineKeyboardButton("← Kembali", callback_data="back_main")
    ]])


# ── /start ───────────────────────────────────────────────────────────────────

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    nama = update.effective_user.first_name or "Sobat"
    await update.message.reply_text(
        f"🍱 Halo, *{nama}\\!* Selamat datang di *Kedai Heula HPP Calculator*\\.\n\n"
        "Tools lengkap buat ngitung *Harga Pokok Produksi* dan simulasi promo "
        "untuk menu Takoyaki, Dimsum, dan Ayam Crispy kamu\\.\n\n"
        "🧮 *Hitung HPP* — isi bahan \\+ biaya, hasil langsung keluar\n"
        "📋 *Ringkasan Menu* — lihat semua menu yang sudah tersimpan\n"
        "🏷️ *Kalkulator Promo* — simulasi diskon, bundling, beli X gratis Y\n"
        "📄 *Export PDF* — cetak referensi bahan baku\n\n"
        "Tap tombol di bawah untuk mulai\\! 👇",
        parse_mode="MarkdownV2",
        reply_markup=kb_main(),
    )


# ── /menu ────────────────────────────────────────────────────────────────────

async def menu_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "🍱 *Pilih fitur yang mau dibuka:*",
        parse_mode="MarkdownV2",
        reply_markup=kb_fitur(),
    )


# ── /help ────────────────────────────────────────────────────────────────────

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "📖 *Cara Pakai Kalkulator HPP*\n\n"
        "*1\\. Hitung HPP*\n"
        "Isi nama menu → tambah bahan \\(nama, qty, harga beli, ukuran beli\\) "
        "→ tambah biaya operasional → klik *Hitung HPP*\\. "
        "Saran harga jual 3 tier langsung muncul\\.\n\n"
        "*2\\. Simpan ke Ringkasan*\n"
        "Klik *Simpan ke Ringkasan Menu* setelah hitung HPP\\. "
        "Data disimpan di browser dan bisa dilihat kapan saja\\.\n\n"
        "*3\\. Simulasi Promo*\n"
        "Pilih menu dari ringkasan → pilih tipe promo → lihat "
        "apakah promo masih untung atau boncos\\.\n\n"
        "*4\\. Export PDF*\n"
        "Ringkasan Menu → Detail Bahan → Export PDF → Save as PDF\\.\n\n"
        "💡 Data tersimpan di browser\\. Pakai browser yang sama "
        "supaya data tidak hilang\\.",
        parse_mode="MarkdownV2",
        reply_markup=kb_back(),
    )


# ── Callback query handler ────────────────────────────────────────────────────

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == "help":
        await query.edit_message_text(
            "📖 *Cara Pakai Kalkulator HPP*\n\n"
            "*1\\. Hitung HPP*\n"
            "Isi nama menu → tambah bahan \\(nama, qty, harga beli, ukuran beli\\) "
            "→ tambah biaya operasional → klik *Hitung HPP*\\. "
            "Saran harga jual 3 tier langsung muncul\\.\n\n"
            "*2\\. Simpan ke Ringkasan*\n"
            "Klik *Simpan ke Ringkasan Menu* setelah hitung HPP\\. "
            "Data disimpan di browser dan bisa dilihat kapan saja\\.\n\n"
            "*3\\. Simulasi Promo*\n"
            "Pilih menu dari ringkasan → pilih tipe promo → lihat "
            "apakah promo masih untung atau boncos\\.\n\n"
            "*4\\. Export PDF*\n"
            "Ringkasan Menu → Detail Bahan → Export PDF → Save as PDF\\.\n\n"
            "💡 Data tersimpan di browser\\. Pakai browser yang sama "
            "supaya data tidak hilang\\.",
            parse_mode="MarkdownV2",
            reply_markup=kb_back(),
        )

    elif query.data == "about":
        await query.edit_message_text(
            "ℹ️ *Kedai Heula HPP Calculator*\n\n"
            "Tools bantu bisnis untuk:\n"
            "• Hitung Harga Pokok Produksi \\(HPP\\)\n"
            "• Tentukan harga jual yang tepat\n"
            "• Simulasi berbagai jenis promo\n"
            "• Cetak referensi bahan baku ke PDF\n\n"
            "🏪 *Kedai Heula* — Takoyaki, Dimsum, Ayam Crispy\n"
            "📍 Semarang, Jawa Tengah\n\n"
            "🔒 Data disimpan lokal di browser, tidak dikirim ke server manapun\\.",
            parse_mode="MarkdownV2",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🍱 Buka App", web_app=WebAppInfo(url=APP_URL))],
                [InlineKeyboardButton("← Kembali",   callback_data="back_main")],
            ]),
        )

    elif query.data == "fitur":
        await query.edit_message_text(
            "🍱 *Pilih fitur yang mau dibuka:*",
            parse_mode="MarkdownV2",
            reply_markup=kb_fitur(),
        )

    elif query.data == "back_main":
        await query.edit_message_text(
            "🍱 *Kedai Heula HPP Calculator*\n\nTap tombol di bawah untuk mulai\\! 👇",
            parse_mode="MarkdownV2",
            reply_markup=kb_main(),
        )


# ── Main ─────────────────────────────────────────────────────────────────────

import asyncio

async def main() -> None:
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu",  menu_cmd))
    app.add_handler(CommandHandler("help",  help_cmd))
    app.add_handler(CallbackQueryHandler(button))
    logger.info("Bot Kedai Heula berjalan. Ctrl+C untuk stop.")
    await app.initialize()
    await app.start()
    await app.updater.start_polling(allowed_updates=Update.ALL_TYPES)
    # Jalan terus sampai Ctrl+C
    await asyncio.Event().wait()


if __name__ == "__main__":
    asyncio.run(main())
