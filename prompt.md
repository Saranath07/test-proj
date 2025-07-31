Quiz Master - V2
It is a multi-user app (one requires an administrator and other users) that acts as an exam preparation site for multiple courses.


Frameworks to be used
These are the mandatory frameworks on which the project has to be built.


SQLite for data storage
Flask for API
VueJS for UI
VueJS Advanced with CLI (only if required, not necessary)
Jinja2 templates if using CDN only for entry point (Not to be used for UI)
Bootstrap for HTML generation and styling (No other CSS framework is allowed)
SQLite for database (No other database is permitted)
Redis for caching
Redis and Celery for batch jobs

Note: All demos should be possible on your local machine.


The platform will have two roles:


Admin - root access - It is the superuser of the app and requires no registration

Admin is also known as the quiz master
There is only one admin to this application
The administrator login redirects to the quiz master/admin dashboard
The administrator will manage all the other users
The administrator will create a new subject
The administrator will add various chapters under a subject
The administrator will add quiz questions under a chapter

User - Can attempt any quiz of its choice

User Register and Login
Each user may have:
id - primary key
Username (email)
Password
Full Name
Qualification
DOB
Choose the subject/chapter name
Start the quiz
View the quiz scores
Terminologies

User: The user will register and login and attempt any quiz of his/her interest.


Admin: The superuser with full control over other users and data. Registration is not allowed for the admin: The admin account must pre-exist in the database when the application is initialized.



Subject: The field of study in which the user wishes to give the quiz. The admin will be creating one or many subjects in the application. Every subject can possible have the following fields:


id - primary key
Name
Description
etc: Additional fields (if any)

Chapter: Each subject can be subdivided into multiple modules called chapters. The possible fields of a chapter can be the following:

id - primary key
Name
Description
etc: Additional fields (if any)

Quiz: A quiz is a test that is used to evaluate the user’s understanding of any particular chapter of any particular subject. A test may contain the following attributes:


id - primary key
chapter_id (foreign key-chapter)
date_of_quiz
time_duration(hh:mm)
remarks (if any)
etc: Additional fields (if any)
Questions: Every quiz will have a set of questions created by the admin. Possible fields for a question include:

id - primary key
quiz_id (foreign key-quiz)
question_statement
option1
option2
etc: Additional fields (if any)

Scores: Stores the scores and details of a user's quiz attempt. Possible fields for scores include:

id - primary key
quiz_id (foreign key-quiz)
user_id (foreign key-user)
time_stamp_of_attempt
total_scored
etc: Additional fields (if any)
Note: The above fields are not exhaustive. Students can add more fields as per their specific requirements.

Application Wireframe
Quiz Master

 


Note:
The provided wireframe is intended only to illustrate the application's flow and demonstrate what should appear when a user navigates between pages.

Replication of the exact views is NOT mandatory.
Students are encouraged to work on their own front-end ideas and designs, while maintaining the application's intended functionality and flow.
Core Functionalities
Admin login and User login

A login/register form with fields like username, password etc. for user and admin login
The application should have only one admin identified by its role
You can either use Flask security (session or token) or JWT based Token based authentication to implement role-based access control
The app must have a suitable model to store and differentiate all types of users
Admin Dashboard - for the Admin

The admin should be added, whenever a new database is created
The admin creates/edits/deletes a subject
The admin creates/edits/deletes a chapter under the subject
The admin will create a new quiz under a chapter
Each quiz contains a set of questions  (MCQ - only one option correct)
The admin can search the users/subjects/quizzes
Shows the summary charts

Quiz management - for the Admin

Edit/delete a quiz
The admin specifies the date and duration(HH: MM) of the quiz
The admin creates/edits/deletes the MCQ (only one option correct)  questions inside the specific quiz

User dashboard - for the User

The user can attempt any quiz of his/her interest
Every quiz has a timer
Each quiz score is recorded
The earlier quiz attempts are shown
To be able to see the summary charts
Note: The database must be created programmatically (via table creation or model code). Manual database creation, such as using DB Browser for SQLite, is NOT allowed.


5. Backend Jobs

a. Scheduled Job - Daily reminders - The application should send daily reminders to users on g-chat using Google Chat Webhooks or SMS or mail

Check if a user has not visited or a new quiz is created by the admin
If yes, then send the alert asking them to visit and attempt the quiz if it is relevant to them
The reminder can be sent in the evening, every day (students can choose the time)
b. Scheduled Job - Monthly Activity Report - Devise a monthly report for the user created using HTML and sent via mail.

The activity report can include quiz details, how many quizzes taken in a month, their score, average score, ranking in the quiz etc.
For the monthly report to be sent, start a job on the first day of every month → create a report using the above parameters → send it as an email
c.1 User Triggered Async Job - Export as CSV - Devise a CSV format details for the quizzes completed by the user


This export is meant to download the quiz details (quiz_id, chapter_id,  date_of_quiz, score, remarks etc.)
Have a dashboard from where the user can trigger the export
This should trigger a batch job, and send an alert once done

OR


c.2 User Triggered Async Job - Export as CSV - Devise a CSV format details for the all quizzes to be seen by the admin


This export is meant to download the user details (user_id, quizzes_taken, average score (performance), etc.)
Have a dashboard from where the admin can trigger the export
This should trigger a batch job, and send an alert once done

6. Performance and Caching


Add caching where required to increase the performance
Add cache expiry
API Performance

Recommended Functionalities
Well-designed PDF reports for Monthly activity reports (Students can choose between HTML and PDF reports)
External APIs/libraries for creating charts, e.g. ChartJS
Single Responsive UI for both Mobile and Desktop
Unified UI that works across devices
Add to desktop feature
Implementing frontend validation on all the form fields using HTML5 form validation or JavaScript
Implementing backend validation within your APIs
Optional Functionalities
Provide styling and aesthetics to your application by creating a beautiful and responsive front end using simple CSS or Bootstrap
Incorporate a proper login system to prevent unauthorized access to the app using Flask extensions like flask_login, flask_security etc.
Implement a dummy payment portal (just a view taking payment details from user for paid quizzes
Any additional feature you feel is appropriate for the application



Evaluation
Students have to create and submit a project report (not more than 5 pages) on the portal, along with the actual project submission
The report must include the following things;
Student details
Project details, including the question statement and how you approached the problem statement
Frameworks and libraries used
ER diagram of your database, including all the tables and their relations
API resource endpoints (if any)
Drive link of the presentation video

Click here of project report demo


        Possible folder structure:





All code is to be submitted on the portal in a single zip file (zipping instructions are given in the project document - Project Doc T12025
Video Presentation Guidelines (Advised):
1. A short Intro (not more than 30 sec)

2. How did you approach the problem statement? (30 sec)

3. Highlight key features of the application (90 sec)

4. Any Additional feature(s) implemented other than core requirements (30 sec)

Note:

1. The final video must not exceed 5-10 minutes.

2. Keeping your video feed on during recording (like in a screencast) is optional but recommended.


The video must be uploaded on the student drive with access to anyone with the link and the link must be included in the report:
This will be viewed during or before the viva, so it should be a clear explanation of your work.
Viva: after the video explanation, you are required to give a demo of your work, and answer any questions that the examiner asks:
This includes making changes as requested and running the code for a live demo.
Other questions that may be unrelated to the project itself but are relevant to the course.
Instructions
This is a live document and will be updated with more details (wireframe)
We will freeze the problem statement on or before 20/12/2024, beyond which any modifications to the statement will be communicated via proper announcements.
The project has to be submitted as a single zip file.