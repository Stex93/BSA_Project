import sys

if __name__ == '__main__':

    try:
        vcf = open("./" + sys.argv[1], "r")
    except IOError:
        print "No such file or directory: " + sys.argv[1]
        print "Exiting.."
        sys.exit()
    # vcf = open("calls.vcf", "r")

    print "Calculating final alignment.."

    line = "#"
    while line[0] == "#":
        line = vcf.readline()

    ref_original = ""
    ref_name = ""

    with open("A.fasta", "r") as f:
        ref_name = f.readline().rstrip("\n")
        for x in f:
            ref_original += x.rstrip("\n")

    f.close()

    ref = []
    target = []
    l = len(ref_original)

    for i in range(l):
        tmp = line.split("\t")
        if i == int(tmp[1]):
            ref_frag = tmp[3]
            target_frag = tmp[4].split(",")[0]  # fix maybe later

            ref.append(ref_frag)
            target.append(target_frag)

            if len(ref_frag) > len(target_frag):
                for a in range(len(ref_frag) - len(target_frag)):
                    target.append("-")
            elif len(ref_frag) < len(target_frag):
                for a in range(len(target_frag) - len(ref_frag)):
                    ref.append("-")

            # maybe we should just comment this line?
            i += len(ref_frag) - 1

            nextline = vcf.readline()
            if len(nextline) > 1:
                line = nextline
        else:
            ref.append(ref_original[i])
            target.append(ref_original[i])

    vcf.close()

    ref_str = "".join(ref)
    target_str = "".join(target)

    n = 70

    ref_list = [ref_str[i:i+n] for i in range(0, len(ref_str), n)]
    target_list = [target_str[i:i+n] for i in range(0, len(target_str), n)]

    print "Saving output file.."
    output = open(sys.argv[1][:len(sys.argv[1])-3] + "output.fasta", "w")
    # output = open("output.fasta", "w")

    output.write(ref_name + "\n")
    for lin in ref_list:
        output.write(lin + "\n")

    output.write(">B'\n")
    for lin in target_list:
        output.write(lin + "\n")

    print "Complete!"

    output.close()
