import os, random, signal
from copy import deepcopy
from csv import DictReader
from operator import itemgetter


# Step 1: Edit MentorSignup.csv and StudentSignup.csv which should both be downloaded and renamed from the project review signup forms. Edit the column names
# to be 'name', 'times', 'areas', 'email'. These are the only columns that need to be extracted for this algorithm.
# Step 2: Move results and directories as you find fit.
# Step 3: Run python3 project_review.py
# Step 4: Ctrl + c when you think there are enough results generated.
# Step 5: Copy paste results to the spreadsheet created on the drive.


boolean = True


def signal_handler(sig, frame):
	global boolean
	print('\nRandom Matching Algorithm ending...')
	boolean = False


def loadMentors(path):
	mentors = []
	with open(path + '/MentorSignup.csv') as infile:
		read = DictReader(infile)
		for row in read:
			person = {'name':'', 'times':[], 'areas':[], 'tcount':0, 'acount':0, 'count':0, 'email':''}
			person['name'] = row['name']
			person['times'] = row['times'].split(', ')
			person['tcount'] = len(person['times'])
			person['areas'] = row['areas'].split(', ')
			person['acount'] = len(person['areas'])
			person['email'] = row['email']
			mentors.append(person)
	return mentors


def loadStudents(path):
	students = []
	with open(path + '/StudentSignup.csv') as infile:
		read = DictReader(infile)
		for row in read:
			person = {'name':'', 'times':[], 'areas':[], 'tcount':0, 'acount':0, 'mentor':'None', 'email':'', 'mentoremail':'None'}
			person['name'] = row['name']
			person['times'] = row['times'].split(', ')
			person['tcount'] = len(person['times'])
			person['areas'] = row['areas'].split(', ')
			person['acount'] = len(person['areas'])
			person['email'] = row['email']
			students.append(person)
	return students


def matchMake(path, students, mentors):
	# timeDemand = {'6:30 - 7:00 pm': 0, '7:00 - 7:30 pm': 0, '7:30 - 8:00 pm': 0}
	# timeSupply = {'6:30 - 7:00 pm': 0, '7:00 - 7:30 pm': 0, '7:30 - 8:00 pm': 0}
	oldMentors = deepcopy(mentors)
	oldStudents = deepcopy(students)
	while boolean:
		score = 0
		students = deepcopy(oldStudents)
		random.shuffle(students)
		mentors = deepcopy(oldMentors)
		for s in students:
			# for i in students:
			# 	for t in i[times]:
			# 		timeDict[t] += 1
			# mentors = sorted(mentors, key=itemgetter('count', 'tcount', 'acount'))
			random.shuffle(mentors)
			for m in mentors:
				if m['count'] <= 2:
					found = verifyMatch(s, m)
					if found > 0:
						score += found
						break
		output = True

		for s in students:
			if s['mentor'] == 'None':
				output = False

		outfilename = str(score) + '.txt'
		if (output) & (not os.path.isfile(path + '/results/results' + outfilename)):
			print('Matching Found: results' + str(score) + '.txt')
			with open(path + '/results/results' + outfilename, 'w') as outfile:
				outfile.write(str(score))
				outfile.write('\n-----\n')
				for s in students:
					outfile.write('{:25} | {:14} | {:25} | {:40} | {:100}'.format(s['mentor'], s['time'], s['name'], s['mentoremail'], s['email']))
					outfile.write('\n')
				outfile.write('Counts\n-----\n')
				for m in mentors:
					outfile.write('{:25} | {:1}'.format(m['name'], m['count']))
					outfile.write('\n')
				outfile.write('\n')
		else:
			print('Something went wrong. Matching not found. Most likely there are not enough mentor time slots for the students.')
			with open(path + '/results/results' + outfilename, 'w') as outfile:
				for s in students:
					if s['mentor'] == 'None':
						outfile.write('{:25} | {:14} | {:25} | {:40} | {:100}'.format(s['mentor'], 'No Time Avail ', s['name'], s['mentoremail'], s['email']))
	return


def verifyMatch(student, mentor):
	first = False
	found = False
	score = 0
	matches = []
	time = ''
	for t in student['times']:
		if t in mentor['times']:
			matches.append(t)
			first = True
	if matches:
		random.shuffle(matches)
		mentor['times'].remove(matches[0])
	if first:
		score += 1
		for a in student['areas']:
			if a in mentor['areas']:
				score += 1
		found = True
	if found:
		student['mentor'] = mentor['name']
		student['mentoremail'] = mentor['email']
		student['time'] = matches[0]
		mentor['count'] += 1
	return score


def main():
	signal.signal(signal.SIGINT, signal_handler)
	path = os.getcwd()
	mentors = loadMentors(path)
	students = loadStudents(path)
	students = sorted(students, key=itemgetter('tcount', 'acount'))
	matchMake(path, students, mentors)
	# for s in students:
	# 	print(s['name'] + ': ' + s['mentor'])
	# for m in mentors:
	# 	print(m['name'] + ': ' + str(m['count']))
	return

if __name__ == '__main__':
	main()