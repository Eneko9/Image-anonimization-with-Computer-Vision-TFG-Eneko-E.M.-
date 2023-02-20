import os

results = r"C:\Users\eneko\GitHub\TFG-Eneko-Eguiguren-Teknei\static\annotationResults"
expected = r"C:\Users\eneko\GitHub\TFG-Eneko-Eguiguren-Teknei\testing\expected-annotations"

def getInfoFromYoloAnnotations(line):
    annotationArray = []
    if line != "":
        line = line.split(" ")
        line[-1] = line[-1].split("\n")[0]
        annotationArray.extend([int(line[0]), float(line[1]), float(line[2]), float(line[3]), float(line[4])])
    return annotationArray

def check_annotation(expected, results):
    # Comprobamos si las anotaciones tienen la misma clase
    if expected[0] != results[0]:
        return False
    
    # Obtenemos las coordenadas de los rectángulos delimitadores
    exp_x, exp_y, exp_w, exp_h = expected[1:]
    res_x, res_y, res_w, res_h = results[1:]
    
    # Comprobamos si el objeto esperado está dentro del objeto detectado
    if (res_x - res_w/2) <= exp_x <= (res_x + res_w/2) and \
       (res_y - res_h/2) <= exp_y <= (res_y + res_h/2) and \
       exp_w <= res_w and exp_h <= res_h:
        return True
    else:
        return False

def compareResults(results, expected):
    expectedNumerOfImgs = 129
    with open("report.txt", "w") as report:
        precisions = [] # list of percentages of correct annotations
        generalPrecisions = []
        for folder in os.listdir(expected):
            print(f"-------------->IMAGES THAT CONTAIN {folder} ({len(os.listdir(expected + os.path.sep + folder))} in total)")
            report.write(f"-------------->IMAGES THAT CONTAIN {folder} ({len(os.listdir(expected + os.path.sep + folder))} in total) \n")
            for f in os.listdir(results):
                correct = 0
                filename = f.split(".")[0]
                if f.endswith(".txt") and f in os.listdir(expected + os.path.sep + folder):
                    with open(os.path.join(results, f), "r") as result:
                        with open(os.path.join(expected + os.path.sep + folder, f), "r") as exp:
                            resultLines = result.readlines()
                            expectedLines = exp.readlines()
                            for i in range(len(expectedLines)):
                                detected = False
                                for z in range(len(resultLines)):
                                    if check_annotation(getInfoFromYoloAnnotations(expectedLines[i]), getInfoFromYoloAnnotations(resultLines[z])):
                                        correct += 1
                                        detected = True
                                        break
                                if not detected:
                                    print(f"WARNING: The model has not detected one object ({i+1}) in image {filename} .")
                                    report.write(f"WARNING: The model has not detected one object ({i+1}) in image {filename} .\n")  
                            #get the precision  
                            print(correct)
                            print(len(expectedLines))
                            precision = correct / len(expectedLines) * 100

                            print(f"In image {filename} there are {correct} / {len(expectedLines)} correct annotations.")
                            report.write(f"In image {filename} there are {correct} / {len(expectedLines)} correct annotations.\n")

                            print(f"The precision in image {filename} is {precision} %")
                            report.write(f"The precision in image {filename} is {precision} %\n")

                            print("··························")
                            report.write("··························\n")

                            precisions.append(precision)

            print("/////////////////////////////////////")
            report.write("/////////////////////////////////////\n")
            generalPrecisions.append(sum(precisions) / len(os.listdir(expected + os.path.sep + folder))) 
            print(sum(precisions) / len(precisions))
            print(f"The average precision in {folder} is {sum(precisions) / len(os.listdir(expected + os.path.sep + folder))}% (in {len(precisions)} / {len(os.listdir(expected + os.path.sep + folder))} images was detected something)")
            report.write(f"The average precision in {folder} is {sum(precisions) / len(os.listdir(expected + os.path.sep + folder))}% ({len(precisions)} / {len(os.listdir(expected + os.path.sep + folder))})\n")

            print("/////////////////////////////////////")
            report.write("/////////////////////////////////////\n")
                    
            precisions.clear()   

        nothingDetected = expectedNumerOfImgs - len(os.listdir(results))
        print(nothingDetected)
        print("-------------------------------------")
        report.write("-------------------------------------\n")
        print(generalPrecisions)
        print(f"The average precision is {sum(generalPrecisions) / len(generalPrecisions)} %")
        report.write(f"The average precision is {sum(generalPrecisions) / len(generalPrecisions)} %\n")
                        
compareResults(results, expected)

