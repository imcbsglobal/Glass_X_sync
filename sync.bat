@echo off
echo Starting Sync... >> sync.log
sync.exe >> sync.log 2>&1
echo Sync Finished. >> sync.log
exit
