#!/usr/bin/env python
import csv 
import sys
import subprocess 
import re
import sys
import shlex 

def ipToNum(ip):
    segments = ip.split(".")
    if len(segments) != 4:
        pass
    num = 0
    for i in range(0, len(segments)):
        num = num << 8 | int(segments[i]) 
    return num


def subnetCalculator():
    z = 3 
    for i in L4[3:]:
        try:
            args = "sipcalc " + i 
            args = shlex.split(args)
            proc = subprocess.Popen(args, stdout = subprocess.PIPE, stderr=subprocess.STDOUT)
            result = proc.wait() 
            if result == 0:
                output = proc.stdout.read() 
                p      = re.compile("[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+\ -\ [0-9]+\.[0-9]+\.[0-9]+\.[0-9]+") 
                first  = ipToNum(p.findall(output)[1].split("-")[0])
                last   = ipToNum(p.findall(output)[1].split("-")[1]) 
                ipInfo = p.findall(output)[1].split("-")[0].strip() + "," + p.findall(output)[1].split("-")[1].strip() + "," + str(first) +"," + str(last) + "," +  L1[z] + "," +  L2[z] + "," +  L3[z]  
                print ipInfo 
            z += 1 
        except ValueError:
            pass 
        except IndexError:
            pass 


def rangeToNum(firstRange, lastRange):
    for i in xrange(0, len(firstRange) - 1):
        result = L1[i] + ',' + L2[i] + ',' + str(ipToNum(L1[i])) + ',' + str(ipToNum(L2[i])) +  ',' + L3[i] + ',' + L4[i] + ',' + L5[i]  
        print result 
    

if __name__ == '__main__':
    csvSource = "IP_LOCATION.csv" 
    L1 = [ x[0] for x in csv.reader(open(csvSource,'r')) ]
    L2 = [ x[1] for x in csv.reader(open(csvSource,'r')) ]
    L3 = [ x[2] for x in csv.reader(open(csvSource,'r')) ]
    L4 = [ x[3] for x in csv.reader(open(csvSource,'r')) ]
    L5 = [ x[4] for x in csv.reader(open(csvSource,'r')) ]
    rangeToNum(L1, L2) 

