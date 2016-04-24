import sys

if __name__ == '__main__':

    try:
        f = open("./" + sys.argv[1], "r")
    except IOError:
        print "No such file or directory: " + sys.argv[1]
        print "Exiting.."
        sys.exit()

    try:
        vcf = open("./" + sys.argv[2], "r")
    except IOError:
        print "No such file or directory: " + sys.argv[2]
        print "Exiting.."
        sys.exit()

    print "Calculating final alignment.."

    line = "#"
    while line[0] == "#":
        line = vcf.readline()

    ref_original = ""
    ref_name = ""

    ref_name = f.readline().rstrip("\n")
    for x in f:
        ref_original += x.rstrip("\n")

    f.close()

    ref = []
    target = []

    for c in ref_original:
        ref.append(c)
        target.append(c)

    insertions = 0
    while len(line) > 1:
        tmp = line.split("\t")
        pos = int(tmp[1])
        ref_frag = tmp[3]
        target_frag = tmp[4].split(",")[0]  # fix maybe later
        if len(ref_frag) == len(target_frag):
            i = 0
            for c in target_frag:
                target[pos - 1 + i + insertions] = c
                i += 1
        elif len(ref_frag) > len(target_frag):
            i = 0
            for c in target_frag:
                target[pos - 1 + i + insertions] = c
                i += 1
            n = len(ref_frag) - len(target_frag)
            for j in range(n):
                target[pos - 1 + i + insertions] = "-"
                i += 1
        elif len(ref_frag) < len(target_frag):
            i = 0
            for c in target_frag[:len(ref_frag)]:
                target[pos - 1 + i + insertions] = c
                i += 1
            n = len(target_frag) - len(ref_frag)
            for j in range(n):
                ref.insert(pos - 1 + i + insertions, "-")
                target.insert(pos - 1 + i + insertions, target_frag[i])
                insertions += 1
                i += 1
        line = vcf.readline()

    vcf.close()

    ref_str = "".join(ref)
    target_str = "".join(target)

    j = 0
    for i in range(0, len(ref_str)):
        if ref_str[i] != target_str[i]:
            j += 1
    print "Variants detected: " + str(j)

    b = True
    check = ref_str.replace("-", "")
    if check != ref_original:
        b = False
    print "Format check: " + str(b)

    n = 70

    ref_list = [ref_str[i:i+n] for i in range(0, len(ref_str), n)]
    target_list = [target_str[i:i+n] for i in range(0, len(target_str), n)]

    print "Saving output file.."
    output = open(sys.argv[2][:len(sys.argv[2])-3] + "output.fasta", "w")
    # output = open("output.fasta", "w")

    output.write(ref_name + "\n")
    for lin in ref_list:
        output.write(lin + "\n")

    output.write(">B'\n")
    for lin in target_list:
        output.write(lin + "\n")

    print "Complete!"

    output.close()
