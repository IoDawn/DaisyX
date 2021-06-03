"""
MIT License
Copyright (c) 2021 TheHamkerCat
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import os

from pyrogram import filters

from DaisyX.function.pluginhelpers import member_permissions
from DaisyX.services.pyrogram import pbot as app


@app.on_message(filters.command("setgrouptitle") & ~filters.private)
async def set_chat_title(_, message):
    try:
        chat_id = message.chat.id
        user_id = message.from_user.id
        permissions = await member_permissions(chat_id, user_id)
        if "can_change_info" not in permissions:
            await message.reply_text("You Don't Have Enough Permissions.")
            return
        if len(message.command) < 2:
            await message.reply_text("**Usage:**\n/set_chat_title NEW NAME")
            return
        old_title = message.chat.title
        new_title = message.text.split(None, 1)[1]
        await message.chat.set_title(new_title)
        await message.reply_text(
            f"Successfully Changed Group Title From {old_title} To {new_title}"
        )
    except Exception as e:
        print(e)
        await message.reply_text(e)


@app.on_message(filters.command("settitle") & ~filters.private)
async def set_user_title(_, message):
    try:
        chat_id = message.chat.id
        user_id = message.from_user.id
        from_user = message.reply_to_message.from_user
        permissions = await member_permissions(chat_id, user_id)
        if "can_change_info" not in permissions:
            await message.reply_text("You Don't Have Enough Permissions.")
            return
        if len(message.command) < 2:
            await message.reply_text(
                "**Usage:**\n/set_user_title NEW ADMINISTRATOR TITLE"
            )
            return
        title = message.text.split(None, 1)[1]
        await app.set_administrator_title(chat_id, from_user.id, title)
        await message.reply_text(
            f"Successfully Changed {from_user.mention}'s Admin Title To {title}"
        )
    except Exception as e:
        print(e)
        await message.reply_text(e)


@app.on_message(filters.command("setgrouppic") & ~filters.private)
async def set_chat_photo(_, message):
    try:
        chat_id = message.chat.id
        user_id = message.from_user.id

        permissions = await member_permissions(chat_id, user_id)
        if "can_change_info" not in permissions:
            await message.reply_text("You Don't Have Enough Permissions.")
            return
        if not message.reply_to_message:
            await message.reply_text("Reply to a photo to set it as chat_photo")
            return
        if not message.reply_to_message.photo and not message.reply_to_message.document:
            await message.reply_text("Reply to a photo to set it as chat_photo")
            return
        photo = await message.reply_to_message.download()
        await message.chat.set_photo(photo)
        await message.reply_text("Successfully Changed Group Photo")
        os.remove(photo)
    except Exception as e:
        print(e)
        await message.reply_text(e)


__mod_name__ = "Admin"

__help__ = """
Permudah admin untuk mengelola pengguna dan grup dengan modul admin!

<b>Perintah yang tersedia:</b>

<b> Daftar admin </b>
- /adminlist: menunjukkan semua admin di obrolan grup.*
- /admincache: Perbarui cache admin, untuk memperhitungkan izin admin/admin baru.*

<b> Mute </b>
- /mute: bisukan pengguna
- /unmute: berhenti bisukan pengguna
- /tmute [entitas]: Untuk sementara memberi pengguna untuk interval waktu.
- /unmuteall: Tanpa Rendam semua anggota yang diredam/mute

<b> Bans & Kicks </b>
- /ban: melarang pengguna
- /tban [entitas]: Menjalankan sementara pengguna untuk interval waktu.
- /unban: lepas ban Pengguna
- /unbanall: Unban semua anggota yang dilarang
- /banme: ban diri anda(khusus yg tau diri)
- /kick: menendang pengguna
- /kickme: menendangmu

<b> Promot & Demote </ b>
- /promote (pengguna)(title): mempromosikan pengguna ke admin.*
- /demote (Pengguna): Demot pengguna dari admin.*
- /lowpromote: Promosikan anggota dengan Hak Rendah*
- /midpromote: Promosikan anggota dengan Hak menengah*
- /highpromote: Promosikan anggota dengan Hak Maksimum*
- /lowdemote: Demote admin ke izin rendah*
- /middemote: Demote admin ke pertengahan izin*

<b> Cleaner/Purge </b>
- /purge: Menghapus semua pesan dari pesan yang Anda jawab
- /del: menghapus pesan dengan cara dibalas/reply
- /zombies: Menghitung jumlah akun yang dihapus di grup Anda
- /kickthefools: Tendang anggota yang tidak aktif dari grup (satu minggu)

<b> info pengguna </b>
- /info: Dapatkan Info Pengguna
- /users: Dapatkan daftar pengguna grup
- /spwinfo: Periksa info spam pengguna dari Layanan SpamProteksi Inlotivoid
- /whois: Memberikan info Pengguna Seperti Pyrogram

<b> Lainnya </b>
- /invitelink: Dapatkan tautan undangan obrolan grup
- /settitle [entitas][title]: Tetapkan title khusus untuk admin. Jika tidak [titLe] akan menjadi default ke "admin"
- /setgrouptitle [teks] mengatur grup title
- /setgrouppic: Balas/reply ke gambar untuk ditetapkan sebagai foto grup
- /setdescription: set deskripsi grup
- /setsticker: atur stiker grup

*Catatan:
Saat Anda mempromosikan atau menurunkan admin secara manual, bot mungkin tidak segera menyadarinya. Ini karena untuk menghindari spamming server telegram, status admin di-cache secara lokal.
Ini berarti bahwa Anda kadang-kadang harus menunggu beberapa menit untuk hak admin untuk memperbarui. Jika Anda ingin segera memperbaruinya, Anda dapat menggunakan perintah /admincache; Itu akan memaksa bot untuk memeriksa siapa admin itu lagi.
"""
