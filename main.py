'''
Calendar Reminder Template Project

This application creates Google Calendar events with preset reminders.
Reminder presets: 0min, 30min, 1hr, 3hr & 5hr
The user can choose how critical the event is to determine how many reminders to set.
'''

import os
import datetime
import pickle
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import google.auth.exceptions
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Google Calendar API setup
SCOPES = ['https://www.googleapis.com/auth/calendar']

def get_calendar_service():
    """Set up and return a Google Calendar service object."""
    creds = None
    
    # Check if token.json exists with stored credentials
    if os.path.exists('token.json'):
        with open('token.json', 'rb') as token:
            creds = pickle.load(token)
    
    # If credentials don't exist or are invalid, get new ones
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except google.auth.exceptions.RefreshError:
                # If refresh fails, create new credentials
                if os.path.exists('credentials.json'):
                    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                    creds = flow.run_local_server(port=0)
                else:
                    messagebox.showerror("Error", "credentials.json file not found. Please download it from Google Cloud Console.")
                    return None
        elif os.path.exists('credentials.json'):
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        else:
            messagebox.showerror("Error", "credentials.json file not found. Please download it from Google Cloud Console.")
            return None
        
        # Save the credentials for future use
        with open('token.json', 'wb') as token:
            pickle.dump(creds, token)

    # Build and return the service
    return build('calendar', 'v3', credentials=creds)

class CalendarReminderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calendar Reminder Template")
        self.root.geometry("600x400")
        self.root.resizable(False, False)
        
        # Define reminder presets (in minutes)
        self.reminder_presets = {
            "0min": 0,
            "30min": 30,
            "1hr": 60,
            "3hr": 180,
            "5hr": 300
        }
        
        # Define criticality levels and corresponding reminders
        self.criticality_levels = {
            "Low (1 reminder)": ["0min"],
            "Medium (3 reminders)": ["0min", "30min", "1hr"],
            "High (All reminders)": ["0min", "30min", "1hr", "3hr", "5hr"]
        }
        
        self.create_widgets()
    
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill="both", expand=True)
        
        # Event name
        ttk.Label(main_frame, text="Event Name:").grid(row=0, column=0, sticky="w", pady=(0, 10))
        self.event_name_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.event_name_var, width=40).grid(row=0, column=1, sticky="ew", pady=(0, 10))
        
        # Date selection
        ttk.Label(main_frame, text="Date:").grid(row=1, column=0, sticky="w", pady=(0, 10))
        self.date_picker = DateEntry(main_frame, width=20, background='darkblue',
                               foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
        self.date_picker.grid(row=1, column=1, sticky="w", pady=(0, 10))
        
        # Time selection
        time_frame = ttk.Frame(main_frame)
        time_frame.grid(row=2, column=0, columnspan=2, sticky="w", pady=(0, 10))
        
        ttk.Label(time_frame, text="Time:").pack(side="left", padx=(0, 10))
        
        self.hour_var = tk.StringVar()
        self.hour_combobox = ttk.Combobox(time_frame, textvariable=self.hour_var, width=3)
        self.hour_combobox['values'] = [f"{i:02d}" for i in range(24)]
        self.hour_combobox.current(9)  # Default to 9 AM
        self.hour_combobox.pack(side="left")
        
        ttk.Label(time_frame, text=":").pack(side="left")
        
        self.minute_var = tk.StringVar()
        self.minute_combobox = ttk.Combobox(time_frame, textvariable=self.minute_var, width=3)
        self.minute_combobox['values'] = [f"{i:02d}" for i in range(0, 60, 5)]
        self.minute_combobox.current(0)  # Default to 00
        self.minute_combobox.pack(side="left")
        
        # Duration
        ttk.Label(main_frame, text="Duration (minutes):").grid(row=3, column=0, sticky="w", pady=(0, 10))
        self.duration_var = tk.StringVar(value="60")
        duration_entry = ttk.Entry(main_frame, textvariable=self.duration_var, width=10)
        duration_entry.grid(row=3, column=1, sticky="w", pady=(0, 10))
        
        # Criticality selection
        ttk.Label(main_frame, text="Event Criticality:").grid(row=4, column=0, sticky="w", pady=(0, 10))
        self.criticality_var = tk.StringVar()
        criticality_combobox = ttk.Combobox(main_frame, textvariable=self.criticality_var, width=25)
        criticality_combobox['values'] = list(self.criticality_levels.keys())
        criticality_combobox.current(1)  # Default to medium
        criticality_combobox.grid(row=4, column=1, sticky="w", pady=(0, 10))
        
        # Show reminders that will be set
        ttk.Label(main_frame, text="Reminders to be set:").grid(row=5, column=0, sticky="w", pady=(0, 10))
        
        self.reminders_var = tk.StringVar()
        ttk.Label(main_frame, textvariable=self.reminders_var).grid(row=5, column=1, sticky="w", pady=(0, 10))
        
        # Update reminders display when criticality changes
        self.criticality_var.trace('w', self.update_reminders_display)
        self.update_reminders_display()
        
        # Create event button
        create_button = ttk.Button(main_frame, text="Create Event", command=self.create_event)
        create_button.grid(row=6, column=0, columnspan=2, pady=(20, 0))
        
        # API status indicator
        self.status_var = tk.StringVar(value="API Status: Not Connected")
        status_label = ttk.Label(main_frame, textvariable=self.status_var)
        status_label.grid(row=7, column=0, columnspan=2, pady=(20, 0))
        
        # Connect to API on startup
        self.root.after(1000, self.check_api_connection)
    
    def update_reminders_display(self, *args):
        criticality = self.criticality_var.get()
        if (criticality in self.criticality_levels):
            reminder_list = self.criticality_levels[criticality]
            self.reminders_var.set(", ".join(reminder_list))
    
    def check_api_connection(self):
        try:
            service = get_calendar_service()
            if service:
                self.status_var.set("API Status: Connected")
                self.service = service
            else:
                self.status_var.set("API Status: Not Connected")
        except Exception as e:
            self.status_var.set(f"API Error: {str(e)[:50]}")
    
    def create_event(self):
        # Validate inputs
        event_name = self.event_name_var.get().strip()
        if not event_name:
            messagebox.showerror("Error", "Please enter an event name")
            return
        
        # Get date and time
        selected_date = self.date_picker.get_date()
        try:
            hour = int(self.hour_var.get())
            minute = int(self.minute_var.get())
            duration = int(self.duration_var.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid time and duration values")
            return
        
        # Create start and end datetimes
        start_time = datetime.datetime.combine(selected_date, datetime.time(hour, minute))
        end_time = start_time + datetime.timedelta(minutes=duration)
        
        # Format for Google Calendar API
        start_str = start_time.isoformat()
        end_str = end_time.isoformat()
        
        # Get criticality and corresponding reminders
        criticality = self.criticality_var.get()
        reminder_names = self.criticality_levels.get(criticality, ["0min"])
        
        # Create event
        try:
            if not hasattr(self, 'service'):
                self.check_api_connection()
                if not hasattr(self, 'service'):
                    messagebox.showerror("Error", "Not connected to Google Calendar API")
                    return
            
            # Create reminders
            reminders = {
                'useDefault': False,
                'overrides': [
                    {'method': 'popup', 'minutes': self.reminder_presets[name]} 
                    for name in reminder_names
                ]
            }
            
            event = {
                'summary': event_name,
                'start': {
                    'dateTime': start_str,
                    'timeZone': 'America/Los_Angeles',  # You might want to get this from the system
                },
                'end': {
                    'dateTime': end_str,
                    'timeZone': 'America/Los_Angeles',
                },
                'reminders': reminders,
            }
            
            event = self.service.events().insert(calendarId='primary', body=event).execute()
            messagebox.showinfo("Success", f"Event created: {event.get('htmlLink')}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Failed to create event: {str(e)}")


if __name__ == "__main__":
    # Create the main window
    root = tk.Tk()
    app = CalendarReminderApp(root)
    root.mainloop()