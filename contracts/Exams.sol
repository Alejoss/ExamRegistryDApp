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

        return professorsExam[msg.sender];
    }

    function isOwner(string memory hash) public view returns (bool) {
        // Receives an exam's hash and compares it to see if it belongs to msg.sender
        if(keccak256(abi.encodePacked(professorsExam[msg.sender])) == keccak256(abi.encodePacked(hash))){
            return true;
        } else {
            return false;
        }
    }

    function getProfessorsExam() public view returns (string memory examProfessorHash){
        return professorsExam[msg.sender];
    }

    function studentAddExam(address studentAddress) public returns (string memory returnString){
        // Receives a student's address and adds it to the people that passed that exam
        // Only the creator of the exam can do this
        string memory professorsExamHash = professorsExam[msg.sender];  // The hash of the exam owned by msg.sender
        Exam storage examObj = examHash[professorsExamHash];
        examObj.examSuccess[studentAddress] = true;
        return professorsExamHash;
    }

    function checkStudentPassedExam(string memory examProfessorHash) public view returns (bool){
        // Checks if the msg.sender passed the exam from the examProfessorHash
        Exam storage examObj = examHash[examProfessorHash];
        bool studentPassedExam = examObj.examSuccess[msg.sender];
        return (studentPassedExam);
    }
}
