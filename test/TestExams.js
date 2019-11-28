const Exam = artifacts.require("Exams");

contract("Exams", accounts => {

    it("should pass this test", async () => {
        assert.equal("0", "0", "LOGICAL!")
    });

    it("should add an exam to the exams list", () => {
        let hash_test = "9F86D081884C7D659A2FEAA0C55AD015A3BF4F1B2B0B822CD15D6C15B0F00A08";
        Exam.deployed()
            .then(instance => instance.addExam(hash_test, {from: accounts[0]}))
            .then(hash => {
                assert.equal(hash.valueOf(), hash_test, "Not returning the correct address");
            })
            .then(instance => instance.isOwner(hash_test, {from: accounts[0]}))
            .then(isOwner => {
                assert.equal(isOwner, "true", "Not recognizing hash correctly")
            })
            .then(instance => instance.isOwner("THISISWRONG", {from: accounts[0]}))
            .then(isOwner => {
                assert.equal(isOwner, "false", "Not recognizing hash correctly")
            });
    });

    it("Should add an student address to the people that passed the exam", () => {
        let student_address = accounts[1];
        let examPHash = "";  // to keep the exams hash
        Exam.deployed()
            .then(instance => instance.getProfessorsExam({from: accounts[0]}))
            .then(examProfessorHash => {
                examPHash = examProfessorHash
            })
            .then(instance => instance.studentAddExam(student_address, {from: accounts[0]}))
            .then(examProfessorHash2 => {
                assert.equal(examPHash, examProfessorHash2, "There was a problem saving the student's exam")
            })
            .then(instance => instance.checkStudentPassedExam(examPHash, {from: student_address}))
            .then(studentPassedExam => {
                assert.equal(studentPassedExam.valueOf(), "true", "There was a problem chacking the student hash / exam")
            })
    })
   });
