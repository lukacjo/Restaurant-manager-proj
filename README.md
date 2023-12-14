# Restaurant_Manager
#### Description:
## This project is built to help restaurants taking care of how many ingredients to order and to have notes in one place to not get distracted. 
## The app is based on Python Flask
All used libraries in requirements.txt file
## Project contains mentioned features:
- Placing orders by restaurant staff to MySQL database
- Notes to save recipes or ideas without getting distracted
- Ingredient inventory with suppliers prices, orders by restaurant staff to MySQL database
- Notes to save recipes or ideas without getting distracted
- Ingredient inventory with suppliers prices

My files:
- main.py
- models.py
- views.py
- auth.py
- create_db.py
- __init__.py

## main.py
This file is used to start the app. Having it in one place makes it easy to start it. Here I choose the port on which the flask app is supposed to run and I turn on or turn off the debugger.
## models.py
In this file, I create the models of data that go into the database. I decide here what will be the primary key, Foreign Key, how long the strings can be, what type of data the columns will be, relationships between tables and also the search form is here.
## __init__.py
Here I create the app with a secret key, create a connection to MySql database, I register blueprints for auth and views, also here I create the tables from models in database also here I initialize the login manager
## create_db.py
Here I create the connection to MySql database and I create the database using mysql. connector. Also here, I can delete and the create the database when for example I wanted to change how the tables look. Also, I can see here what databases are created.
## auth.py
In this file I take care of signing up, logging in and logging out. I get the data from html forms and based on that create the account or login. I hash the passwords using the method="sha256", and while logging in I check them using hash.
## views.py
Here, I take care of all of the sites except the ones in auth. py. First thing is using the blueprint that I've created earlier. 
- /Notes 
    - here I create the notes and add them to the database
    - When POST I get the data from form, title and the body of the note
    - I make sure that the input I correct
    - I use the created model to add the data to the database
    - Using db. session. add (new_note) I add it to the database and the I commit it
    - When GET I just render the notes.html template
- /orders
    - When POST I get the data from a hidden input form, I get the food name so I can use a SQL query to delete all occurrences of that food
    - I used mycursor. execute ("USE `managerdatabase`;") to select the database that I wanted
    - When GET, I create a dictionary to show the sum of all foods. Otherwise, it would be too hard to manage that. This way I can show them at the top as a summary of all orders. By using for loop I add each existing food to how many to order to create a dictionary
- /delete-note
    - I use JS to get the id of a note and send it as json to delete-note, then I load it 
    And based of that query sour notes to get note with that ID. Then I delete it.
    - I make sure that ids of current user match.
- /delete-order
    - Similar to delete note I do it on an order.
- /edit_note/<int:id>
    - Going into edit_note I get the id of the note from the link and based on that I search the note. After that I delete the old note and create a new one with the same id and different title or text.
- /search
    - I use the search form to search through the notes to find the note with text containing similar to searched text and then display the searched notes.
- /menu
    - Here, I get the quantity of how much person wants to order and what food they want to order. Then through module I put it in the database. Also, I ensure the input is correct.
## Now the templates. What do they show.
- signup
    - Signup shows the sign-up page. It contains email, name, surname, password and password confirmation. Its made sure that you can input anything else to the email field than an email.
- search
    - In search is what you get after searching for text in notes. So u can see the text that you searched and the notes that contain the searched word and also edit and delete button for every note.
- orders
    - Orders shows the sum of all foods that were ordered, all orders and delete buttons for bot the sums of all foods and for each order.
- notes
    - In notes, you can see all notes, field for creating a new note and buttons for adding, editing the notes and deleting the notes.
- navbar
    - In navbar is everything that is used in the top and bottom bar. Some features are shown only for logged users, and some only for logged out users. It's here not copying it every time.
- menu
    - In menu you can see all of the foods that are available, you can input the amount wanted and the order it. The are also pictures, descriptions and prices of the goods. There is a button to add each food.
- login
    - To login you can see a field for logging so only email and password fields.
- edit_note
    - Edit note takes you to the place where you can edit the note. You can input a new title or new note description. Also, you can delete the note from here.
