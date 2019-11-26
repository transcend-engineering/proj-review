import os, random, signal
from copy import deepcopy
from csv import DictReader
from operator import itemgetter

"""
Editable parameters
"""

NAME_MENTOR = 'Your name (First and Last)'
TIME_MENTOR = 'Time Slot(s) You Can Mentor'
AREA_MENTOR = 'Areas/Industries you\'re interested in hearing about and giving feedback on. (Select all that apply)'
EMAIL_MENTOR = 'Email Address'

NAME_STUDENT = 'Your First and Last Name'
TIME_STUDENT = 'Time Slot(s) You Can Attend'
AREA_STUDENT = 'What areas/industries you need help with specifically? (Select all that apply)'
EMAIL_STUDENT = 'You and your team\'s email addresses'

MAX_STUDENTS_PER_MENTOR = 2

SIGKILL = True


def signalHandler(sig, frame):
	global SIGKILL
	print('\nRandom Matching Algorithm ending...')
	SIGKILL = False


def loadMentors(path):
	"""
	:param path: path to file
	:return: mentor list of dictionaries
	"""
	mentors = []

	with open(path) as infile:
		read = DictReader(infile)
		
		for row in read:
			person = {'name':'', 'times':[], 'areas':[], 'tcount':0, 'acount':0, 'count':0, 'email':''}
			person['name'] = row[NAME_MENTOR]
			person['times'] = row[TIME_MENTOR].split(', ')
			person['tcount'] = len(person['times'])
			person['areas'] = row[AREA_MENTOR].split(', ')
			person['acount'] = len(person['areas'])
			person['email'] = row[EMAIL_MENTOR]
			mentors.append(person)

	return mentors


def loadStudents(path):
	"""
	:param path: path to file
	:return: mentor list of dictionaries
	"""
	students = []

	with open(path) as infile:
		read = DictReader(infile)

		for row in read:
			person = {'name':'', 'times':[], 'areas':[], 'tcount':0, 'acount':0, 'mentor':'None', 'email':'', 'mentoremail':'None'}
			person['name'] = row[NAME_STUDENT]
			person['times'] = row[TIME_STUDENT].split(', ')
			person['tcount'] = len(person['times'])
			person['areas'] = row[AREA_STUDENT].split(', ')
			person['acount'] = len(person['areas'])
			person['email'] = row[EMAIL_STUDENT]
			students.append(person)

	return students


def printResults(path, score, students, mentors):
	"""
	:param path: current directory path
	:param score: weighted score of matching
	:param students: student list of dictionaries
	:param mentors: mentor list of dictionaries
	"""
	outfilename = str(score) + '.txt'
	print('Matching Found: results{}.txt'.format(str(score)))

	with open(path + '/results/results{}'.format(outfilename), 'w') as outfile:
		outfile.write(str(score))
		outfile.write('\n-----\n')

		for s in students:
			if s['mentor'] == 'None':
				outfile.write('{:25} | {:14} | {:25} | {:40} | {:100}'.format(s['mentor'], 'No Time Avail ', s['name'], s['mentoremail'], s['email']))
			else:
				outfile.write('{:25} | {:14} | {:25} | {:40} | {:100}'.format(s['mentor'], s['time'], s['name'], s['mentoremail'], s['email']))
			outfile.write('\n')

		outfile.write('Counts\n-----\n')

		for m in mentors:
			outfile.write('{:25} | {:1}'.format(m['name'], m['count']))
			outfile.write('\n')

		outfile.write('\n')


def matchMake(path, students, mentors):
	"""
	:param path: current directory path
	:param students: student list of dictionaries
	:param mentors: mentor list of dictionaries
	"""
	oldMentors = deepcopy(mentors)
	oldStudents = deepcopy(students)

	while SIGKILL:
		score = 0
		students = deepcopy(oldStudents)
		random.shuffle(students)
		mentors = deepcopy(oldMentors)

		for s in students:
			random.shuffle(mentors)

			for m in mentors:
				if m['count'] <= MAX_STUDENTS_PER_MENTOR:
					found = verifyMatch(s, m)
					if found > 0:
						score += found
						break

		printResults(path, score, students, mentors)



def verifyMatch(student, mentor):
	"""
	:param student: student dictionary
	:param mentor: mentor dictionary
	:return: weighted score of matching
	"""
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
	signal.signal(signal.SIGINT, signalHandler)
	path = os.getcwd()
	mentor_file = 'MentorSignup.csv'
	student_file = 'StudentSignup.csv'
	mentors = loadMentors(os.path.join(path, mentor_file))
	students = loadStudents(os.path.join(path, student_file))
	students = sorted(students, key=itemgetter('tcount', 'acount'))
	matchMake(path, students, mentors)


if __name__ == '__main__':
	main()