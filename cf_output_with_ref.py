#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
COMP9334 Project sample file 

This file compares the output files against their reference.

For trace mode, it checks mrt_*.txt and dep_*.txt

For random mode, it checks mrt_*.txt only 

Assumptions on file location: This file assumes that the output/ and ref/
sub-directories are below the directory that this file is located.
    
    Directory containing cf_output_with_ref.py
    |
    |
    |---- Sub-directory: config
    |---- Sub-directory: output
    |---- Sub-directory: ref
    

This version: 16 March 2024

@author: ctchou
"""

# import sys for input argument 
import sys
import os 


# import numpy for easy comparison 
import numpy as np
import pandas as pd

def read_dep_file(file_path):
    output_df = pd.read_csv(file_path, header=None, sep=r'\s+',
                        names=['arr_time','dep_time','ser_class'],
                        dtype={'arr_time':float,'dep_time':float,'ser_class':str})

    output_class = output_df['ser_class'].str.strip().values.astype(str)

    output_times = output_df[['arr_time','dep_time']].values

    return output_times, output_class

def main():
    
    # Check whether there is an input argument 
    if len(sys.argv) == 2:
        t = int(sys.argv[1])
        test_dep = True
        test_mrt = True      
    elif len(sys.argv) == 3:
        t = int(sys.argv[1])
        if sys.argv[2] == 'dep':
            test_dep = True
            test_mrt = False
        if sys.argv[2] == 'mrt':
            test_dep = False
            test_mrt = True
    else:
        print('Error: Expect the test number as the input argument')
        print('Example usage: python3 cf_output_with_ref.py 1')   
        return
    
    # Location of the folders
    out_folder = 'output'
    ref_folder = 'ref'
        
    # Definitions
    file_ext = '.txt' # File extension
    
    # For trace mode, an absolute tolerance is used
    ABS_TOL = 1e-3  # Absolute tolerance 

    # t is the test number
    # Tests 0 to 3 are trace mode
    # Tests 4 to 6 are is random mode
    trace_mode_test_start = 0
    trace_mode_test_end = 3 # Tests 1 to 6 
    random_mode_test_start = 4
    random_mode_test_end = 6 
    
    # For tests 4-6 (which are in random mode), 
    # the mean response time is expected to be within the range 
    MRT_TOL = { 
                 4: {'class_0':[1.414 , 3.3187], 'class_1': [2.6596, 5.4192]}, 
                 5: {'class_0':[1.5555, 2.5282], 'class_1': [3.3785, 6.8222]}, 
                 6: {'class_0':[2.0404, 3.5834], 'class_1': [2.9928, 5.2165]} 
                }
            
    
    
    if t in range(trace_mode_test_start,trace_mode_test_end+1): 
    
        if test_mrt:
            # Compare mrt against the reference
            out_file = os.path.join(out_folder,'mrt_'+str(t)+file_ext)
            ref_file = os.path.join(ref_folder,'mrt_'+str(t)+'_ref'+file_ext)
            
            try: 
                if os.path.isfile(out_file):
                    mrt_stu = np.loadtxt(out_file)
                else:
                    print('Error: File ',out_file,'does NOT exist')    
                    return
                
                if os.path.isfile(ref_file): 
                    mrt_ref = np.loadtxt(ref_file)
                else:
                    print('Error: File ',ref_file,'does NOT exist')    
                    return  
            
                if np.allclose(mrt_stu,mrt_ref,atol=ABS_TOL):
                    print('Test '+str(t)+': Mean response time matches the reference')
                else: 
                    print('Test '+str(t)+': Mean response time does NOT match the reference')
            except:
                print('Something went wrong with the comparison.')
                print(f'The contents of the mrt_{t}.txt that your program has produced are:')
                os.system(f'cat output/mrt_{t}.txt')
   
        if test_dep:
            # Compare dep against the reference  
            out_file = os.path.join(out_folder,'dep_'+str(t)+file_ext)
            ref_file = os.path.join(ref_folder,'dep_'+str(t)+'_ref'+file_ext)

            try:             
                if os.path.isfile(out_file):
                    [dep_stu_times, dep_stu_class] = read_dep_file(out_file)
                else:
                    print('Error: File ',out_file,'does NOT exist')    
                    return            
                
                if os.path.isfile(ref_file):
                    [dep_ref_times, dep_ref_class] = read_dep_file(ref_file)
                else:
                    print('Error: File ',ref_file,'does NOT exist')    
                    return                      
    
                # print(dep_stu.shape)
                # print(dep_ref.shape, dep_stu.shape == dep_ref.shape)
                if dep_stu_times.shape == dep_ref_times.shape and \
                   dep_stu_class.shape == dep_ref_class.shape:    
                    if np.allclose(dep_stu_times,dep_ref_times,atol=ABS_TOL) and \
                       np.all(dep_stu_class == dep_ref_class):
                        print('Test '+str(t)+': Departure times match the reference')
                    else: 
                        print('Test '+str(t)+': Departure times do NOT match the reference')
                else:
                    nr_stu = dep_stu_times.shape[0]
                    nc_stu = dep_stu_times.shape[1]
                    nr_ref = dep_ref_times.shape[0]
                    nc_ref = dep_ref_times.shape[1]
                    print(f"Error: Your dep_{t}.txt has {nr_stu} rows and {nc_stu} columns but we expect {nr_ref} rows and {nc_ref}")
            except:
                print('Something went wrong with the comparison.')
                print(f'The contents of the dep_{t}.txt that your program has produced are:')
                os.system(f'cat output/dep_{t}.txt')
  
    
    elif t in range(random_mode_test_start,random_mode_test_end+1): 
        out_file = os.path.join(out_folder,'mrt_'+str(t)+file_ext)
       
        if os.path.isfile(out_file):
            mrt_stu = np.loadtxt(out_file)
        else:
            print('Error: File ',out_file,'does NOT exist')    
            return        
    
        
        classes = ['class_0','class_1']
    
        for idx in [0,1]:
            if MRT_TOL[t][classes[idx]][0] <= mrt_stu[idx] <= MRT_TOL[t][classes[idx]][1]:
                print('Test '+str(t)+': Mean response time is within tolerance')
            else: 
                print('Test '+str(t)+': Mean response time is NOT within tolerance')
                print('You should try to run a new simulation round with new random numbers.')
                print('Your output need to be within the tolerance for most of the rounds.')
        
    else:
        print('The input argument is not a valid test number')
        
if __name__ == '__main__':
    dep_error = main()            