#!/bin/bash

# Define the README content
readme_content="# 📌 Reminder App  

A **GUI-based Reminder App** built using **Python (Tkinter)** that allows users to set and manage reminders with an intuitive interface.  

## 📜 Features  
- ✅ **Add, view, and remove reminders**  
- 📅 **Select date and time** for each reminder  
- 🔔 **Custom notification mediums**, including **WhatsApp, Email, Text, Alarm, and more**  
- 🛠 **Easy-to-use graphical interface**  
- 💾 **Reminders saved locally** using JSON  

## 🏗 Technologies Used  
- **Programming Language:** Python  
- **GUI Library:** Tkinter  
- **Storage:** JSON file for saving reminders  
- **Other Libraries:** \`datetime\`, \`json\`, \`ttk\` (for dropdowns)  

## 🚀 Installation & Setup  

1. **Clone the repository**  
   \`\`\`bash
   git clone https://github.com/your-username/Reminder-App.git
   cd Reminder-App
   \`\`\`

2. **Run the app**  
   \`\`\`bash
   python reminder_app.py
   \`\`\`

## 📷 Screenshots (Optional)  
_Add screenshots of your app's interface here._  

## 🛠 How It Works  
1. **Adding a Reminder:**  
   - Enter a **title**  
   - Select **date & time**  
   - Choose a **reminder medium** (WhatsApp, Email, Alarm, etc.)  
   - Click **\"Add Reminder\"**  

2. **Viewing Reminders:**  
   - Click **\"Display Reminders\"** to see all saved reminders  

3. **Removing a Reminder:**  
   - Click **\"Remove Reminder\"**, select a reminder, and delete it  

## 🤝 Contributing  
Feel free to fork this repository and submit a pull request with improvements.  

## 📜 License  
This project is licensed under the **MIT License**.  
"

# Write to README.md
echo "$readme_content" > README.md

# Ensure we're in a Git repository
if [ ! -d ".git" ]; then
    echo "❌ Error: Not inside a Git repository. Initializing Git..."
    git init
    git remote add origin git@github.com:your-username/Reminder-App.git
fi

# Stage the file
git add README.md

# Commit the changes if there are any
if git diff --cached --quiet; then
    echo "✅ No changes to commit."
else
    git commit -m "Update README.md with new content"
    git push origin main
    echo "✅ README.md file has been updated and pushed successfully!"
fi
