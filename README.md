# Python Dzen2 Pomodoro Timer

A simple desktop pomodoro timer written in python. 

### Prerequisites

You will need [Dzen2](https://github.com/robm/dzen), and python3

### Using the timer 

You can use the timer by piping it to dzen2 with your desired settings. 
Make sure you run python with unbuffered stdout flag -u

For example:

```
cd dzen_timer
python -u time_controller.py  | dzen2 -x 10 -y 1000 -w 300 -h 30 -u
```

NOTE: This will run the timer in a dzen title bar, (rather than a slave window). So it will elminate
any existing dzen title bars. Depending on you display you will have to adjust the x and y coordinates
to place it on your taskbar. 






