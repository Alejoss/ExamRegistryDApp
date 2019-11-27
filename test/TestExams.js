const Exam = artifacts.require("Exams");

contract("Exams", async accounts => {

    it("should pass this test", async () => {
        assert.equal("0", "0", "LOGICAL!")
    });


    it("should add an exam to the exams list", async () => {
        // This should test the complete functionality
        let hash_test = "fB03aA5E2E71De1470ae2";
        let instance = await Exam.deployed();
        let hash = instance.addExam(hash_test, {from: accounts[0]});
        assert.equal(hash.valueOf(), hash_test, "Not returning the correct address");

        let is_owner = instance.isOwner(hash_test, {from: accounts[0]});
        assert.equal(hash.valueOf(), "true", "Not recognizing hash correctly");

        let is_not_owner = instance.isOwner("anotherhashabc123", {from: accounts[0]});
        assert.equal(hash.valueOf(), "false", "Not recognizing hash correctly");
    });

    it("Should add an student address to the people that passed the exam", async () => {
        let student_address = "STUD3NT4ADD5E88ST3ST";
        let instance = await Exam.deployed();
        let hash = instance.addStudentExam(student_address, {from: accounts[0]});
        assert.equal(hash.valueOf(), student_address, "There was a problem saving the student's exam");

        let check_hash = instance.checkStudentExam(check_hash, {from: accounts[0]});
        assert.equal(hash.valueOf(), student_address, "There was a problem chacking the student hash / exam")
    });
   });
