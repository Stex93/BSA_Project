

vcf = open("calls.vcf", "r")

line = "#"
while(line[0] == "#"):
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
        target_frag = tmp[4].split(",")[0]  #fix maybe later

        ref.append(ref_frag)
        target.append(target_frag)

        if len(ref_frag) > len(target_frag):
            for a in range(len(ref_frag) - len(target_frag)):
                target.append("-")
        elif len(ref_frag) < len(target_frag):
            for a in range(len(target_frag) - len(ref_frag)):
                ref.append("-")

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

print len(ref)
print len(ref_original)

output = open("output2.fasta", "w")

output.write(ref_name + "\n")
output.write(ref_str + "\n")
output.write(">B'\n")
output.write(target_str + "\n")

output.close()