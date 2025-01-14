@echo on
REM test_django.bat

cd C:\Users\grego\logboekmentalegezondheid\mental_health_web
call C:\Users\grego\logboekmentalegezondheid\venv\Scripts\activate.bat
python manage.py runserver 127.0.0.1:8000
pause