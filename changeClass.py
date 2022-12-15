import os 

inPath = r"C:\Users\eneko\GitHub\TFG-Eneko-Eguiguren-Teknei\annotationsToChange"
outPath = r"C:\Users\eneko\GitHub\TFG-Eneko-Eguiguren-Teknei\newAnnotations"

for txt in os.listdir(inPath):
    newLine = ""
    filename = inPath + os.sep + txt
    with open(filename) as f:
        t = f.readlines()
        for i in t:
            l = list(i)
            l[0] = '1'
            newLine = ''.join(l)
            print(newLine)

    try:
        with open(filename, 'w') as f:
            f.write(newLine)
    except FileNotFoundError:
        print("The 'docs' directory does not exist")