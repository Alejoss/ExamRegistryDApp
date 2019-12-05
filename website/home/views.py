from django.shortcuts import render
import hashlib
import json
from web3 import Web3, HTTPProvider
from django.shortcuts import render, redirect
from django.http import HttpResponse

# Create your views here.
from home.models import Exam, Professor
from home.utils import setup_conection


def home(request):
    template = "home.html"
    professors = Professor.objects.all()
    for p in professors:
        if not p.exam:
            e = Exam.objects.create(hash="na")
            p.exam = e
            p.save()

    context = {'professors': professors}
    return render(request, template, context)


def exams_index(request, exam_id):
    template = "exams.html"
    exam = Exam.objects.get(id=exam_id)
    professor = Professor.objects.get(user=request.user)
    context = {'exam': exam, 'professor': professor}
    return render(request, template, context)


def edit_exam(request):
    template = "edit_exam.html"
    if request.method == "POST":
        q1 = request.POST.get("question1")
        q2 = request.POST.get("question2")
        q3 = request.POST.get("question3")
        q4 = request.POST.get("question4")
        q5 = request.POST.get("question5")
        q6 = request.POST.get("question6")
        q7 = request.POST.get("question7")
        q8 = request.POST.get("question8")
        q9 = request.POST.get("question9")
        q10 = request.POST.get("question10")
        professor = Professor.objects.get(user=request.user)
        exam = professor.exam
        exam.q1 = q1
        exam.q2 = q2
        exam.q3 = q3
        exam.q4 = q4
        exam.q5 = q5
        exam.q6 = q6
        exam.q7 = q7
        exam.q8 = q8
        exam.q9 = q9
        exam.q10 = q10
        exam.hash = hashlib.sha3_256((q1 + q2 + q3 + q4 + q5 + q6 + q7 + q8 + q9 + q10).encode('utf-8')).hexdigest()
        exam.save()

        # Conect to the blockchain, edit the professors exam hash
        w3, contract = setup_conection()
        tx_hash = contract.functions.addExam("watevs").transact()
        print(tx_hash)

        return redirect('exams', exam_id=professor.exam.id)

    else:
        # Get the professor actual exam
        if request.user.is_authenticated:
            current_user = request.user
            professor = Professor.objects.get(user=current_user)
            return render(request, template, {'professor': professor, 'exam': professor.exam})
        else:
            return HttpResponse("You need to login to create an exam")


def add_student(request):
    template = "add_student.html"
    professor = Professor.objects.get(user=request.user)
    if request.method == "POST":
        student_address = request.POST.get("student_address")
        # Send student address to the blockchain
        w3, contract = setup_conection()
        tx_hash = contract.functions.studentAddExam(student_address).transact()
        print(tx_hash)
    else:
        context = {"exam": professor.exam}
        return render(request, template, context)


def check_student_passed(request):
    pass

