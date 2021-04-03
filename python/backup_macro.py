import sys
import time
from shutil import copyfile
timestamp = str(time.strftime("%Y-%m-%d-%H-%M"))
print(timestamp)
newname = '12tails_backup_'+timestamp+'.py'
copyfile('12tails.py', r'backup\\'+newname)
# copyfile(sys.argv[1], r'backup\\'+newname)
