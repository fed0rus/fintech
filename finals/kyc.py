#!/usr/bin/env python

from eth_abi import encode_abi
import json
import requests
from web3 import Web3, HTTPProvider
import argparse

# -----------UTILS START------------

def initParser():

    parser = argparse.ArgumentParser()
    parser.add_argument("--list", action="store", help="List all the requests")
    parser.add_argument("--confirm", action="store", help="Confirm the request")
    parser.add_argument("--get", action="store", help="Get the account by phone number")
    args = parser.parse_args()
    return vars(args)

class User(object):

    def __init__(self, UUID, PIN):
        self.UUID = "0x" + str(UUID.replace('-', ''))
        self.PIN = [int(k) for k in PIN]

    def setServer(self, server):
        self.server = server

    def generatePrivateKey(self):
        UUID = self.UUID
        PIN = self.PIN
        privateKey = server.solidityKeccak(["bytes16"], [b''])
        for k in range(4):
            privateKey = Web3.solidityKeccak(["bytes16", "bytes16", "int8"], [privateKey, UUID, PIN[k]]) # ABI-packed, keccak256 hashed
        self.privateKey = privateKey

    def generateAddress(self):
        account = Account.privateKeyToAccount(self.privateKey)
        self.address = account.address

def scaleValue(value):
    if value == 0:
        return "0 poa"
    elif value < 1e3:
        return str(value) + " wei"
    elif 1e3 <= value < 1e6:
        val = float("{:.6f}".format((float(value) / 1e3)))
        return str(int(val)) + " kwei" if val - int(val) == 0 else str(val) + " kwei"
    elif 1e6 <= value < 1e9:
        val = float("{:.6f}".format((float(value) / 1e6)))
        return str(int(val)) + " mwei" if val - int(val) == 0 else str(val) + " mwei"
    elif 1e9 <= value < 1e12:
        val = float("{:.6f}".format((float(value) / 1e9)))
        return str(int(val)) + " gwei" if val - int(val) == 0 else str(val) + " gwei"
    elif 1e12 <= value < 1e15:
        val = float("{:.6f}".format((float(value) / 1e12)))
        return str(int(val)) + " szabo" if val - int(val) == 0 else str(val) + " szabo"
    elif 1e15 <= value < 1e18:
        val = float("{:.6f}".format((float(value) / 1e15)))
        return str(int(val)) + " finney" if val - int(val) == 0 else str(val) + " finney"
    else:
        val = float("{:.6f}".format((float(value) / 1e18)))
        return str(int(val)) + " poa" if val - int(val) == 0 else str(val) + " poa"

def getBalanceByID(server):
    try:
        with open("person.json", 'r') as person:
            data = json.load(person)
            id = str(data["id"])
        PIN = args["balance"]
        user = User(id, PIN)
        user.setServer(server)
        user.generatePrivateKey()
        user.generateAddress()
        balance = scaleValue(server.eth.getBalance(user.address))
        print("Your balance is {}".format(balance))
    except:
        print("ID is not found")

def getUser(server, _privateKey):
    return server.eth.account.privateKeyToAccount(_privateKey)

def getGasPrice(speed):
    try:
        response = requests.get(_gasPriceURL)
        return int((response.json())[speed] * 1e9)
    except:
        return int(_defaultGasPrice)

def cleanTxResponse(rawReceipt):
    return eval(str(rawReceipt)[14:-1]) if rawReceipt is not None else None

def getValidator(server):
    ABI = json.loads('[{"constant":true,"inputs":[{"name":"c","type":"address"}],"name":"checkValidityKYC","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"c","type":"address"}],"name":"addValidationPH","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"c","type":"address"}],"name":"checkValidityPH","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"list","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"c","type":"address"}],"name":"addValidationKYC","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"}]')
    validator = server.eth.contract(address="0x0B603024EB0d2Da5C5c862a87d84FE9A5a5a905C", abi=ABI)
    return validator

