import pandas
import tensorflow
import datetime
import numpy

#load training data
data0 = pandas.read_csv("WMT.csv")
data1 = pandas.read_csv("C.csv")
data2 = pandas.read_csv("JPM.csv")
data3 = pandas.read_csv("MSFT.csv")
data4 = pandas.read_csv("CL.csv")
data5 = pandas.read_csv("STT.csv")
data6 = pandas.read_csv("CI.csv")
data7 = pandas.read_csv("BK.csv")
data8 = pandas.read_csv("BAC.csv")
data9 = pandas.read_csv("WASH.csv")

#adjust data provided so that it gives us more info
def updateDataFrame(featureFrame):
	featureFrame.insert(6, "Avg. Open/Close", 0.0)
	featureFrame.insert(7, "Avg. Open/Low", 0.0)
	featureFrame.insert(8, "Avg. Open/High", 0.0)
	featureFrame.insert(9, "Avg. Close/Low", 0.0)
	featureFrame.insert(10, "Avg. Close/High", 0.0)
	featureFrame.insert(11, "Avg. Open", 0.0)
	featureFrame.insert(12, "Avg. Close", 0.0)
	featureFrame.insert(13, "Avg. High", 0.0)
	featureFrame.insert(14, "Avg. Low", 0.0)
	featureFrame.insert(15, "Avg. Volume", 0)
	featureFrame.insert(16, "Day of Month", 0)
	featureFrame.insert(17, "Day of Week", 0)
	featureFrame.insert(18, "Week of Month", 0)
	featureFrame.insert(19, "Month of Year", 0)
	featureFrame.insert(20, "Week of Year", 0)
	featureFrame.insert(21, "Recent Ups", 0)
	featureFrame.insert(22, "Recent Downs", 0)
	featureFrame.insert(23, "Open SD", 0.0)
	featureFrame.insert(24, "Close SD", 0.0)
	featureFrame.insert(25, "High SD", 0.0)
	featureFrame.insert(26, "Low SD", 0.0)
	featureFrame.insert(27, "Volume SD", 0.0)
	featureFrame.insert(28, "Open/Close", 0.0)
	featureFrame.insert(29, "Open/Low", 0.0)
	featureFrame.insert(30, "Open/High", 0.0)
	featureFrame.insert(31, "Close/Low", 0.0)
	featureFrame.insert(32, "Close/High", 0.0)
	var0 = 0
	var1 = 0
	var2 = 0
	var3 = 0
	var4 = 0
	var5 = 0
	var6 = 0
	
	for i in range(0,len(featureFrame)):
		temp = featureFrame["Date"][i].split('-')
		temp = datetime.date(int(temp[0]), int(temp[1]), int(temp[2])).toordinal()
		
		if i < 90:
			if featureFrame["Open"][i] < featureFrame["Close"][i]:
				var5 += 1
			else:
				var6 += 1
			var0 += featureFrame["Open"][i]
			var1 += featureFrame["Close"][i]
			var2 += featureFrame["High"][i]
			var3 += featureFrame["Low"][i]
			var4 += featureFrame["Volume"][i]
			if i == 0:
				featureFrame.loc[i,"Avg. Open"] = var0/1
				featureFrame.loc[i,"Avg. Close"] = var1/1
				featureFrame.loc[i,"Avg. High"] = var2/1
				featureFrame.loc[i,"Avg. Low"] = var3/1
				featureFrame.loc[i,"Avg. Volume"] = var4//1
			else:
				featureFrame.loc[i,"Avg. Open"] = var0/i
				featureFrame.loc[i,"Avg. Close"] = var1/i
				featureFrame.loc[i,"Avg. High"] = var2/i
				featureFrame.loc[i,"Avg. Low"] = var3/i
				featureFrame.loc[i,"Avg. Volume"] = var4//i
			featureFrame.loc[i, "Open SD"] = featureFrame["Open"][0:i].std()
			featureFrame.loc[i, "Close SD"] = featureFrame["Close"][0:i].std()
			featureFrame.loc[i, "High SD"] = featureFrame["High"][0:i].std()
			featureFrame.loc[i, "Low SD"] = featureFrame["Low"][0:i].std()
			featureFrame.loc[i, "Volume SD"] = featureFrame["Volume"][0:i].std()
		else:
			if featureFrame["Open"][i-90] < featureFrame["Close"][i-90]:
				var5 -= 1
			else:
				var6 -= 1
			if featureFrame["Open"][i] < featureFrame["Close"][i]:
				var5 += 1
			else:
				var6 += 1
			var0 -= featureFrame["Open"][i-90]
			var0 += featureFrame["Open"][i]
			var1 -= featureFrame["Close"][i-90]
			var1 += featureFrame["Close"][i]
			var2 -= featureFrame["High"][i-90]
			var2 += featureFrame["High"][i]
			var3 -= featureFrame["Low"][i-90]
			var3 += featureFrame["Low"][i]
			var4 -= featureFrame["Volume"][i-90]
			var4 += featureFrame["Volume"][i]
			featureFrame.loc[i,"Avg. Open"] = var0/90
			featureFrame.loc[i,"Avg. Close"] = var1/90
			featureFrame.loc[i,"Avg. High"] = var2/90
			featureFrame.loc[i,"Avg. Low"] = var3/90
			featureFrame.loc[i,"Avg. Volume"] = var4//90
			featureFrame.loc[i, "Open SD"] = featureFrame["Open"][i-90:i].std()
			featureFrame.loc[i, "Close SD"] = featureFrame["Close"][i-90:i].std()
			featureFrame.loc[i, "High SD"] = featureFrame["High"][i-90:i].std()
			featureFrame.loc[i, "Low SD"] = featureFrame["Low"][i-90:i].std()
			featureFrame.loc[i, "Volume SD"] = featureFrame["Volume"][i-90:i].std()
		
		featureFrame.loc[i,"Avg. Open/Close"] = featureFrame.loc[i, "Avg. Open"]/featureFrame.loc[i, "Avg. Close"]
		featureFrame.loc[i,"Avg. Open/Low"] = featureFrame.loc[i, "Avg. Open"]/featureFrame.loc[i, "Avg. Low"]
		featureFrame.loc[i,"Avg. Open/High"] = featureFrame.loc[i, "Avg. Open"]/featureFrame.loc[i, "Avg. High"]
		featureFrame.loc[i,"Avg. Close/Low"] = featureFrame.loc[i, "Avg. Close"]/featureFrame.loc[i, "Avg. Low"]
		featureFrame.loc[i,"Avg. Close/High"] = featureFrame.loc[i, "Avg. Close"]/featureFrame.loc[i, "Avg. High"]
		featureFrame.loc[i, "Day of Month"] = datetime.date.fromordinal(temp).day
		featureFrame.loc[i, "Day of Week"] = datetime.date.fromordinal(temp).weekday()
		featureFrame.loc[i, "Week of Month"] = datetime.date.fromordinal(temp).day // 7
		featureFrame.loc[i, "Month of Year"] = datetime.date.fromordinal(temp).month
		featureFrame.loc[i, "Week of Year"] = datetime.date.fromordinal(temp).isocalendar().week
		featureFrame.loc[i, "Recent Ups"] = var5
		featureFrame.loc[i, "Recent Downs"] = var6
		featureFrame.loc[i,"Open/Close"] = featureFrame.loc[i, "Open"]/featureFrame.loc[i, "Close"]
		featureFrame.loc[i,"Open/Low"] = featureFrame.loc[i, "Open"]/featureFrame.loc[i, "Low"]
		featureFrame.loc[i,"Open/High"] = featureFrame.loc[i, "Open"]/featureFrame.loc[i, "High"]
		featureFrame.loc[i,"Close/Low"] = featureFrame.loc[i, "Close"]/featureFrame.loc[i, "Low"]
		featureFrame.loc[i,"Close/High"] = featureFrame.loc[i, "Open"]/featureFrame.loc[i, "High"]
	
	featureFrame.fillna(0, inplace=True)
	
	return featureFrame

