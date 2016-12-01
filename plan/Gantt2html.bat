@echo off
@echo pandoc Gantt.md -o Gantt.html
pandoc -s -t html5 Gantt.md --template templates/gantt-template.html -o Gantt.html
@echo sed fine-tuning...
sed -i -- 's/.code.gantt/gantt/' Gantt.html
sed -i -- 's/..code.\(..pre.\)/\1/' Gantt.html
@echo.
pause