def checkContract(Server, contract, flag):
    checkerServer = Web3(HTTPProvider("https://sokol.poa.network"))
    validator = getValidator(checkerServer)
    if flag == "kyc":
        status = callContract(validator, methodName="checkValidityKYC", methodArgs=[contract.address])
        if status:
            return True
        return False
    elif flag == "ph":
        status = callContract(validator, methodName="checkValidityPH", methodArgs=[contract.address])
        if status:
            return True
        return False

def kycData():
    # with open("KYC.bin", 'r') as bin:
    #     _bytecode = bin.read()
    # with open("KYC.abi", 'r') as abi:
    #     _abi = json.loads(abi.read())
    _bytecode = "608060405234801561001057600080fd5b5033151561001d57600080fd5b60008054600160a060020a03191633179055610f838061003e6000396000f3fe60806040526004361061011b576000357c010000000000000000000000000000000000000000000000000000000090048063851b16f5116100b25780639ee1bd0f116100815780639ee1bd0f146103a0578063a6f9dae1146103b5578063b93f9b0a146103e8578063bd47824314610412578063f82c50f1146104425761011b565b8063851b16f514610310578063942ea46614610325578063987fa1ed146103585780639c8e149e1461038b5761011b565b80634ca1fad8116100ee5780634ca1fad8146102895780635a58cd4c146102b357806374adad1d146102c857806383904f8d146102fb5761011b565b806309e6707d1461011d5780631d25899b1461016257806330ccebb5146101a85780634157272a146101db575b005b34801561012957600080fd5b506101506004803603602081101561014057600080fd5b5035600160a060020a031661046c565b60408051918252519081900360200190f35b34801561016e57600080fd5b5061018c6004803603602081101561018557600080fd5b503561047e565b60408051600160a060020a039092168252519081900360200190f35b3480156101b457600080fd5b50610150600480360360208110156101cb57600080fd5b5035600160a060020a0316610499565b3480156101e757600080fd5b506101f06104b8565b604051808060200180602001838103835285818151815260200191508051906020019060200280838360005b8381101561023457818101518382015260200161021c565b50505050905001838103825284818151815260200191508051906020019060200280838360005b8381101561027357818101518382015260200161025b565b5050505090500194505050505060405180910390f35b34801561029557600080fd5b5061011b600480360360208110156102ac57600080fd5b503561054c565b3480156102bf57600080fd5b5061011b61062e565b3480156102d457600080fd5b50610150600480360360208110156102eb57600080fd5b5035600160a060020a0316610653565b34801561030757600080fd5b5061011b610665565b34801561031c57600080fd5b5061011b610723565b34801561033157600080fd5b506101506004803603602081101561034857600080fd5b5035600160a060020a03166108e8565b34801561036457600080fd5b5061011b6004803603602081101561037b57600080fd5b5035600160a060020a031661092b565b34801561039757600080fd5b506101f0610c69565b3480156103ac57600080fd5b5061018c610cd4565b3480156103c157600080fd5b5061011b600480360360208110156103d857600080fd5b5035600160a060020a0316610ce4565b3480156103f457600080fd5b5061018c6004803603602081101561040b57600080fd5b5035610d38565b34801561041e57600080fd5b5061011b6004803603604081101561043557600080fd5b5080359060200135610d7a565b34801561044e57600080fd5b5061018c6004803603602081101561046557600080fd5b5035610e74565b60016020526000908152604090205481565b600260205260009081526040902054600160a060020a031681565b600160a060020a0381166000908152600460205260409020545b919050565b6003546060908190818060005b83811015610541576001600460006003848154811015156104e257fe5b6000918252602080832090910154600160a060020a03168352820192909252604001902054111561053957600380548290811061051b57fe5b6000918252602090912001548351600160a060020a03909116908490fe5b6001016104c5565b509093509150509091565b33151561055857600080fd5b6402540be4008110158015610572575064174876e7ff8111155b151561057d57600080fd5b336000908152600460205260409020541561059757600080fd5b33600090815260016020526040902054156105b157600080fd5b33600081815260046020526040808220849055517fdc79fc57451962cfe3916e686997a49229af75ce2055deb4c0f0fdf3d5d2e7c19190a250600380546001810182556000919091527fc2575a0e9e593c00f959f8c92f12db2869c3395a3b0502d05e2516446f71f85b018054600160a060020a03191633179055565b600054600160a060020a0316331461064557600080fd5b600054600160a060020a0316ff5b60046020526000908152604090205481565b33151561067157600080fd5b336000908152600460205260409020541561068b57600080fd5b3360009081526001602052604090205415156106a657600080fd5b3360008181526004602052604080822060019055517f64ed2364f9ee0643b60aeffba4ace8805648fad0d546c5efd449d1de10c8dcee9190a2600380546001810182556000919091527fc2575a0e9e593c00f959f8c92f12db2869c3395a3b0502d05e2516446f71f85b018054600160a060020a03191633179055565b33151561072f57600080fd5b33600090815260046020526040902054151561074a57600080fd5b3360009081526004602052604081205460011415610766575060015b3360009081526004602052604081205580156107ac5760405133907f8c08d387d1333f3da7e980dd7fc958615d513ca73155b6dd2a5a13e17acd116290600090a26107d8565b60405133907fffdf549003cf56ac2e863a28d8d5191467cf2a6d5e659f6a649e855a3d8cd8d090600090a25b60035460606000805b838110156108cd5760038054339190839081106107fa57fe5b600091825260209091200154600160a060020a0316141561081e57600191506108c5565b81151561087557600380548290811061083357fe5b6000918252602090912001548351600160a060020a039091169084908390811061085957fe5b600160a060020a039092166020928302909101909101526108c5565b600380548290811061088357fe5b6000918252602090912001548351600160a060020a0390911690849060001984019081106108ad57fe5b600160a060020a039092166020928302909101909101525b6001016107e1565b5081516108e1906003906020850190610e9c565b5050505050565b600160a060020a038116600090815260016020526040812054151561090f575060006104b3565b50600160a060020a031660009081526001602052604090205490565b600054600160a060020a0316331461094257600080fd5b600160a060020a0381166000908152600460205260409020546001811415610adc57600160a060020a038216600081815260016020908152604080832080549084905580845260029092528083208054600160a060020a0319169055519092917f6381abe854c1429e636a1aa796dd6057d1f1e4836874fbb184650908c49804cc91a260035460606000805b83811015610abe5786600160a060020a03166003828154811015156109ef57fe5b600091825260209091200154600160a060020a03161415610a0f57600191505b811515610a66576003805482908110610a2457fe5b6000918252602090912001548351600160a060020a0390911690849083908110610a4a57fe5b600160a060020a03909216602092830290910190910152610ab6565b6003805482908110610a7457fe5b6000918252602090912001548351600160a060020a039091169084906000198401908110610a9e57fe5b600160a060020a039092166020928302909101909101525b6001016109ce565b508151610ad2906003906020850190610e9c565b5050505050610c65565b6001811115610c6057600160a060020a03821660008181526004602090815260408083205460018352818420819055835260029091528082208054600160a060020a03191684179055517fa010ae0edd95ff06bc66e3eacf9d4f39b23da7ae3056a38dd6c1dcd05630a6da9190a260035460606000805b83811015610c435785600160a060020a0316600382815481101515610b7457fe5b600091825260209091200154600160a060020a03161415610b9457600191505b811515610beb576003805482908110610ba957fe5b6000918252602090912001548351600160a060020a0390911690849083908110610bcf57fe5b600160a060020a03909216602092830290910190910152610c3b565b6003805482908110610bf957fe5b6000918252602090912001548351600160a060020a039091169084906000198401908110610c2357fe5b600160a060020a039092166020928302909101909101525b600101610b53565b508151610c57906003906020850190610e9c565b50505050610c65565b600080fd5b5050565b6003546060908190818060005b838110156105415760046000600383815481101515610c9157fe5b6000918252602080832090910154600160a060020a0316835282019290925260400190205460011415610ccc57600380548290811061051b57fe5b600101610c76565b600054600160a060020a03165b90565b600054600160a060020a03163314610cfb57600080fd5b600054600160a060020a0382811691161415610d1657600080fd5b60008054600160a060020a031916600160a060020a0392909216919091179055565b600081815260026020526040812054600160a060020a03161515610d5e575060006104b3565b50600090815260026020526040902054600160a060020a031690565b331515610d8657600080fd5b610d8e610f01565b338152602081019283526040810191825242606082019081526005805460018101825560009190915291517f036b6384b5eca791c62761152d0c79bb0604c104a5fb6f4eb0703f3154bb3db060049093029283018054600160a060020a031916600160a060020a0390921691909117905592517f036b6384b5eca791c62761152d0c79bb0604c104a5fb6f4eb0703f3154bb3db182015590517f036b6384b5eca791c62761152d0c79bb0604c104a5fb6f4eb0703f3154bb3db282015590517f036b6384b5eca791c62761152d0c79bb0604c104a5fb6f4eb0703f3154bb3db390910155565b6003805482908110610e8257fe5b600091825260209091200154600160a060020a0316905081565b828054828255906000526020600020908101928215610ef1579160200282015b82811115610ef15782518254600160a060020a031916600160a060020a03909116178255602090920191600190910190610ebc565b50610efd929150610f33565b5090565b6080604051908101604052806000600160a060020a031681526020016000815260200160008152602001600081525090565b610ce191905b80821115610efd578054600160a060020a0319168155600101610f3956fea165627a7a723058209025ac58f3182597e868c4c0250fa3cb522fbea8b8ddfd6b6ac1f560ea0990c40029"
    _abi = json.loads('[{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"AtN","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"NtA","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_address","type":"address"}],"name":"getStatus","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"listAdd","outputs":[{"name":"","type":"address[]"},{"name":"","type":"uint256[]"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_phoneNumber","type":"uint256"}],"name":"addRequest","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"deleteContract","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"requests","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"delRequest","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"cancelRequest","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_address","type":"address"}],"name":"getNumber","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"applicant","type":"address"}],"name":"confirmRequest","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"listDel","outputs":[{"name":"","type":"address[]"},{"name":"","type":"uint256[]"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"whoIsOwner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"newOwner","type":"address"}],"name":"changeOwner","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_pn","type":"uint256"}],"name":"getAddress","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_pn","type":"uint256"},{"name":"_value","type":"uint256"}],"name":"sendMoney","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"log","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"payable":true,"stateMutability":"payable","type":"fallback"},{"anonymous":false,"inputs":[{"indexed":true,"name":"sender","type":"address"}],"name":"RegistrationRequest","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"sender","type":"address"}],"name":"UnregistrationRequest","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"sender","type":"address"}],"name":"RegistrationCanceled","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"sender","type":"address"}],"name":"UnregistrationCanceled","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"sender","type":"address"}],"name":"RegistrationConfirmed","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"sender","type":"address"}],"name":"UnregistrationConfirmed","type":"event"}]')
    return _bytecode, _abi

