import os

results = r"C:\Users\eneko\GitHub\TFG-Eneko-Eguiguren-Teknei\static\annotationResults"
expected = r"C:\Users\eneko\GitHub\TFG-Eneko-Eguiguren-Teknei\testing\expectedAnnotations"

def getInfoFromYoloAnnotations(line):
    if line != "":
        line = line.split(" ")
        line[-1] = line[-1].split("\n")[0]
        classtype = line[0]
        x = float(line[1])
        y = float(line[2])
        w = float(line[3])
        h = float(line[4])
    return classtype, x, y, w, h

def compareResults(results, expected):
    with open("report.txt", "w") as report:
        precisions = [] # list of percentages of correct annotations
        for f in os.listdir(results):
            correct = 0
            filename = f.split(".")[0]
            if f.endswith(".txt") and f in os.listdir(expected):
                with open(os.path.join(results, f), "r") as result:
                    with open(os.path.join(expected, f), "r") as exp:
                        resultLines = result.readlines()
                        expectedLines = exp.readlines()
                        for i in range(len(expectedLines)):
                            detected = False
                            exp_class, exp_x, exp_y, exp_w, exp_h = getInfoFromYoloAnnotations(expectedLines[i])
                            for z in range(len(resultLines)):
                                res_class, res_x, res_y, res_w, res_h = getInfoFromYoloAnnotations(resultLines[z])
                                half_w = res_w / 2
                                half_h = res_h / 2
                                #si la clase es la misma, comprobar que los valores de x, y, w, h del expected estan dentro del resultado
                                if exp_class == res_class:
                                    if exp_x >= res_x-half_w and exp_x <= res_x+half_w:
                                            if exp_y >= res_y-half_h and exp_y <= res_y+half_h:
                                                        correct += 1
                                                        detected = True
                                                        break
                            if not detected:
                                print(f"WARNING: The model has not detected one object ({i+1}) in image {filename} .")
                                report.write(f"WARNING: The model has not detected one object ({i+1}) in image {filename} .\n")  
                        #get the precision  
                        precision = correct / len(expectedLines) * 100

                        print(f"In image {filename} there are {correct} / {len(expectedLines)} correct annotations.")
                        report.write(f"In image {filename} there are {correct} / {len(expectedLines)} correct annotations.\n")

                        print(f"The precision in image {filename} is {precision} %")
                        report.write(f"The precision in image {filename} is {precision} %\n")

                        print("··························")
                        report.write("··························\n")

                        precisions.append(precision)

        print("-------------------------------------")
        report.write("-------------------------------------\n")
        print(f"The average precision is {sum(precisions) / len(precisions)} %")
        report.write(f"The average precision is {sum(precisions) / len(precisions)} %\n")
                        
compareResults(results, expected)

