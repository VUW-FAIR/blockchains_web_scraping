import pandas as pd
import csv




'''
This script goes through a reddit CSV file and searches based on particular subreddit terms.
It then extracts the particular subreddit posts into a new CSV file. This is meant to be used in 
conjunction with the json to csv reddit converter which takes the json reddit file and makes it 
into a flattened CSV. 
'''
def main():
    terms = ['gaming', 'sex']
    read_file_and_output_sorted(terms, "RC_2011-01.csv")

def read_file_and_output_sorted(terms, filename):
    print("hello")

    chunksize = 10 ** 6
    try:
        for input in pd.read_csv(filename, chunksize=chunksize):

            print("fin")
            lines = []
            for i in range(0, len(input)):
                for term in terms:
                    print(term)
                    print("line is " + str(i))
                    if(str(input.subreddit[i]) == term):
                        lines.append(i+1)


            f =  open(filename, newline='', encoding='utf-8')
            w = open('converted_' + filename ,'a', encoding='utf-8', newline="") #a
            out = csv.writer(w)
            reader = csv.reader(f)

            i = 0
            current_line_index = 0 #index of lines array we're currently at
            for row in reader:
                if(i == lines[current_line_index]):
                    print(row)
                    out.writerow(row)
                    current_line_index +=1
                    if(current_line_index >= len(lines)):
                        break
                i +=1

            f.close()
    except Exception as e:
        print(e)

main()