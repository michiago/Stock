import fillDatabase  as db
import application as app

selection = input('Do you want to reinstall the database? \nYour choice (y/n): ')
if selection == 'y':
    db.createTables()

app.menu()
