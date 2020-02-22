echo populating database...
cd database 
python3 initialize_database.py
cd ..

echo starting server...
python3 main.py
cd database
