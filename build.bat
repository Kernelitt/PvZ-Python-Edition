@echo off

echo Building executable...
pyinstaller --onefile --distpath build main.py

echo Copying assets...
xcopy images build\images /E /I /H /Y
xcopy animations build\animations /E /I /H /Y
xcopy sounds build\sounds /E /I /H /Y
xcopy music build\music /E /I /H /Y
xcopy particles build\particles /E /I /H /Y
xcopy properties build\properties /E /I /H /Y
xcopy reanim build\reanim /E /I /H /Y

copy levels.json build\
copy user.json build\
copy HOUSE_OF_TERROR.ttf build\
copy pico12.ttf build\

echo Build complete. Run build\main.exe to play the game.