def test_contract(request):
    w3 = Web3(HTTPProvider('http://127.0.0.1:7545'))

    # contract_dir = os.path.abspath('./contracts/')
    abi = json.loads(
        '[{"constant":false,"inputs":[{"internalType":"address","name":"studentAddress","type":"address"}],"name":"studentAddExam","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"internalType":"string","name":"examProfessorHash","type":"string"}],"name":"checkStudentPassedExam","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"internalType":"string","name":"hash","type":"string"}],"name":"isOwner","outputs":[{"internalType":"bool","name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"internalType":"string","name":"hash","type":"string"}],"name":"addExam","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"getProfessorsExam","outputs":[{"internalType":"string","name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"}]')
    bytecode = "608060405234801561001057600080fd5b50336000806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055506109cb806100606000396000f3fe608060405234801561001057600080fd5b50600436106100575760003560e01c80633c9a1c391461005c578063acc600b514610119578063b85e943d146101ec578063db874295146102bf578063e7624d541461037a575b600080fd5b61009e6004803603602081101561007257600080fd5b81019080803573ffffffffffffffffffffffffffffffffffffffff1690602001909291905050506103fd565b6040518080602001828103825283818151815260200191508051906020019080838360005b838110156100de5780820151818401526020810190506100c3565b50505050905090810190601f16801561010b5780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b6101d26004803603602081101561012f57600080fd5b810190808035906020019064010000000081111561014c57600080fd5b82018360208201111561015e57600080fd5b8035906020019184600183028401116401000000008311171561018057600080fd5b91908080601f016020809104026020016040519081016040528093929190818152602001838380828437600081840152601f19601f8201169050808301925050505050505091929192905050506105ab565b604051808215151515815260200191505060405180910390f35b6102a56004803603602081101561020257600080fd5b810190808035906020019064010000000081111561021f57600080fd5b82018360208201111561023157600080fd5b8035906020019184600183028401116401000000008311171561025357600080fd5b91908080601f016020809104026020016040519081016040528093929190818152602001838380828437600081840152601f19601f820116905080830192505050505050509192919290505050610676565b604051808215151515815260200191505060405180910390f35b610378600480360360208110156102d557600080fd5b81019080803590602001906401000000008111156102f257600080fd5b82018360208201111561030457600080fd5b8035906020019184600183028401116401000000008311171561032657600080fd5b91908080601f016020809104026020016040519081016040528093929190818152602001838380828437600081840152601f19601f8201169050808301925050505050505091929192905050506107bb565b005b610382610812565b6040518080602001828103825283818151815260200191508051906020019080838360005b838110156103c25780820151818401526020810190506103a7565b50505050905090810190601f1680156103ef5780820380516001836020036101000a031916815260200191505b509250505060405180910390f35b606080600260003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000208054600181600116156101000203166002900480601f0160208091040260200160405190810160405280929190818152602001828054600181600116156101000203166002900480156104d35780601f106104a8576101008083540402835291602001916104d3565b820191906000526020600020905b8154815290600101906020018083116104b657829003601f168201915b5050505050905060006003826040518082805190602001908083835b6020831061051257805182526020820191506020810190506020830392506104ef565b6001836020036101000a0380198251168184511680821785525050505050509050019150509081526020016040518091039020905060018160000160008673ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060006101000a81548160ff0219169083151502179055508192505050919050565b6000806003836040518082805190602001908083835b602083106105e457805182526020820191506020810190506020830392506105c1565b6001836020036101000a0380198251168184511680821785525050505050509050019150509081526020016040518091039020905060008160000160003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060009054906101000a900460ff1690508092505050919050565b6000816040516020018082805190602001908083835b602083106106af578051825260208201915060208101905060208303925061068c565b6001836020036101000a03801982511681845116808217855250505050505090500191505060405160208183030381529060405280519060200120600260003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200190815260200160002060405160200180828054600181600116156101000203166002900480156107875780601f10610765576101008083540402835291820191610787565b820191906000526020600020905b815481529060010190602001808311610773575b50509150506040516020818303038152906040528051906020012014156107b157600190506107b6565b600090505b919050565b80600260003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff168152602001908152602001600020908051906020019061080e9291906108f1565b5050565b6060600260003373ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff1681526020019081526020016000208054600181600116156101000203166002900480601f0160208091040260200160405190810160405280929190818152602001828054600181600116156101000203166002900480156108e75780601f106108bc576101008083540402835291602001916108e7565b820191906000526020600020905b8154815290600101906020018083116108ca57829003601f168201915b5050505050905090565b828054600181600116156101000203166002900490600052602060002090601f016020900481019282601f1061093257805160ff1916838001178555610960565b82800160010185558215610960579182015b8281111561095f578251825591602001919060010190610944565b5b50905061096d9190610971565b5090565b61099391905b8082111561098f576000816000905550600101610977565b5090565b9056fea265627a7a72315820577369a2616b07fa7f9d751e3587a78ee02983b476ea24fdd5f412ce84a7c5e364736f6c634300050b0032"

    w3.eth.defaultAccount = w3.eth.accounts[0]
    Exams = w3.eth.contract(abi=abi, bytecode=bytecode)

    # This deploys the contract
    tx_hash = Exams.constructor().transact()

    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    exams = w3.eth.contract(
        address=tx_receipt.contractAddress,
        abi=abi
    )

    # Test the contract
    exam_hash = "9B70ECA3C4BF210264CE44B42DE6A2095C440B857D8F94A44F7440E389A3A1BC"

    # Add an exam to the first address
    tx_hash = exams.functions.addExam(exam_hash).transact()
    return HttpResponse(tx_hash)