#add the extra values for the data frames
data0 = updateDataFrame(data0)
data1 = updateDataFrame(data1)
data2 = updateDataFrame(data2)
data3 = updateDataFrame(data3)
data4 = updateDataFrame(data4)
data5 = updateDataFrame(data5)
data6 = updateDataFrame(data6)
data7 = updateDataFrame(data7)
data8 = updateDataFrame(data8)
data9 = updateDataFrame(data9)

#features need to map to the labels, where the label is for the day after the feature
#so features start at the first entry and end before the last entry
#labels start on the  2nd entry and end on the last entry
trainingFeatures = pandas.concat([data0[0:len(data0)-2], data1[0:len(data1)-2], data2[0:len(data2)-2], data3[0:len(data3)-2], data5[0:len(data5)-2],
	data6[0:len(data6)-2], data7[0:len(data7)-2], data8[0:len(data8)-2], data9[0:len(data9)-2]],ignore_index = True)
trainingLabels = pandas.concat([data0[1:len(data0)-1], data1[1:len(data1)-1], data2[1:len(data2)-1], data3[1:len(data3)-1], data5[1:len(data5)-1],
	data6[1:len(data6)-1], data7[1:len(data7)-1], data8[1:len(data8)-1], data9[1:len(data9)-1]],ignore_index = True)