def phData():
    # with open("PaymentHandler.bin", 'r') as bin:
    #     _bytecode = bin.read()
    # with open("PaymentHandler.abi", 'r') as abi:
    #     _abi = json.loads(abi.read())
    _bytecode = "608060405234801561001057600080fd5b5033151561001d57600080fd5b60008054600160a060020a0319163317905561018c8061003e6000396000f3fe608060405260043610610050577c010000000000000000000000000000000000000000000000000000000060003504635a58cd4c81146100525780639ee1bd0f14610067578063a6f9dae114610098575b005b34801561005e57600080fd5b506100506100cb565b34801561007357600080fd5b5061007c6100f0565b60408051600160a060020a039092168252519081900360200190f35b3480156100a457600080fd5b50610050600480360360208110156100bb57600080fd5b5035600160a060020a03166100ff565b600054600160a060020a031633146100e257600080fd5b600054600160a060020a0316ff5b600054600160a060020a031690565b600054600160a060020a0316331461011657600080fd5b600054600160a060020a038281169116141561013157600080fd5b6000805473ffffffffffffffffffffffffffffffffffffffff1916600160a060020a039290921691909117905556fea165627a7a72305820526f825b0f9f8428b7535543052e096311f15a10c1a7ae2ddf550741af04d4df0029"
    _abi = json.loads('[{"constant":false,"inputs":[],"name":"deleteContract","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"whoIsOwner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"newOwner","type":"address"}],"name":"changeOwner","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"payable":true,"stateMutability":"payable","type":"fallback"}]')
    return _bytecode, _abi


