import json
from datetime import datetime
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
from dotenv import load_dotenv
import os

# ----------------- Load BOT Token from .env -----------------
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

# ----------------- Globals -----------------
TASK_FILE = "tasks.json"
tasks = {}  # {user_id: [task_dicts]}
task_counter = 1
user_points = {}  # Gamification points

# ----------------- Custom Font -----------------
def to_custom_font(text):
    mapping = {
        "A":"ᴧ","B":"ʙ","C":"ᴄ","D":"ᴅ","E":"ᴇ","F":"ꜰ","G":"ɢ","H":"ʜ",
        "I":"ɪ","J":"ᴊ","K":"ᴋ","L":"ʟ","M":"ᴍ","N":"η","O":"ᴏ","P":"ᴘ",
        "Q":"ǫ","R":"ʀ","S":"ꜱ","T":"ᴛ","U":"ᴜ","V":"ᴠ","W":"ᴡ","X":"x",
        "Y":"ʏ","Z":"ᴢ",
        "a":"ᴀ","b":"ʙ","c":"ᴄ","d":"ᴅ","e":"ᴇ","f":"ꜰ","g":"ɢ","h":"ʜ",
        "i":"ɪ","j":"ᴊ","k":"ᴋ","l":"ʟ","m":"ᴍ","n":"η","o":"ᴏ","p":"ᴘ",
        "q":"ǫ","r":"ʀ","s":"ꜱ","t":"ᴛ","u":"ᴜ","v":"ᴠ","w":"ᴡ","x":"x",
        "y":"ʏ","z":"ᴢ",
    }
    return ''.join(mapping.get(c, c) for c in text)

# ----------------- Load/Save Tasks -----------------
def load_tasks():
    global tasks, task_counter
    try:
        with open(TASK_FILE, "r") as f:
            data = json.load(f)
            if isinstance(data, dict):
                tasks.update({int(k): v for k, v in data.items()})
            else:
                tasks.clear()
            all_ids = []
            for u, tlist in tasks.items():
                for t in tlist:
                    if "id" not in t:
                        t["id"] = max(all_ids)+1 if all_ids else 1
                    for field in ["subject","lesson","title","deadline","completed"]:
                        if field not in t:
                            t[field] = "N/A" if field!="completed" else False
                    all_ids.append(t["id"])
            task_counter = max(all_ids)+1 if all_ids else 1
    except:
        tasks.clear()

def save_tasks():
    with open(TASK_FILE,"w") as f:
        json.dump(tasks,f)

# ----------------- Progress Bar -----------------
def progress_bar(user_id):
    user_tasks = tasks.get(user_id,[])
    if not user_tasks: return "No tasks!"
    completed = sum(1 for t in user_tasks if t.get("completed"))
    total = len(user_tasks)
    percent = int((completed/total)*100)
    blocks = int(percent/10)
    bar = "█"*blocks + "░"*(10-blocks)
    return f"[{bar}] {percent}% ({completed}/{total})"