testFeatures = data4.copy()[0:len(data4)-2]
testLabels = data4.copy()[1:len(data4)-1]

#turn date to ordinal for a single integer value, outdated
for i in range(0,len(trainingFeatures)):
	date = trainingFeatures["Date"][i].split('-')
	date = datetime.date(int(date[0]), int(date[1]), int(date[2])).toordinal()
	trainingFeatures.loc[i,"Date"] = date

#drop data we dont use and convert integer 'volume' to float
trainingFeatures = trainingFeatures.drop("Date", axis = 1)
trainingFeatures["Volume"] = trainingFeatures["Volume"].astype(float)
trainingFeatures = trainingFeatures.drop("Adj Close", axis = 1)
trainingLabels["Volume"] = trainingLabels["Volume"].astype(float)
#only predicting these 4 values
trainingLabels = pandas.concat( [trainingLabels["Open"], trainingLabels["High"], trainingLabels["Low"], trainingLabels["Close"]], axis = 1)

#turn date to ordinal for a single integer value, outdated
for i in range(0,len(testFeatures)):
	date = testFeatures["Date"][i].split('-')
	date = datetime.date(int(date[0]), int(date[1]), int(date[2])).toordinal()
	testFeatures.loc[i,"Date"] = date

#drop data we dont use and convert integer 'volume' to float
testFeatures = testFeatures.drop("Date", axis = 1)
testFeatures["Volume"] = testFeatures["Volume"].astype(float)
testFeatures = testFeatures.drop("Adj Close", axis = 1)
testLabels["Volume"] = testLabels["Volume"].astype(float)
#only predicting these 4 values
testLabels = pandas.concat( [testLabels["Open"], testLabels["High"], testLabels["Low"], testLabels["Close"]], axis = 1)

#create numpy arrays
trainingFeatures = numpy.array(trainingFeatures)
trainingLabels = numpy.array(trainingLabels)
testFeatures = numpy.array(testFeatures)
testLabels = numpy.array(testLabels)

#model
normalize = tensorflow.keras.layers.Normalization()
normalize.adapt(trainingFeatures)
stockModel = tensorflow.keras.Sequential([
	normalize,
	tensorflow.keras.layers.Dense(256, kernel_regularizer=tensorflow.keras.regularizers.l2(0.001)),
	tensorflow.keras.layers.Dense(256, kernel_regularizer=tensorflow.keras.regularizers.l2(0.001)),
	tensorflow.keras.layers.Dense(256, kernel_regularizer=tensorflow.keras.regularizers.l2(0.001)),
	tensorflow.keras.layers.Dense(256, kernel_regularizer=tensorflow.keras.regularizers.l2(0.001)),
	tensorflow.keras.layers.Dense(256, kernel_regularizer=tensorflow.keras.regularizers.l2(0.001)),
	tensorflow.keras.layers.Dense(256, kernel_regularizer=tensorflow.keras.regularizers.l2(0.001)),
	tensorflow.keras.layers.Dense(256, kernel_regularizer=tensorflow.keras.regularizers.l2(0.001)),
	tensorflow.keras.layers.Dense(4)
])

stockModel.compile(loss = tensorflow.keras.losses.MeanSquaredError(), optimizer = tensorflow.keras.optimizers.Adam(learning_rate = .00003), metrics = ['mae'])
stockModel.fit(trainingFeatures, trainingLabels, epochs=3000,validation_data = (testFeatures,testLabels),
	batch_size = 32)
stockModel.summary()
stockModel.save("AI/Stock.ai")
