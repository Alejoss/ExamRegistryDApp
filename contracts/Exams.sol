pragma solidity >=0.4.22 <0.6.0;


contract Exams {
    
    address contractOwner;
    string examsFinalHash;
    mapping(address => string) professorsExam;
    
    struct Exam {
        mapping(string => bool) examSuccess;
    }
    
    mapping(string => Exam) examHash;

    function getContractOwner() public pure returns (string memory contractOwnerAddress) {
        return "0x67F4CfB03aA5E2E71De1470ae26adB7e33B7892E";
    }

    constructor () public {
        contractOwner = msg.sender;
    }
    
    modifier onlyOwner () {
        require(contractOwner == msg.sender);
        _;
    }
    
    
    function addExam(string memory hash) public returns (string memory examProfessorHash) {
        // save the exam hash and link it with the professors address
        professorsExam[msg.sender] = hash;
        
        return hash;
    }
    
    function isOwner(string memory hash) public view returns (bool) {
        // Receives an exam's hash and compares it to see if it belongs to msg.sender
        if(keccak256(abi.encodePacked(professorsExam[msg.sender])) == keccak256(abi.encodePacked(hash))){
            return true;
        } else {
            return false;
        }
    }
    
    function studentAddExam(string memory hash) public view returns (bool){
        // Receives a student's address and adds it to the people that passed that exam
        // Only the creator of the exam can do this
        string memory professorsExamHash = professorsExam[msg.sender];  // The hash of the exam owned by msg.sender
        Exam storage examObj = examHash[professorsExamHash];
        bool studentPassedExam = examObj.examSuccess[hash];
        return (studentPassedExam);
    }
}

