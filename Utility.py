import os
#updates settings function, pass the name of the setting and the value
def updateSettings(setting,value):
	data = []
	with open(os.getcwd()+"\\Settings\\Settings.txt","a+") as f:
		f.seek(0)
		data = f.readlines()
		valueExists = False
		for i in range(0,len(data)):
			data[i] = data[i].strip("\n")
			temp = data[i].split(":")
			#once the setting is found it gets split based on ':'
			#temp[0] is always the setting name
			#anything with a greater index than 0 is part of the value
			if temp[0] == setting:
				valueExists = True
				if len(temp) == 2:
					temp[1] = value
				else:
					temp = [temp[0],value]
				temp = ":".join(temp)
				data[i] = temp
		#if the setting doesn't exist it gets appended to the list
		if not valueExists:
			data.append(setting + ":" + value)
		f.close()
	#updates contents of the file
	with open(os.getcwd()+"\\Settings\\Settings.txt","w+") as f:
		f.write("\n".join(data))
		f.close()
#retrieves the value associated with the setting
def getSetting(setting):
	with open(os.getcwd()+"\\Settings\\Settings.txt","a+") as f:
		f.seek(0)
		for line in f:
			temp = line.strip("\n")
			#turns temp into an array
			temp = temp.split(":")
			if temp[0] == setting:
				#anything in the temp array with an index > 0 is part of the value
				#since the values were split up with ':' we rejoin them with ':'
				return ":".join(temp[1:])
		f.close()
	return ""