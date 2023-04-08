from sklearn.externals import joblib



nomePred = input("Digite modelo do Preditor\n");
preditor = joblib.load(nomePred+'.pkl')
scalator = joblib.load('Scaler_'+nomePred+'.pkl')
while(True):
	original = input("Qntd Core ORIGINAIS\n");
	ip = input("Qntd Core IP\n");
	total = int(original)+int(ip)
	print("TOTAL: ", total)
	teste = [[original,ip,total]]

	testeS = scalator.transform(teste)
	print("\nCaso de Teste: ", testeS)
	resp = preditor.predict(testeS)
	print("\nresp: ", resp)
