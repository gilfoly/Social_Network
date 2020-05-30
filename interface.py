from web3 import Web3
import json

ganache_url = 'http://127.0.0.1:8545'

web3 = Web3(Web3.HTTPProvider(ganache_url))
print('Ganache is connected :',web3.isConnected())


accounts = web3.eth.accounts
user = web3.eth.accounts[0] 

abi = json.loads('[{"constant":true,"inputs":[],"name":"name","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"posts","outputs":[{"name":"id","type":"uint256"},{"name":"content","type":"string"},{"name":"tipAmount","type":"uint256"},{"name":"author","type":"address"},{"name":"ipfsHash","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"postCount","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_content","type":"string"},{"name":"_ipfsHash","type":"string"}],"name":"createPost","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_author","type":"address"}],"name":"moneyTransfer","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"constant":false,"inputs":[{"name":"_id","type":"uint256"}],"name":"tipPost","outputs":[],"payable":true,"stateMutability":"payable","type":"function"},{"anonymous":false,"inputs":[{"indexed":false,"name":"id","type":"uint256"},{"indexed":false,"name":"content","type":"string"},{"indexed":false,"name":"tipAmount","type":"uint256"},{"indexed":false,"name":"author","type":"address"},{"indexed":false,"name":"ipfsHash","type":"string"}],"name":"PostCreated","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"id","type":"uint256"},{"indexed":false,"name":"content","type":"string"},{"indexed":false,"name":"tipAmount","type":"uint256"},{"indexed":false,"name":"author","type":"address"},{"indexed":false,"name":"ipfsHash","type":"string"}],"name":"PostTipped","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"_from","type":"address"},{"indexed":false,"name":"_to","type":"address"},{"indexed":false,"name":"_value","type":"uint256"}],"name":"Transfer","type":"event"}]')
address = web3.toChecksumAddress('0x942b738eddc3a5cdb881cc535971ae325b5f1dbf')

SocialNetwork = web3.eth.contract(address=address,abi=abi)

name = SocialNetwork.functions.name().call()
print(name)

def createPost(content,ipfsHash):
	tx_hash = SocialNetwork.functions.createPost(content,ipfsHash).transact({
		'from': user
		})
	tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)

def tipPost(id):
	tx_hash = SocialNetwork.functions.tipPost(id).transact({
		'from': user,
		'value': web3.toWei(0.1,'ether')
		})
	tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)

def moneyTransfer(receiver,amount):
	tx_hash = SocialNetwork.functions.moneyTransfer(receiver).transact({
		'from': user,
		'value': web3.toWei(amount,'ether')
		})
	tx_receipt = web3.eth.waitForTransactionReceipt(tx_hash)

def Data():
	postCount = SocialNetwork.functions.postCount().call() 
	posts=[]
	for i in range(1,postCount+1):
		post = SocialNetwork.functions.posts(i).call()
		posts.append(post)
	posts = sorted(posts,key = lambda x: x[2], reverse = True)
	userBalance = web3.fromWei(web3.eth.getBalance(user),'ether')

	return posts,user,userBalance
try:
	moneyTransfer('0x9CA0CdA18a156d4DdAc1Ec70c11650d9B645D894',110)
	print('1')
except Exception:
	print('Transaction unsuccessfully')