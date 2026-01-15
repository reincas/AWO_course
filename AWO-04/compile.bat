@echo off

REM Extract lecture number from folder of this batch file
set ScriptPath=%~dp0
set ScriptPath=%ScriptPath:~0,-1%
for %%F in ("%ScriptPath%") do set FolderName=%%~nxF
for /f "tokens=2 delims=-" %%a in ("%FolderName%") do set lecture=%%a
echo Compiling lecture AWO-%lecture%

REM Pause if the resulting pdf file is currently opened
set output=AWO-%lecture%.pdf
set temp=temp.pdf
if exist %temp% (
	del %temp%
)
if exist %output% (
	echo Check status of file %output%...
	rename %output% %temp%
	if errorlevel 1 (
		pause
	) else (
		rename %temp% %output%
	)
)

REM Run the pandoc command for this lecture
@echo on
pandoc AWO-%lecture%.md -o %output% -t beamer --columns=300 --dpi=540

REM Pause in case of an error to keep the window open
@echo off
if errorlevel 1 (
    pause
)