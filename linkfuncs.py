import sqlite3
import datetime
from pytz import timezone

# Set Local timezone
tz = timezone("Asia/Kolkata")

link = sqlite3.connect("timelink.db")

# Returning List Values instead of Rows
def list_factory(cursor, row):
    lst = []
    for idx, col in enumerate(cursor.description):
        lst.append(row[idx])
    return lst

link.row_factory = list_factory
#--------------------------------------
cursor = link.cursor()

def currentLink(day,time):
    with link:
        cursor.execute("""  SELECT link FROM idlink
                            INNER JOIN timetable
                            ON timetable.class_id = idlink.class_id
                            WHERE timetable.weekday = :day AND timetable.hour = :hour; """,
                            {'day':day,'hour':time})

        class_link = cursor.fetchall()
        
        if len(class_link) == 1:
            return class_link
        else:
            return None

def nameToLink(name):
	with link:
		cursor.execute("""	SELECT idlink.link,idname.class_name,idname.code FROM idname
							INNER JOIN idlink ON idlink.class_id = idname.class_id
							INNER JOIN enum ON enum.class_name = idname.class_name
							WHERE enum.nickname = :nickname LIMIT 1;""",{'nickname':name})

		class_info = cursor.fetchall()

		if len(class_info) == 1:
			return class_info[0]
		else:
			return [None,None,None]

def getlivechannels():
	cursor.execute("""SELECT channel_id FROM live_channels""")
	channels = cursor.fetchall()
	flat_list = [item for sublist in channels for item in sublist]
	return flat_list
	
	
def channelsupdate(channel_id):
	cursor.execute("""	SELECT channel_id FROM live_channels
						WHERE channel_id = :idchannel""",{'idchannel':channel_id})	
	if_exists = cursor.fetchall()
	print(if_exists)
	if if_exists == []:
		with link:
			cursor.execute("""	INSERT INTO live_channels
								VALUES (:idchannel) """,
								{'idchannel':channel_id})
		return 1
	else:
		with link:
			cursor.execute("""	DELETE FROM live_channels
								WHERE channel_id = :idchannel""",{'idchannel':channel_id})
			link.commit()
		return 0

def checkCHannel():
	cursor.execute("""SELECT * FROM live_channels""")
	print(cursor.fetchall())

def updateLink(class_code,limk):

	cursor.execute(""" SELECT class_id FROM idname
						WHERE code LIKE :txt""",{'txt':class_code})

	class_info = cursor.fetchone()
	if class_info != [] and class_info != None:
		class_info = class_info[0]
		print(class_info)
		with link:
			cursor.execute("""UPDATE idlink SET link = :lnk
								WHERE class_id = :idclass""",
								{'lnk':limk,'idclass':class_info})
			cursor.fetchall()
			cursor.execute("""SELECT link FROM idlink
							WHERE class_id = :idclass""",
							{'idclass':class_info})
			print(cursor.fetchall())
			link.commit()
		return 1
	return 0


def currentClassCodeName(day,time):
	with link:
		cursor.execute("""  SELECT code,class_name FROM idname
		INNER JOIN timetable
		ON timetable.class_id = idname.class_id
		WHERE timetable.weekday = :day AND timetable.hour = :hour;  """,
		{'day':day,'hour':time})

		class_info = cursor.fetchall()
		print(class_info)

		if len(class_info) == 1:
			return class_info
		else:
			return [None,None]

def currentCodeLink(day,time):
	class_link = currentLink(day,time)
	if class_link != [] and class_link != None:
		class_link = class_link[0][0]
		classCodeName = currentClassCodeName(day,time)
		class_code = classCodeName[0][0]
		class_name = classCodeName[0][1]
		print(class_code,class_name)
		return [class_link,class_code,class_name]
	else:
		return [None,None,None]

def liveClassCodeLink():
    livetime = datetime.datetime.now(tz)
    weekday = datetime.date.weekday(livetime)
    hour = livetime.hour
    minutes = livetime.minute

    if minutes >= 45:
        hour += 1

    return currentCodeLink(weekday,hour)

def periodicClassLink():
	livetime = datetime.datetime.now(tz)
	weekday = datetime.date.weekday(livetime)
	hour 	= livetime.hour
	minutes = livetime.minute

	if minutes >= 45 and minutes <= 59:
		hour += 1
		sets = currentCodeLink(weekday,hour)
		print(sets)
		if sets != None:
			return sets
		else:
			return [0,0,0]

def codeToLink(code):
    if len(code) == 5 and type(code) == str:
        with link:
            cursor.execute("""  SELECT link FROM idlink
                                INNER JOIN idname
                                ON idname.class_id = idlink.class_id
                                WHERE idname.code = code;  """,
                                {'code':code})

def todaySchedule():
	livetime = datetime.datetime.now(tz)
	weekday = datetime.date.weekday(livetime)

	with link:
		cursor.execute("""  SELECT class_name,timetable.hour FROM idname
							INNER JOIN timetable
							ON timetable.class_id = idname.class_id
							WHERE timetable.weekday = :day; """,
							{'day': weekday})

		dayData = cursor.fetchall()
		if len(dayData) < 3:
			return None

		timeCorrected = sorted(dayData, key = lambda x: x[1])

		return timeCorrected