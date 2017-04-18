import csv

# get csv of param info from running the following:
# /Users/scott.cook/Documents/MrsWatson/main/mrswatson -p Obxd --display-info

# file should be of format:
# param num,param name,param value
reader = csv.reader(open('vst_params/Obxd_params.csv'))

#  import to list of lists
# format = {1: ['MidiLearn', '0.000000'], 2: ['Volume', '0.500000'],
# vst_params[1][1] gives 0.00000
vst_params = {}
for row in reader:
    key = int(row[0])
    vst_params[key] = row[1:]

print(vst_params[1])

vst_params_append = ''
for i in vst_params:
    vst_params_append += " --parameter %s,%s" % (i, vst_params[i][1])

# append this to the end of the unix command after setting each value
print vst_params_append
