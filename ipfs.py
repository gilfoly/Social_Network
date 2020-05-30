import ipfsApi

api = ipfsApi.Client('https://ipfs.infura.io',5001)

def addFile(file):
	res = api.add(file)
	print(res)
	return res
