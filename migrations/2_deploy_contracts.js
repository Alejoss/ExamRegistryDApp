var Exams = artifacts.require("../contracts/Exams.sol");

module.exports = function(deployer){
    deployer.deploy(Exams);
};
