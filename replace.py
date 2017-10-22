fo = open("8085.py", "r")

lines = fo.readlines()
fo.close()

i=0
while(i<len(lines)):

    if(lines[i].strip() == "'''"):
        lines.pop(i)

        while(lines[i].strip() != "'''"):

            if(lines[i].strip() == ""):
                lines[i] = "        #\n"
                i+=1
                continue

            lines[i] = "        # " + lines[i].lstrip()
            i+=1
        lines.pop(i)

    else:
        i+=1

fo = open("8085_1.py", "w")
for line in lines:
    fo.write(line)
fo.close()