@echo off

cd "%~1"
for /r %i in (*) do @unoconv %i