def send(server, sender, dest, val):
    txUnsigned = {
        "from": sender.address,
        "to": dest,
        "nonce": server.eth.getTransactionCount(sender.address),
        "gas": 21000,
        "gasPrice": getGasPrice(speed="fast"),
        "value": int(val),
    }
    txSigned = sender.signTransaction(txUnsigned)
    try:
        txHash = server.eth.sendRawTransaction(txSigned.rawTransaction).hex()
    except:
        return "No funds to send the payment"
    return txHash

def getContract(server, flag):

    try:
        with open("registrar.json", 'r') as db:
            data = json.load(db)
    except:
        return "No contract address"
    # switch contract type
    if flag == "kyc":
        _stub, _abi = kycData()
    elif flag == "ph":
        _stub, _abi = phData()
    contractAddress = data["registrar"]["address"]
    _contract = server.eth.contract(address=contractAddress, abi=_abi)
    return _contract

def invokeContract(server, sender, contract, methodName, methodArgs):

    _args = str(methodArgs)[1:-1]
    invoker = "contract.functions.{methodName}({methodArgs})".format(
        methodName=methodName,
        methodArgs=_args,
    )
    _gas = eval(invoker).estimateGas({"from": sender.address})
    txUnsigned = eval(invoker).buildTransaction({
        "from": sender.address,
        "nonce": server.eth.getTransactionCount(sender.address),
        "gas": _gas,
        "gasPrice": getGasPrice(speed="fast"),
    })
    txSigned = sender.signTransaction(txUnsigned)
    txHash = server.eth.sendRawTransaction(txSigned.rawTransaction).hex()
    return txHash

