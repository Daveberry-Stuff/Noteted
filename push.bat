@echo off
set /p "GitCommitName=Git Commit Name: "
set /p "GitCommitDescription=Git Commit Description: "
echo    Continue?
pause

git add .
git commit -a -m "%GitCommitName%" -m "%GitCommitDescription%"
git push