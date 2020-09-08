# Project Review

### Background
A randomized matching algorithm for matching mentors with students for Transcend's bi-annual event, Project Review. Generates pairs based using the areas/industries and timeslots as weights.

### Requirements
(If the google signup forms were changed at all, this code won't properly work.)
Python3

### Installation
```
git clone https://github.com/transcend-engineering/proj-review.git
```

### Development
```
1. Download mentor and student google spreadsheets as .csv files
2. Rename mentor spreadsheet to MentorSignup.csv
3. Rename student spreadsheet to StudentSignup.csv
4. Ensure the mentors and students didn't put something unhelpful in their areas/industry section
5. python project_review.py
6. Ctrl + C to end program when you think enough results have been generated
7. Pick a matching in the results/ directory (higher score = better)
8. Paste results to the spreadsheet on the google drive

```
