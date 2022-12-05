ROBOCODE - MAXIMAZING HITS

LEARNING MODE

1.	First set in robocodeAIServer.py variable learning_mode=True
2.	Start robocodeAIServer.py	
3.	Start robocode API
4.	Select oponent robots and MyRobotScan (this robot collects data)
5.	Start battle

TRAINING MODE

1.	Set dataset and keras model name in train_model.py
1.1.	You can change number of epochs, batch size, validation split (0-1)
2.	Start train_model.py

APPLYING OF TRAINED DATA

1.	Change variable to learning_mode=False in robocodeAIServer.py
2.	Start robocodeAIServer.py again
3.	Start robocode API
4.	Select MyRobotLearn and its oponents
5. 	Start battle 
 