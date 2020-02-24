echo populating database...
cd database 
python3 initialize_database.py
cd ..


echo starting main server...
python3 main.py
cd database