# ----------------- /start -----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    username = update.effective_user.first_name
    if user_id not in tasks: tasks[user_id]=[]
    welcome = f"""
{to_custom_font('👋 Hello')} {to_custom_font(username)}!
{to_custom_font('Welcome to the Student Task Bot 🎓')}
{to_custom_font('Use buttons below to navigate and manage your study tasks efficiently')}
"""
    keyboard = [
        [InlineKeyboardButton(to_custom_font("How to Use Me"), callback_data="how_to_use")],
        [InlineKeyboardButton(to_custom_font("Student Mode"), callback_data="student_mode")],
        [
            InlineKeyboardButton(to_custom_font("Owner"), url="https://t.me/YourOwnerUsername"),
            InlineKeyboardButton(to_custom_font("Support"), url="https://t.me/YourSupportUsername")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_photo(photo="https://files.catbox.moe/dgelfj.jpg", caption=welcome, reply_markup=reply_markup)

# ----------------- /help -----------------
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton(to_custom_font("Student Mode"), callback_data="student_mode")],
        [InlineKeyboardButton(to_custom_font("Back to Home"), callback_data="back_home")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    msg = f"""
{to_custom_font('👋 Hello')} {to_custom_font(update.effective_user.first_name)}!
{to_custom_font('Press Student Mode to:')}
1️⃣ Add new tasks (Subject → Lesson → Title → Deadline)
2️⃣ View your tasks
3️⃣ Check progress and points
"""
    await update.message.reply_text(msg, reply_markup=reply_markup)

# ----------------- Home Page -----------------
async def home_page(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.callback_query.from_user.id
    username = update.callback_query.from_user.first_name
    if user_id not in tasks: tasks[user_id]=[]
    welcome = f"""
{to_custom_font('👋 Hello')} {to_custom_font(username)}!
{to_custom_font('Welcome to the Student Task Bot 🎓')}
"""
    keyboard = [
        [InlineKeyboardButton(to_custom_font("How to Use Me"), callback_data="how_to_use")],
        [InlineKeyboardButton(to_custom_font("Student Mode"), callback_data="student_mode")],
        [
            InlineKeyboardButton(to_custom_font("Owner"), url="https://t.me/YourOwnerUsername"),
            InlineKeyboardButton(to_custom_font("Support"), url="https://t.me/YourSupportUsername")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.callback_query.message.reply_photo(photo="https://files.catbox.moe/dgelfj.jpg", caption=welcome, reply_markup=reply_markup)

# ----------------- Button Handler -----------------
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global task_counter
    query = update.callback_query
    user_id = query.from_user.id
    await query.answer()
    data = query.data

    # How to Use
    if data=="how_to_use":
        keyboard = [
            [InlineKeyboardButton(to_custom_font("Student Mode"), callback_data="student_mode")],
            [InlineKeyboardButton(to_custom_font("Back to Home"), callback_data="back_home")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        msg = f"""
{to_custom_font('👋 Hello')} {to_custom_font(query.from_user.first_name)}!
{to_custom_font('Press Student Mode to manage tasks')}
"""
        await query.message.reply_text(msg, reply_markup=reply_markup)

    # Student Mode
    elif data=="student_mode":
        keyboard = [
            [InlineKeyboardButton(to_custom_font("Add Task"), callback_data="add_task")],
            [InlineKeyboardButton(to_custom_font("View Tasks"), callback_data="view_tasks")],
            [InlineKeyboardButton(to_custom_font("Progress / Stats"), callback_data="progress")],
            [InlineKeyboardButton(to_custom_font("Back to Home"), callback_data="back_home")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        msg = f"{to_custom_font('Student Mode Menu: Choose an option')}"
        await query.message.reply_text(msg, reply_markup=reply_markup)

    # Back Home
    elif data=="back_home":
        await home_page(update, context)

    # Add Task Flow
    elif data=="add_task":
        await query.message.reply_text(to_custom_font("Enter Subject/Topic:"))
        context.user_data["adding_task_step"]="subject"

    # View Tasks
    elif data=="view_tasks":
        user_tasks = tasks.get(user_id, [])
        if not user_tasks:
            await query.message.reply_text(to_custom_font("No tasks found!"))
            return
        for t in user_tasks:
            status = "✅" if t.get("completed") else "❌"
            keyboard = [[
                InlineKeyboardButton(to_custom_font("Done"), callback_data=f"done_{t['id']}"),
                InlineKeyboardButton(to_custom_font("Edit"), callback_data=f"edit_{t['id']}"),
                InlineKeyboardButton(to_custom_font("Delete"), callback_data=f"delete_{t['id']}")
            ]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            deadline_text = f" (Due: {t.get('deadline','N/A')})"
            await query.message.reply_text(
                f"{status} {to_custom_font(t.get('title'))} - {to_custom_font(t.get('subject'))} / {to_custom_font(t.get('lesson'))}{deadline_text}",
                reply_markup=reply_markup
            )

    # Done / Delete / Edit / Delete All
    elif data=="delete_all":
        tasks[user_id]=[]
        save_tasks()
        user_points[user_id]=0
        await query.message.reply_text(to_custom_font("✅ All tasks cleared, points reset!"))
    elif data.startswith("done_"):
        tid = int(data.split("_")[1])
        for t in tasks[user_id]:
            if t["id"]==tid:
                t["completed"]=True
                save_tasks()
                user_points[user_id] = user_points.get(user_id,0)+1
                await query.message.reply_text(to_custom_font(f"Task '{t['title']}' completed! ✅ Points: {user_points[user_id]}"))
                break
    elif data.startswith("delete_"):
        tid = int(data.split("_")[1])
        tasks[user_id] = [t for t in tasks[user_id] if t["id"]!=tid]
        save_tasks()
        await query.message.reply_text(to_custom_font("Task deleted 🗑️"))
    elif data.startswith("edit_"):
        tid = int(data.split("_")[1])
        context.user_data["edit_task_id"]=tid
        await query.message.reply_text(to_custom_font("Send new Title:"))
        context.user_data["adding_task_step"]="edit_title"

    # Progress / Stats
    elif data=="progress":
        user_tasks=tasks.get(user_id,[])
        if not user_tasks:
            await query.message.reply_text(to_custom_font("No tasks!"))
            return
        completed = sum(1 for t in user_tasks if t.get("completed"))
        total = len(user_tasks)
        percent = int((completed/total)*100)
        bar = "█"*int(percent/10)+"░"*(10-int(percent/10))
        msg=f"""
{to_custom_font('Progress Bar:')} [{bar}] {percent}% ({completed}/{total})
{to_custom_font(f'Points: {user_points.get(user_id,0)}')}
"""
        keyboard=[[InlineKeyboardButton(to_custom_font("Delete All Tasks"),callback_data="delete_all")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(msg, reply_markup=reply_markup)

# ----------------- Multi-step Add / Edit -----------------
async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global task_counter
    user_id = update.effective_user.id
    step = context.user_data.get("adding_task_step")
    if step=="subject":
        context.user_data["subject"]=update.message.text
        context.user_data["adding_task_step"]="lesson"
        await update.message.reply_text(to_custom_font("Enter Lesson Name:"))
    elif step=="lesson":
        context.user_data["lesson"]=update.message.text
        context.user_data["adding_task_step"]="title"
        await update.message.reply_text(to_custom_font("Enter Task Title:"))
    elif step=="title":
        context.user_data["title"]=update.message.text
        context.user_data["adding_task_step"]="deadline"
        await update.message.reply_text(to_custom_font("Enter Deadline (YYYY-MM-DD) or type 'None':"))
    elif step=="deadline":
        dl=update.message.text
        try:
            if dl.lower()!="none":
                datetime.strptime(dl,"%Y-%m-%d")
        except ValueError:
            dl="N/A"
        new_task={"id":task_counter,
                  "title":context.user_data["title"],
                  "subject":context.user_data["subject"],
                  "lesson":context.user_data["lesson"],
                  "deadline":dl,
                  "completed":False}
        tasks[user_id].append(new_task)
        task_counter+=1
        save_tasks()
        context.user_data["adding_task_step"]=None
        keyboard=[
            [InlineKeyboardButton(to_custom_font("Add More Tasks"),callback_data="add_task")],
            [InlineKeyboardButton(to_custom_font("Back to Student Mode"),callback_data="student_mode")]
        ]
        reply_markup=InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(to_custom_font(f"Task '{new_task['title']}' added ✅"),reply_markup=reply_markup)
    elif step=="edit_title":
        tid=context.user_data.get("edit_task_id")
        for t in tasks[user_id]:
            if t["id"]==tid:
                t["title"]=update.message.text
                save_tasks()
                await update.message.reply_text(to_custom_font("Task title updated ✅"))
        context.user_data["adding_task_step"]=None

# ----------------- Main -----------------
def main():
    load_tasks()
    app=ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start",start))
    app.add_handler(CommandHandler("help",help_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND,message_handler))
    print("Bot is running...")
    app.run_polling()

if __name__=="__main__":
    main()
