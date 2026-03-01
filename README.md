
# Student Task Bot

A fully-featured **Telegram bot for students** to manage study tasks, track progress, and gamify learning.

---

## **Features**

- ✅ **Add Tasks**: Multi-step flow to add a task with:
  - Subject / Topic
  - Lesson Name
  - Task Title
  - Deadline (YYYY-MM-DD)  
- ✅ **View Tasks**: See all your tasks with **✅ completed** or **❌ pending** indicators.  
- ✅ **Edit / Delete Tasks**: Edit task title or delete individual tasks.  
- ✅ **Progress Bar**: Shows your completed tasks percentage and points earned.  
- ✅ **Delete All Tasks**: Reset all tasks and points in one click.  
- ✅ **Custom Font**: All messages in a stylized readable font.  
- ✅ **Inline Navigation Buttons**: Home, Student Mode, How to Use, Support, Owner.  
- ✅ **Gamification**: Earn points for completed tasks.

---

## **Setup & Installation**

### 1️⃣ Clone the repository
```bash
git clone <repo_url>
cd StudentTaskBot
2️⃣ Install Python & Dependencies
Requires Python 3.10+
Bash
Copy code
pip install -r requirements.txt
3️⃣ Add your Telegram Bot Token
You have two options:
Option 1: Using .env file (Recommended)
Create a file named .env in the project root:
Text
Copy code
BOT_TOKEN=123456789:ABCdefGHIjklMNOpqRS_TUVwxyz
In TaskBot.py, the bot will automatically load the token using dotenv.
Option 2: Directly in TaskBot.py
Replace the token line:
Python
Copy code
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
Remove from dotenv import load_dotenv and load_dotenv() if using direct token.
⚠️ Important: Never push your token to a public repository.
4️⃣ Running on VPS
Upload the repo to your VPS (using scp or GitHub clone).
Make sure Python 3.10+ is installed.
Install dependencies:
Bash
Copy code
pip install -r requirements.txt
Run the bot:
Bash
Copy code
python TaskBot.py
Keep the bot running:
Use screen or tmux:
Bash
Copy code
screen -S StudentBot
python TaskBot.py
# Press Ctrl+A then D to detach
Or use systemd service for auto-start on reboot.
Bot Usage
Start the Bot
/start → Displays welcome message + buttons:
How to Use Me
Student Mode
Owner (link)
Support (link)
How to Use Me
Explains bot features.
Button to go to Student Mode.
Student Mode
Add Task → Step by step: Subject → Lesson → Title → Deadline.
View Tasks → See all tasks with ✅/❌, Edit or Delete buttons.
Progress / Stats → Shows a visual progress bar, completed tasks, and points.
Back to Student Mode/Home → Navigate easily.
Gamification
Each completed task adds 1 point.
Progress bar shows percentage completed visually: [█████░░░░░] 50%.
Delete All Tasks
Clears all tasks and points with one click.
Folder Structure
Copy code

StudentTaskBot/
│
├─ TaskBot.py         # Main bot code
├─ tasks.json         # User task data (auto-generated)
├─ .env               # Secret bot token (optional)
├─ .gitignore         # Ignore secrets and cache
├─ requirements.txt   # Dependencies
└─ README.md          # This documentation
Notes & Tips
Keep tasks.json private if deploying publicly.
Use a VPS for 24/7 uptime.
Customize Owner / Support URLs in the inline buttons.
Custom Font can be modified in to_custom_font() function.
Enjoy managing your study tasks efficiently! 🎓
