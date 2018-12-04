import os
from csv import DictReader
from operator import itemgetter
import random
from copy import deepcopy

				# Want to fill in fewest students in certain time first
				# Want to use mentors with more times first
				# Want to use mentors with fewer students first
				# Want to ideally use counts of areas as well
					# Want to fill in fewest students 
				# Option 1: extensive search with a score rubric//
					# first search on students and mentors and their areas
						# second search on all possible times
				# Option 2: greedy search with many factors
				# Option 3: random search until all assigned or for highest score


def loadMentors(path):
	mentors = []
	with open(path + '/MentorSignup.csv') as infile:
		read = DictReader(infile)
		for row in read:
			person = {'name':'', 'times':[], 'areas':[], 'tcount':0, 'acount':0, 'count':0}
			person['name'] = row['name']
			person['times'] = row['times'].split(', ')
			person['tcount'] = len(person['times'])
			person['areas'] = row['areas'].split(', ')
			person['acount'] = len(person['areas'])
			mentors.append(person)
	return mentors


def loadStudents(path):
	students = []
	with open(path + '/StudentSignup.csv') as infile:
		read = DictReader(infile)
		for row in read:
			person = {'name':'', 'times':[], 'areas':[], 'tcount':0, 'acount':0, 'mentor':'None'}
			person['name'] = row['name']
			person['times'] = row['times'].split(', ')
			person['tcount'] = len(person['times'])
			person['areas'] = row['areas'].split(', ')
			person['acount'] = len(person['areas'])
			students.append(person)
	return students


def matchMake(path, students, mentors):
	# timeDemand = {'6:30 - 7:00 pm': 0, '7:00 - 7:30 pm': 0, '7:30 - 8:00 pm': 0}
	# timeSupply = {'6:30 - 7:00 pm': 0, '7:00 - 7:30 pm': 0, '7:30 - 8:00 pm': 0}
	oldMentors = deepcopy(mentors)
	oldStudents = deepcopy(students)
	while True:
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
				if m['count'] < 2:
					found = verifyMatch(s, m)
					if found > 0:
						score += found
						break
		output = True
		for s in students:
			if s['mentor'] == 'None':
				output = False
		if output:
			with open(path + '/results/results' + str(score) + '.txt', 'w') as outfile:
				outfile.write(str(score))
				outfile.write('\n---\n')
				for s in students:
					outfile.write(s['name'] + ': ' + s['mentor'] + ': ' + s['time'])
					outfile.write('\n')
				for m in mentors:
					outfile.write(m['name'] + ': ' + str(m['count']))
					outfile.write('\n')
				outfile.write('\n')


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
		for a in student['areas']:
			if a in mentor['areas']:
				score += 1
				found = True
	if found:
		student['mentor'] = mentor['name']
		student['time'] = matches[0]
		mentor['count'] += 1
	return score


def main():
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