pragma solidity ^0.5.0;


contract SocialNetwork {
	string public name;
	uint public postCount = 0;

	mapping (uint => Post) public posts;
	struct Post {
		uint id;
		string content;
		uint tipAmount;
		address payable author;
		string ipfsHash;
		
	}
    
	event PostCreated(
        uint id,
        string content,
        uint tipAmount,
        address payable author,
        string ipfsHash
    );
	
	event PostTipped(
        uint id,
        string content,
        uint tipAmount,
        address payable author,
        string ipfsHash
    );

    event Transfer(address payable _from, address payable _to, uint256 _value);
	

	function createPost(string memory _content,string memory _ipfsHash) public{
		
		require (bytes(_content).length>0);
		postCount++;
        posts[postCount] = Post(postCount, _content, 0, msg.sender,_ipfsHash);
		emit PostCreated(postCount,_content,0,msg.sender,_ipfsHash);
	}

	function tipPost(uint _id) public payable {
        require(_id > 0 && _id <= postCount);
        Post memory _post = posts[_id];
        address payable _author = _post.author;
        address(_author).transfer(msg.value);
        _post.tipAmount = _post.tipAmount + msg.value;
        posts[_id] = _post;
        emit PostTipped(postCount, _post.content, _post.tipAmount, _author,_post.ipfsHash);
    }

    function moneyTransfer(address payable _author) public payable {
            if(msg.sender.balance >= msg.value){
            address(_author).transfer(msg.value);
            emit Transfer(msg.sender,_author,msg.value);
            }
    }
    
	
}


