import NeuralNetwork
import pickle

NeuralNet = NeuralNetwork.NeuralNetwork()
NeuralNet.resetNeurons()
NeuralNet.loadDataTable("MSFT.csv")
NeuralNet.train()
print("1/3 Complete")
NeuralNet.loadDataTable("CVX.csv")
NeuralNet.train()
print("2/3 Complete")
NeuralNet.loadDataTable("WMT.csv")
NeuralNet.train()
print("3/3 Complete")
ai = open("StockAI.ai",'wb')
pickle.dump(NeuralNet,ai)
print("Finished and AI saved")