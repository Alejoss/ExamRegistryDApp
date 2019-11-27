pragma solidity >=0.4.22 <0.6.0;


contract Exams {
    
    address contractOwner;
    string examsFinalHash;
    mapping(address => string) professorsExam;

    struct Exam {
        mapping(address => bool) examSuccess;
    }

    mapping(string => Exam) examHash;


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

    function studentAddExam(address studentAddress) public returns (string memory hash){
        // Receives a student's address and adds it to the people that passed that exam
        // Only the creator of the exam can do this
        string memory professorsExamHash = professorsExam[msg.sender];  // The hash of the exam owned by msg.sender
        if(bytes(professorsExamHash).length == 0){
            return "No exam hash asociated with this professor address";
        }
        Exam storage examObj = examHash[professorsExamHash];  // Get the correct Exam struct
        examObj.examSuccess[studentAddress] = true;  // updates the examSuccess mapping with the student hash pointing to true
        return (professorsExamHash);
    }

    function checkStudentExam(string memory examCheckHash) public view returns (string memory hash){
        // Receives an Exam Hash and checks weather message.sender is recorded as having completed that exam
        Exam storage examObj = examHash[examCheckHash];
        if (examObj.examSuccess[msg.sender] == true){
            return examCheckHash;
        } else {
            return "Student address not recorded as having passed the exam";
        }
    }
}
