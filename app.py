from flask import Flask,render_template,url_for,request,jsonify,flash,redirect
from interface import Data,moneyTransfer,createPost,tipPost
from ipfs import addFile

app = Flask(__name__)
app.secret_key = "abc"  

@app.route('/')
def home():
	posts,user,userBalance = Data()
	return render_template('Home.html',user=user)

@app.route('/posts')
def posts():
	posts,user,userBalance = Data()
	print(posts)
	return render_template('posts.html',posts=posts,user=user)

@app.route('/transaction')
def transaction():
	posts,user,userBalance = Data()
	return render_template('Transaction.html',balance=userBalance,user=user)

@app.route('/pay',methods=['POST','GET'])
def paytoreceiver():
	try:
		if request.method == 'POST': 
			receiver = request.form.get('receiver')
			money = request.form.get('money')
			moneyTransfer(receiver,money)
			posts,user,userBalance = Data()
			flash('Ether transfered sussesfully !','success')

			return redirect('transaction')
	except Exception as e:
		flash('Transaction Failed ','danger')
		return redirect('transaction')

@app.route('/sendPost',methods=['GET','POST'])
def uploadPost():
	try:
		if request.method == 'POST':
			userpost = request.form['userpost']
			userImage = request.form['InputFile']
			if userImage:
				ipfsHash = addFile(userImage)['Hash']
			else:
				ipfsHash =''
			createPost(userpost,ipfsHash)
			posts,user,userBalance = Data()
			flash('Post uploaded sussesfully !','success')

			return redirect(url_for('posts'))
	except Exception:
		flash('Post was not uploaded','danger')
		return redirect(url_for('posts'))

@app.route('/tip',methods=['GET','POST'])
def PostTipped():
	try:
		if request.method == 'POST':
			userid = int(request.form['userid'])
			tipPost(userid)
			posts,user,userBalance = Data()
			flash('Post tipped !','success')
			return redirect(url_for('posts'))
	except Exception:
		flash('Post was not monetized','danger')
		return redirect(url_for('posts'))

if __name__ == '__main__':
	app.run(debug=True)

