# **Calendar Reminder Template Project**

A Python GUI application that simplifies creating Google Calendar events with customizable reminder configurations.

## **Overview**

This application addresses a common need for consistent reminder patterns when creating calendar events. Instead of manually configuring multiple reminders for each new calendar event, this tool lets you:

* Select from predefined "criticality" levels that determine how many reminders you'll get  
* Choose dates and times with an intuitive interface  
* Set event durations easily  
* Automatically apply your preferred reminder configuration (0min, 30min, 1hr, 3hr, 5hr) based on event importance

## **Features**

* **Reminder Templates**: Preconfigured reminder sets based on event criticality  
  * Low (1 reminder): Notification at event time  
  * Medium (3 reminders): Notifications at event time, 30 minutes, and 1 hour before  
  * High (5 reminders): Notifications at event time, 30 minutes, 1 hour, 3 hours, and 5 hours before  
* **User-Friendly Interface**:  
  * Date picker calendar  
  * Time selection dropdowns  
  * Duration input  
  * Criticality level selector  
* **Google Calendar Integration**:  
  * Securely connects to your Google Calendar  
  * Creates events with proper reminder configurations  
  * Provides OAuth authentication flow

## **Requirements**

* Python 3.6 or higher  
* Google account with Calendar access  
* Google Cloud project with Calendar API enabled

## **Installation**

1. Clone the repository:  
2. git clone https://github.com/yourusername/Calendar\_Reminder\_Template\_Project.git  
3. cd Calendar\_Reminder\_Template\_Project  
4. Install the required packages:  
5. pip install \-r requirements.txt  
6. Set up Google Calendar API:  
   * Go to the Google Cloud Console  
   * Create a new project  
   * Enable the Google Calendar API  
   * Create OAuth credentials (Desktop Application)  
   * Download the credentials JSON file and save it as credentials.json in the project folder

## **Usage**

1. Run the application:  
2. python main.py  
3. On first run:  
   * The app will open a browser window asking you to authorize access to your Google Calendar  
   * After authorization, the token will be saved for future use  
4. Creating an event:  
   * Enter the event name  
   * Select the date  
   * Choose the time and duration  
   * Select criticality level  
   * Click "Create Event"

## **Dependencies**

* google-api-python-client: Google API client library  
* google-auth-httplib2: HTTP client for Google Auth  
* google-auth-oauthlib: OAuth support for Google Auth  
* tkcalendar: Calendar widget for tkinter

## **License**

MIT

## **Contributing**

Contributions are welcome\! Please feel free to submit a Pull Request.  
