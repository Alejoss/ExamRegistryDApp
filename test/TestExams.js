const Exam = artifacts.require("Exams");

contract("Exams", async accounts => {
   it("should pass this test", async () => {
        assert.equal("0", "0", "LOGICAL!")
    });

   it("should keep the contract owner", async () => {
   let instance = await Exam.deployed();
   let address = await instance.getContractOwner.call({from: accounts[0]});
   // console.log(address);
   assert.equal(address.valueOf(), "0x67F4CfB03aA5E2E71De1470ae26adB7e33B7892E", "the address is not correct");
   });

    it("should add an exam to the exams list", async () => {
        // This should test the complete functionality
        let hash_test = "fB03aA5E2E71De1470ae2";
        let instance = await Exam.deployed();
        let hash = instance.addExam(hash_test).call({from: accounts[0]});
        assert.equal(hash.valueOf(), hash_test, "Not returning the correct address")
    })
   });
