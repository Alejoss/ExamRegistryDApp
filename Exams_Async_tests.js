const Exam = artifacts.require("Exams");

contract("Exams", async accounts => {

    it("should pass this test", async () => {
        assert.equal("0", "0", "LOGICAL!")
    });

    it("should add an exam to the exams list", async () => {
        // This should test the complete functionality
        let hash_test = "9F86D081884C7D659A2FEAA0C55AD015A3BF4F1B2B0B822CD15D6C15B0F00A08";
        let instance = await Exam.deployed();
        let hash = await instance.addExam(hash_test, {from: accounts[0]});
        console.log("LA PUTA MADRE PENDEJADA:");
        console.log(hash.valueOf());
        assert.equal(hash.valueOf(), hash_test, "Not returning the correct address");

        let is_owner = await instance.isOwner(hash_test, {from: accounts[0]});
        assert.equal(hash.valueOf(), "true", "Not recognizing hash correctly");

        let is_not_owner = await instance.isOwner("anotherhashabc123", {from: accounts[0]});
        assert.equal(hash.valueOf(), "false", "Not recognizing hash correctly");
    });

    it("Should add an student address to the people that passed the exam", async () => {
        let student_address = accounts[1];
        let instance = await Exam.deployed();
        let examProfessorHash = instance.getProfessorsExam({from: accounts[0]});
        let examProfessorHash2 = instance.studentAddExam(student_address, {from: accounts[0]});
        assert.equal(examProfessorHash2.valueOf(), examProfessorHash, "There was a problem saving the student's exam");

        let studentPassedExam = instance.checkStudentPassedExam(examProfessorHash, {from: student_address});
        assert.equal(studentPassedExam.valueOf(), "true", "There was a problem chacking the student hash / exam")
    });
   });
