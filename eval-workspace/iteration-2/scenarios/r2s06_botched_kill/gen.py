open("data.bin","wb").write(bytes(range(256))*200000)
print("wrote data.bin ~51MB")
