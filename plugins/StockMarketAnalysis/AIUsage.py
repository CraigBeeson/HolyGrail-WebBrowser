import datetime

def useAI(AI,data):
	data = processData(data)
	return AI.predict(data.iloc[len(data)-1].to_numpy())

def processData(data):
	data.insert(6, "Avg. Open/Close", 0.0)
	data.insert(7, "Avg. Open/Low", 0.0)
	data.insert(8, "Avg. Open/High", 0.0)
	data.insert(9, "Avg. Close/Low", 0.0)
	data.insert(10, "Avg. Close/High", 0.0)
	data.insert(11, "Avg. Open", 0.0)
	data.insert(12, "Avg. Close", 0.0)
	data.insert(13, "Avg. High", 0.0)
	data.insert(14, "Avg. Low", 0.0)
	data.insert(15, "Avg. Volume", 0)
	data.insert(16, "Day of Month", 0)
	data.insert(17, "Day of Week", 0)
	data.insert(18, "Week of Month", 0)
	data.insert(19, "Month of Year", 0)
	data.insert(20, "Week of Year", 0)
	data.insert(21, "Recent Ups", 0)
	data.insert(22, "Recent Downs", 0)
	data.insert(23, "Open SD", 0.0)
	data.insert(24, "Close SD", 0.0)
	data.insert(25, "High SD", 0.0)
	data.insert(26, "Low SD", 0.0)
	data.insert(27, "Volume SD", 0.0)
	data.insert(28, "Open/Close", 0.0)
	data.insert(29, "Open/Low", 0.0)
	data.insert(30, "Open/High", 0.0)
	data.insert(31, "Close/Low", 0.0)
	data.insert(32, "Close/High", 0.0)
	var0 = 0
	var1 = 0
	var2 = 0
	var3 = 0
	var4 = 0
	var5 = 0
	var6 = 0
	
	for i in range(len(data)-90,len(data)):
		temp = data["Date"][i].split('-')
		temp = datetime.date(int(temp[0]), int(temp[1]), int(temp[2])).toordinal()
		if data["Open"][i] < data["Close"][i]:
			var5 += 1
		else:
			var6 += 1
		var0 += data["Open"][i]
		var1 += data["Close"][i]
		var2 += data["High"][i]
		var3 += data["Low"][i]
		var4 += data["Volume"][i]
		data.loc[i,"Avg. Open"] = var0/90
		data.loc[i,"Avg. Close"] = var1/90
		data.loc[i,"Avg. High"] = var2/90
		data.loc[i,"Avg. Low"] = var3/90
		data.loc[i,"Avg. Volume"] = var4//90
		data.loc[i, "Open SD"] = data["Open"][i-90:i].std()
		data.loc[i, "Close SD"] = data["Close"][i-90:i].std()
		data.loc[i, "High SD"] = data["High"][i-90:i].std()
		data.loc[i, "Low SD"] = data["Low"][i-90:i].std()
		data.loc[i, "Volume SD"] = data["Volume"][i-90:i].std()
		
		data.loc[i,"Avg. Open/Close"] = data.loc[i, "Avg. Open"]/data.loc[i, "Avg. Close"]
		data.loc[i,"Avg. Open/Low"] = data.loc[i, "Avg. Open"]/data.loc[i, "Avg. Low"]
		data.loc[i,"Avg. Open/High"] = data.loc[i, "Avg. Open"]/data.loc[i, "Avg. High"]
		data.loc[i,"Avg. Close/Low"] = data.loc[i, "Avg. Close"]/data.loc[i, "Avg. Low"]
		data.loc[i,"Avg. Close/High"] = data.loc[i, "Avg. Close"]/data.loc[i, "Avg. High"]
		data.loc[i, "Day of Month"] = datetime.date.fromordinal(temp).day
		data.loc[i, "Day of Week"] = datetime.date.fromordinal(temp).weekday()
		data.loc[i, "Week of Month"] = datetime.date.fromordinal(temp).day // 7
		data.loc[i, "Month of Year"] = datetime.date.fromordinal(temp).month
		data.loc[i, "Week of Year"] = datetime.date.fromordinal(temp).isocalendar().week
		data.loc[i, "Recent Ups"] = var5
		data.loc[i, "Recent Downs"] = var6
		data.loc[i,"Open/Close"] = data.loc[i, "Open"]/data.loc[i, "Close"]
		data.loc[i,"Open/Low"] = data.loc[i, "Open"]/data.loc[i, "Low"]
		data.loc[i,"Open/High"] = data.loc[i, "Open"]/data.loc[i, "High"]
		data.loc[i,"Close/Low"] = data.loc[i, "Close"]/data.loc[i, "Low"]
		data.loc[i,"Close/High"] = data.loc[i, "Open"]/data.loc[i, "High"]
	data = data.drop("Date", axis = 1)
	data["Volume"] = data["Volume"].astype(float)
	data = data.drop("Adj Close", axis = 1)
	return data