import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from datetime import datetime
import json

class ReminderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Reminder App")
        self.root.geometry("700x700")

        # Buttons placed in a single row
        self.add_button = tk.Button(root, text="Add Reminder", command=self.show_add_fields)
        self.add_button.grid(row=0, column=0, padx=10, pady=10)

        self.display_button = tk.Button(root, text="Display Reminders", command=self.display_reminders)
        self.display_button.grid(row=0, column=1, padx=10, pady=10)

        self.remove_button = tk.Button(root, text="Remove Reminder", command=self.remove_reminder)
        self.remove_button.grid(row=0, column=2, padx=10, pady=10)

        # Initialize reminders list and load from file if exists
        self.reminders = self.load_reminders()

        # Initialize frames
        self.fields_frame = None
        self.display_frame = tk.Frame(root)
        self.display_frame.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

    def show_add_fields(self):
        # Hide remove reminder and display reminder sections if shown
        self.hide_remove_fields()
        self.hide_display_fields()

        # Show the fields to add a reminder
        if self.fields_frame:
            self.fields_frame.destroy()  # Remove previous fields if they exist
        self.fields_frame = tk.Frame(self.root)
        self.fields_frame.grid(row=1, column=0, columnspan=3, padx=10, pady=10)

        # Title label and input field
        self.Title = tk.Label(self.fields_frame, text="Reminder Title:")
        self.Title.grid(row=0, column=0, padx=5, pady=5)
        self.Title_entry = tk.Entry(self.fields_frame)
        self.Title_entry.grid(row=0, column=1, padx=5, pady=5)

        # Medium label and combobox for options
        self.Medium = tk.Label(self.fields_frame, text="Reminder Medium:")
        self.Medium.grid(row=1, column=0, padx=5, pady=5)

        # Medium Combobox with predefined options
        self.Medium_options = [
            "Whatsapp", "Email", "Text", "Post a Video",
            "Alarm", "Run Command on Shell", "Other"
        ]
        self.Medium_combobox = ttk.Combobox(self.fields_frame, values=self.Medium_options, width=20)
        self.Medium_combobox.set(self.Medium_options[0])  # Default value
        self.Medium_combobox.grid(row=1, column=1, padx=5, pady=5)

        # Custom Entry for Other option
        self.custom_medium_label = tk.Label(self.fields_frame, text="Please specify:")
        self.custom_medium_label.grid(row=2, column=0, padx=5, pady=5)
        self.custom_medium_entry = tk.Entry(self.fields_frame)
        self.custom_medium_entry.grid(row=2, column=1, padx=5, pady=5)
        self.custom_medium_label.grid_forget()  # Hide initially
        self.custom_medium_entry.grid_forget()  # Hide initially

        # Show custom input if "Other" is selected
        self.Medium_combobox.bind("<<ComboboxSelected>>", self.toggle_custom_medium)

        # Month Label and Picker
        self.month_label = tk.Label(self.fields_frame, text="Month:")
        self.month_label.grid(row=3, column=0, padx=5, pady=0)

        self.month_combobox = ttk.Combobox(self.fields_frame, values=[ 
            "January", "February", "March", "April", "May", "June", 
            "July", "August", "September", "October", "November", "December"
        ])  
        self.month_combobox.set("January")
        self.month_combobox.grid(row=4, column=0, padx=5, pady=0)

        # Year Label and Picker
        self.year_label = tk.Label(self.fields_frame, text="Year:")
        self.year_label.grid(row=3, column=1, padx=5, pady=0)

        current_year = datetime.now().year
        self.year_combobox = ttk.Combobox(self.fields_frame, values=[str(year) for year in range(current_year, current_year + 11)], width=8)
        self.year_combobox.set(str(current_year))
        self.year_combobox.grid(row=4, column=1, padx=5, pady=0)

        # Time Pickers (Hour, Minute, Second) aligned horizontally in the same row
        self.time_frame = tk.Frame(self.fields_frame)
        self.time_frame.grid(row=3, column=2, rowspan=2, padx=10, pady=0)

        # Hour Picker
        self.hour_label = tk.Label(self.time_frame, text="Hour:")
        self.hour_label.grid(row=0, column=0, padx=2, pady=0)

        self.hours = ttk.Combobox(self.time_frame, values=[f"{i:02}" for i in range(24)], width=5)
        self.hours.set("00")
        self.hours.grid(row=1, column=0, padx=2, pady=0)

        # Minute Picker
        self.minute_label = tk.Label(self.time_frame, text="Minute:")
        self.minute_label.grid(row=0, column=1, padx=2, pady=0)

        self.minutes = ttk.Combobox(self.time_frame, values=[f"{i:02}" for i in range(60)], width=5)
        self.minutes.set("00")
        self.minutes.grid(row=1, column=1, padx=2, pady=0)

        # Second Picker
        self.second_label = tk.Label(self.time_frame, text="Second:")
        self.second_label.grid(row=0, column=2, padx=2, pady=0)

        self.seconds = ttk.Combobox(self.time_frame, values=[f"{i:02}" for i in range(60)], width=5)
        self.seconds.set("00")
        self.seconds.grid(row=1, column=2, padx=2, pady=0)

        # Day Picker: 1 to 31
        self.day_label = tk.Label(self.fields_frame, text="Day:")
        self.day_label.grid(row=5, column=0, padx=5, pady=0)

        # Create day buttons (1 to 31)
        self.day_buttons_frame = tk.Frame(self.fields_frame)
        self.day_buttons_frame.grid(row=6, column=0, columnspan=3, pady=5)

        self.day_buttons = []
        for day in range(1, 32):
            day_button = tk.Button(self.day_buttons_frame, text=str(day), width=4, command=lambda day=day: self.select_day(day))
            self.day_buttons.append(day_button)
            day_button.grid(row=(day-1)//7, column=(day-1)%7, padx=2, pady=2)

        # Add Reminder Button
        self.add_reminder_button = tk.Button(self.fields_frame, text="Add Reminder", command=self.add_reminder)
        self.add_reminder_button.grid(row=7, column=1, padx=5, pady=5)

        # Close Reminder Button (Newly added just below the "Add Reminder" button)
        self.close_reminder_button = tk.Button(self.fields_frame, text="Close", command=self.close_fields)
        self.close_reminder_button.grid(row=8, column=1, padx=5, pady=5)

        self.selected_day = None  # Track selected day

    def select_day(self, day):
        self.selected_day = day
        print(f"Selected day: {self.selected_day}")  # You can replace this with your logic

    def toggle_custom_medium(self, event=None):
        # Show or hide the custom input field based on the selected option
        if self.Medium_combobox.get() == "Other":
            self.custom_medium_label.grid(row=2, column=0, padx=5, pady=5)
            self.custom_medium_entry.grid(row=2, column=1, padx=5, pady=5)
        else:
            self.custom_medium_label.grid_forget()
            self.custom_medium_entry.grid_forget()

    def add_reminder(self):
        title = self.Title_entry.get()
        medium = self.Medium_combobox.get()

        # If "Other" is selected, get custom input
        if medium == "Other":
            medium = self.custom_medium_entry.get()
            if not medium:
                messagebox.showerror("Error", "Please specify a custom reminder medium.")
                return

        month = self.month_combobox.get()
        year = self.year_combobox.get()
        day = self.selected_day
        hours = self.hours.get()
        minutes = self.minutes.get()
        seconds = self.seconds.get()

        if not title or not medium or not month or not year or not hours or not minutes or not seconds or not day:
            messagebox.showerror("Error", "Please fill in all the fields.")
            return

        try:
            date_string = f"{month} {day} {year} {hours}:{minutes}:{seconds}"
            datetime_obj = datetime.strptime(date_string, "%B %d %Y %H:%M:%S")
        except ValueError:
            messagebox.showerror("Error", "Invalid date or time format.")
            return

        for reminder in self.reminders:
            if reminder["Title"] == title:
                messagebox.showerror("Error", f"A reminder with the title '{title}' already exists.")
                return

        reminder = {
            "Title": title,
            "Medium": medium,
            "Date and Time": datetime_obj.strftime("%d-%B-%Y %H:%M:%S"),
        }
        self.reminders.append(reminder)
        self.save_reminders()

        messagebox.showinfo("Reminder Added", "Reminder has been added successfully!")

        # Automatically display the reminders after adding
        self.display_reminders()

    def close_fields(self):
        # Close the add reminder fields
        self.hide_add_fields()

    def hide_add_fields(self):
        if self.fields_frame:
            self.fields_frame.destroy()
            self.fields_frame = None

    def hide_remove_fields(self):
        for widget in self.display_frame.winfo_children():
            widget.destroy()

    def hide_display_fields(self):
        for widget in self.display_frame.winfo_children():
            widget.destroy()

    def load_reminders(self):
        try:
            with open("reminders.json", "r") as file:
                reminders = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            messagebox.showerror("E rror", f"Error loading reminders: {str(e)}")
            reminders = []
        return reminders

    def save_reminders(self):
        try:
            with open("reminders.json", "w") as file:
                json.dump(self.reminders, file)
        except IOError as e:
            messagebox.showerror("Error", f"Error saving reminders: {str(e)}")

    def display_reminders(self):
        self.hide_add_fields()
        self.hide_remove_fields()

        for widget in self.display_frame.winfo_children():
            widget.destroy()

        if not self.reminders:
            messagebox.showinfo("No Reminders", "No reminders to display.")
        else:
            # Sort reminders by date and time before displaying
            sorted_reminders = sorted(self.reminders, key=lambda x: datetime.strptime(x["Date and Time"], "%d-%B-%Y %H:%M:%S"), reverse=True)

            for idx, reminder in enumerate(sorted_reminders):
                reminder_text = f"{idx + 1}. {reminder['Title']} - {reminder['Medium']} - Date: {reminder['Date and Time']}"
                reminder_label = tk.Label(self.display_frame, text=reminder_text, anchor="w")
                reminder_label.grid(row=idx, column=0, sticky="w")

            # Close Button in Display Reminders Section
            close_button = tk.Button(self.display_frame, text="Close", command=self.hide_display_fields)
            close_button.grid(row=len(sorted_reminders), column=0, pady=10)

    def remove_reminder(self):
        self.hide_add_fields()
        self.hide_display_fields()

        for widget in self.display_frame.winfo_children():
            widget.destroy()

        if not self.reminders:
            messagebox.showinfo("No Reminders", "No reminders to remove.")
            return

        for idx, reminder in enumerate(self.reminders):
            reminder_text = f"{reminder['Title']} - {reminder['Medium']} - {reminder['Date and Time']}"
            reminder_label = tk.Label(self.display_frame, text=reminder_text, anchor="w")
            reminder_label.grid(row=idx, column=0, sticky="w")

            remove_button = tk.Button(self.display_frame, text="Remove", command=lambda idx=idx: self.remove_specific_reminder(idx))
            remove_button.grid(row=idx, column=1, padx=5, pady=5)

        # Close Button in Remove Reminder Section
        close_button = tk.Button(self.display_frame, text="Close", command=self.hide_remove_fields)
        close_button.grid(row=len(self.reminders), column=0, pady=10)

    def remove_specific_reminder(self, idx):
        reminder = self.reminders.pop(idx)
        self.save_reminders()
        messagebox.showinfo("Reminder Removed", f"Reminder '{reminder['Title']}' has been removed successfully.")
        self.remove_reminder()

if __name__ == "__main__":
    root = tk.Tk()
    app = ReminderApp(root)
    root.mainloop()
