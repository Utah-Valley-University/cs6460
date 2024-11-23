echo off
REM This bat file runs a modified version of the grid world specifically
REM to show the answer to the Value Iteration questions on the midterm
REM do NOT distribute this to students
echo on
python gridworld.py -g ExamGrid -d 0.5 -n 0.0 -v -a value -i 10

echo off
REM just to be complete, here is the ExamGrid code.
REM In my version of gridworld.py, it is an undocumented option
REM on purpose!
REM 
REM def getExamGrid():
REM     grid = [[' ',' ',' ',+1],
REM             [' ','#',' ', ' '],
REM             ['S',' ',' ', +100]]
REM     return Gridworld(grid)