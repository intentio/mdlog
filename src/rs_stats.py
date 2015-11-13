from optparse import OptionParser

parser = OptionParser()
parser.add_option("-r", "--results", dest="results",
                  help="list of result directories", metavar="RESULTS")
parser.add_option("-s", "--space", dest="space",
                  help="number of configurations", metavar="SPACE")

(options, args) = parser.parse_args()

##Goal: given a set of result directory
# - display configuration space size (product space)
# - display the number of application represented, and their sparsity
# - display % of sparsity

entries = {}
applications = {}

results = open(options.results, 'r')
for result in results.readlines():
  result = result.rstrip('\r\n')
  run = result.split('/')[3].split('-')

  if (run[7] == 'wikipedia'):
    name = run[6] + run[7] + run[8]
  else:
    name = run[6] + run[7]

  entries[run[1]] = {'name': name, 
                     'combination': run[3] + run[4] + run[5],
                     'size': run[7]}

  if (name in applications):
    applications[name] += 1
  else:
    applications[name] = 1

#applications = set((entries[k]['name'] for k in entries.keys()))
event_space = len(applications) * int(options.space)
sparsity = 100 - float((len(entries) * 100/ event_space))
app_sparsity = {a: (100 - float(applications[a] * 100 / 112)) for a in applications}

#for a in applications:
#  print(a + ":" + str(applications[a]))

for e in entries:
  print(e + ":" + str(entries[e]['combination']))

#print(len(set(entries[e]['combination'] for e in entries))) #if entries[e]['name'] == 'cc5m')))

print("###########################################")
print("EVENT SPACE: " + str(event_space))
print("--> CONFIGURATIONS: " + options.space)
print("--> APPLICATIONS: " + str(len(applications)))
print("###########################################")
print("TOTAL TESTS: " + str(len(entries)))
print("TOTAL SPARSITY: " + str(sparsity) + '%')
print("DETAILED APPLICATION SPARSITY: " + str(list(a +":"+ str(app_sparsity[a]) for a in app_sparsity)))
print("###########################################")
