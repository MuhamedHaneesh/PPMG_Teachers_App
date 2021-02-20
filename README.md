# PPMG Teachers App

## Run Directory App
1. Goto the directory where requirements.txt file located run the below commands to install dependancies.
    pip install -r requirements.txt
    

2. Navigate to directory folder where manage.py file located run the beloww commands.

    python manage.py makemigrations

    python manage.py migrate
   
3. Create default user (username:admin,password:admin123).

    python manage.py createsuperuser

4. Run application.

    python manage.py runserver

5. Once you logged in, There will be a bulk upload option on the right.
   choose the teachers csv file as "Names" and zip file which comprises images as  "Images"
   Then click Upload.
   
6. Once you uploaded you can click on the Teachers list in the header navigation.
   see the list of teachers that you uploaded.
   against each teacher, there is a "about link" to get more info about the teacher.