def callContract(contract, methodName, methodArgs=""):

    _args = str(methodArgs)[1:-1]
    response = "contract.functions.{methodName}({methodArgs}).call()".format(
    methodName=methodName,
    methodArgs=_args,
    )
    return eval(response)

# ------------UTILS END-------------

def listAdd(server):
    _contract = getContract(server, flag="kyc")
    addresses, numbers = callContract(_contract, methodName="listAdd")
    print(addresses)
    print(numbers)

def get(server, number):

    contract = getContract(server, flag="kyc")
    if contract == "No contract address":
        return contract

    if not checkContract(server, contract, flag="kyc"):
        return "Seems that the contract address is not the registrar contract"

    address = callContract(contract, methodName="getAddress", methodArgs=[int(number[1:])])
    if address == "0x0000000000000000000000000000000000000000":
        return "Correspondence not found"
    else:
        return "Registered correspondence: {}".format(address)
# ----------MAIN MUTEX------------

if __name__ == "__main__":

    # ----------START SET------------

    with open("network.json", 'r') as ethConfig:
        global _defaultGasPrice
        global _gasPriceURL
        global _rpcURL
        global _privateKey
        read = json.load(ethConfig)
        _rpcURL = str(read["rpcUrl"])
        _privateKey = str(read["privKey"])
        _gasPriceURL = str(read["gasPriceUrl"])
        _defaultGasPrice = str(read["defaultGasPrice"])

    args = initParser()
    server = Web3(HTTPProvider(_rpcURL))
    user = getUser(server, _privateKey)

    # -----------END SET-------------

    if args["list"] is not None:
        listAdd(server)

    elif args["get"] is not None:
        _phoneNumber = args["get"]
        if _phoneNumber[0] == '+' and _phoneNumber[1:].isdigit() and len(_phoneNumber) == 12:
            print(get(server, _phoneNumber))
        else:
            print("Incorrect phone number")
