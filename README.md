# Job Application Log Automator

**Job Application Log Automator** is a lightweight tool that automates logging job applications from the *Welcome to the Jungle* job board into a Google Sheet. It drastically reduces manual entry time—just run it, follow the prompts, and let it do the work.

---

### Features

- Scrapes job listing info (e.g., title, company, location, pay, etc.)
- Populates a Google Sheet with columns E–S
- Reduces data entry time from ~60 seconds to ~5 seconds per application
- Option to switch target spreadsheet from within the tool
- Simple terminal interface for easy use

---

### How It Works

Run the program and interact in the terminal. You'll be prompted to provide a job listing URL from *Welcome to the Jungle*. The script will automatically extract job details and write them to your configured Google Sheet. Or you can go to the options menu where you can change the sheet info, enter a URL, or exit the application.

---

### Setup

You’ll need:

- A Google Sheet (preformatted or templated to your liking)
- A Google service account with access to the sheet
- Python 3 and required packages (`gspread`, `oauth2client`, `beautifulsoup`, etc.)
- API with setting to allow automated changes to a sheet, not just the ability to read one.

Make sure to add your credentials file and adjust the config if needed.

### Sheet Layout

The sheet should start on row 4 (titles, 5 is first data line).
It should start on column E and go to S with the following headings.

ID | Company Name | Position | Role | Date | City | State | Country | Position Type | Location Type | Gov? | Salary | Fav? | Notes | Response

ID – Unique identifier for each job entry

Company Name – Name of the company offering the position

Position – Name of position for hire

Role – Type of role (e.g., Job, Internship, Contract)

Date – Date you applied

City – City where the job is located

State – State or region of the job location

Country – Country of the job

Position Type – Weekly time expectations (e.g. Full-time, Part-time, Internship, etc.)

Location Type – Remote, On-site, Hybrid

Gov? – Whether the position is government-related (Yes/No)

Salary – Salary offered or expected (if known, else leave blank)

Fav? – Whether it’s a favorite or preferred job (Yes, else leave blank)

Notes – Any custom notes or observations

Response – Outcome or current status (e.g., ? (meaning waiting for response), Yes, Test, Code Review, Interview, No, etc.)

### Required Files
google-sheet-API.json

sheet-info.json

The API file info is available online or using AI code generation.

The sheet info file should look like this:
{
    "sheet_name": "Your Sheet Name",
    "worksheet_name": "Your Worksheet Name"
}

---

### Future Plans

- Add support for LinkedIn, Indeed, and other major job platforms.
- Add a way to get the state from the given city.
- Add a way to handle non-American applications.
- Maybe implement optional browser extension or GUI.

---

### Disclaimer

Currently supports only *Welcome to the Jungle*. Expanding support is in progress. Use responsibly—always respect platform terms of service.
