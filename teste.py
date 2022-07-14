
# Import datetime module
import datetime
 
# Get current date and time
dt = datetime.datetime.now()
 
# Format datetime string
x = dt.strftime("%Y-%m-%d %H:%M:%S")
 
# This is going to print something like:
# 2018-08-11 16:25:05
print(x)