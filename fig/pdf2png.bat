@echo off
echo Turning .pdf to .png
echo ""
for %%f in (*.pdf) do (
    echo   %%~nf
    mutool.exe draw -o "%%~nf.png" -w 600 "%%~nf.pdf"
)
echo ""
pause