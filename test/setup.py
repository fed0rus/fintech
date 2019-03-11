#!/usr/bin/env python

from eth_abi import encode_abi
import json
import requests
from web3 import Web3, HTTPProvider
import argparse
import time

# -----------UTILS START------------

HexBytes = lambda x: x

def initParser():

    parser = argparse.ArgumentParser()
    parser.add_argument("--deploy", action="store_true", help="Deploy a new contract")
    parser.add_argument("--owner", action="store", help="Know the owner of the contract")
    parser.add_argument("--chown", action="store", nargs='+', help="Change the owner of the contract")
    parser.add_argument("--send", action="store", nargs='+', help="Send money")
    args = parser.parse_args()
    return vars(args)

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

def kycData():
    # with open("KYC.bin", 'r') as bin:
    #     _bytecode = bin.read()
    # with open("KYC.abi", 'r') as abi:
    #     _abi = json.loads(abi.read())
    _bytecode = "608060405234801561001057600080fd5b5033151561001d57600080fd5b60008054600160a060020a0319163317905561101e8061003e6000396000f3fe60806040526004361061011b576000357c010000000000000000000000000000000000000000000000000000000090048063942ea466116100b2578063b93f9b0a11610081578063b93f9b0a14610325578063bd4782431461034f578063f82c50f11461037f578063fc735e99146103a9578063fddc5f28146103d25761011b565b8063942ea46614610277578063987fa1ed146102aa5780639ee1bd0f146102dd578063a6f9dae1146102f25761011b565b80635a58cd4c116100ee5780635a58cd4c1461020557806374adad1d1461021a57806383904f8d1461024d578063851b16f5146102625761011b565b806309e6707d1461011d5780631d25899b1461016257806330ccebb5146101a85780634ca1fad8146101db575b005b34801561012957600080fd5b506101506004803603602081101561014057600080fd5b5035600160a060020a0316610528565b60408051918252519081900360200190f35b34801561016e57600080fd5b5061018c6004803603602081101561018557600080fd5b503561053a565b60408051600160a060020a039092168252519081900360200190f35b3480156101b457600080fd5b50610150600480360360208110156101cb57600080fd5b5035600160a060020a0316610555565b3480156101e757600080fd5b5061011b600480360360208110156101fe57600080fd5b5035610574565b34801561021157600080fd5b5061011b610656565b34801561022657600080fd5b506101506004803603602081101561023d57600080fd5b5035600160a060020a031661067b565b34801561025957600080fd5b5061011b61068d565b34801561026e57600080fd5b5061011b61074b565b34801561028357600080fd5b506101506004803603602081101561029a57600080fd5b5035600160a060020a0316610910565b3480156102b657600080fd5b5061011b600480360360208110156102cd57600080fd5b5035600160a060020a0316610953565b3480156102e957600080fd5b5061018c610ca8565b3480156102fe57600080fd5b5061011b6004803603602081101561031557600080fd5b5035600160a060020a0316610cb8565b34801561033157600080fd5b5061018c6004803603602081101561034857600080fd5b5035610d0c565b34801561035b57600080fd5b5061011b6004803603604081101561037257600080fd5b5080359060200135610d4e565b34801561038b57600080fd5b5061018c600480360360208110156103a257600080fd5b5035610e48565b3480156103b557600080fd5b506103be610e70565b604080519115158252519081900360200190f35b3480156103de57600080fd5b50610405600480360360208110156103f557600080fd5b5035600160a060020a0316610e75565b6040518080602001806020018060200180602001858103855289818151815260200191508051906020019060200280838360005b83811015610451578181015183820152602001610439565b50505050905001858103845288818151815260200191508051906020019060200280838360005b83811015610490578181015183820152602001610478565b50505050905001858103835287818151815260200191508051906020019060200280838360005b838110156104cf5781810151838201526020016104b7565b50505050905001858103825286818151815260200191508051906020019060200280838360005b8381101561050e5781810151838201526020016104f6565b505050509050019850505050505050505060405180910390f35b60016020526000908152604090205481565b600260205260009081526040902054600160a060020a031681565b600160a060020a0381166000908152600460205260409020545b919050565b33151561058057600080fd5b6402540be400811015801561059a575064174876e7ff8111155b15156105a557600080fd5b33600090815260046020526040902054156105bf57600080fd5b33600090815260016020526040902054156105d957600080fd5b33600081815260046020526040808220849055517fdc79fc57451962cfe3916e686997a49229af75ce2055deb4c0f0fdf3d5d2e7c19190a250600380546001810182556000919091527fc2575a0e9e593c00f959f8c92f12db2869c3395a3b0502d05e2516446f71f85b018054600160a060020a03191633179055565b600054600160a060020a0316331461066d57600080fd5b600054600160a060020a0316ff5b60046020526000908152604090205481565b33151561069957600080fd5b33600090815260046020526040902054156106b357600080fd5b3360009081526001602052604090205415156106ce57600080fd5b3360008181526004602052604080822060019055517f64ed2364f9ee0643b60aeffba4ace8805648fad0d546c5efd449d1de10c8dcee9190a2600380546001810182556000919091527fc2575a0e9e593c00f959f8c92f12db2869c3395a3b0502d05e2516446f71f85b018054600160a060020a03191633179055565b33151561075757600080fd5b33600090815260046020526040902054151561077257600080fd5b336000908152600460205260408120546001141561078e575060015b3360009081526004602052604081205580156107d45760405133907f8c08d387d1333f3da7e980dd7fc958615d513ca73155b6dd2a5a13e17acd116290600090a2610800565b60405133907fffdf549003cf56ac2e863a28d8d5191467cf2a6d5e659f6a649e855a3d8cd8d090600090a25b60035460606000805b838110156108f557600380543391908390811061082257fe5b600091825260209091200154600160a060020a0316141561084657600191506108ed565b81151561089d57600380548290811061085b57fe5b6000918252602090912001548351600160a060020a039091169084908390811061088157fe5b600160a060020a039092166020928302909101909101526108ed565b60038054829081106108ab57fe5b6000918252602090912001548351600160a060020a0390911690849060001984019081106108d557fe5b600160a060020a039092166020928302909101909101525b600101610809565b508151610909906003906020850190610f37565b5050505050565b600160a060020a03811660009081526001602052604081205415156109375750600061056f565b50600160a060020a031660009081526001602052604090205490565b600054600160a060020a0316331461096a57600080fd5b600160a060020a0381166000908152600460205260409020546001811415610b1557600160a060020a0382166000818152600160209081526040808320805490849055808452600283528184208054600160a060020a03191690558484526004909252808320839055519092917f6381abe854c1429e636a1aa796dd6057d1f1e4836874fbb184650908c49804cc91a260035460606000805b83811015610af75786600160a060020a0316600382815481101515610a2457fe5b600091825260209091200154600160a060020a03161415610a485760019150610aef565b811515610a9f576003805482908110610a5d57fe5b6000918252602090912001548351600160a060020a0390911690849083908110610a8357fe5b600160a060020a03909216602092830290910190910152610aef565b6003805482908110610aad57fe5b6000918252602090912001548351600160a060020a039091169084906000198401908110610ad757fe5b600160a060020a039092166020928302909101909101525b600101610a03565b508151610b0b906003906020850190610f37565b5050505050610ca4565b6001811115610ca457600160a060020a03821660008181526004602081815260408084208054600184528286208190558552600283528185208054600160a060020a031916871790558585529290915290829055517fa010ae0edd95ff06bc66e3eacf9d4f39b23da7ae3056a38dd6c1dcd05630a6da9190a260035460606000805b83811015610c8b5785600160a060020a0316600382815481101515610bb857fe5b600091825260209091200154600160a060020a03161415610bdc5760019150610c83565b811515610c33576003805482908110610bf157fe5b6000918252602090912001548351600160a060020a0390911690849083908110610c1757fe5b600160a060020a03909216602092830290910190910152610c83565b6003805482908110610c4157fe5b6000918252602090912001548351600160a060020a039091169084906000198401908110610c6b57fe5b600160a060020a039092166020928302909101909101525b600101610b97565b508151610c9f906003906020850190610f37565b505050505b5050565b600054600160a060020a03165b90565b600054600160a060020a03163314610ccf57600080fd5b600054600160a060020a0382811691161415610cea57600080fd5b60008054600160a060020a031916600160a060020a0392909216919091179055565b600081815260026020526040812054600160a060020a03161515610d325750600061056f565b50600090815260026020526040902054600160a060020a031690565b331515610d5a57600080fd5b610d62610f9c565b338152602081019283526040810191825242606082019081526005805460018101825560009190915291517f036b6384b5eca791c62761152d0c79bb0604c104a5fb6f4eb0703f3154bb3db060049093029283018054600160a060020a031916600160a060020a0390921691909117905592517f036b6384b5eca791c62761152d0c79bb0604c104a5fb6f4eb0703f3154bb3db182015590517f036b6384b5eca791c62761152d0c79bb0604c104a5fb6f4eb0703f3154bb3db282015590517f036b6384b5eca791c62761152d0c79bb0604c104a5fb6f4eb0703f3154bb3db390910155565b6003805482908110610e5657fe5b600091825260209091200154600160a060020a0316905081565b600190565b600554606090819081908190819081908190819060005b81811015610f26578a600160a060020a0316600582815481101515610ead57fe5b6000918252602090912060049091020154600160a060020a03161415610ed65785516001908790fe5b600160a060020a038b166000908152600160205260409020546005805483908110610efd57fe5b9060005260206000209060040201600101541415610f1e5785516000908790fe5b600101610e8c565b509399929850909650945092505050565b828054828255906000526020600020908101928215610f8c579160200282015b82811115610f8c5782518254600160a060020a031916600160a060020a03909116178255602090920191600190910190610f57565b50610f98929150610fce565b5090565b6080604051908101604052806000600160a060020a031681526020016000815260200160008152602001600081525090565b610cb591905b80821115610f98578054600160a060020a0319168155600101610fd456fea165627a7a7230582031b38a39cb23177069cee5b8bd513962195f496cd0052717afc5848a822d138a0029"
    _abi = json.loads('[{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"AtN","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"NtA","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_address","type":"address"}],"name":"getStatus","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_phoneNumber","type":"uint256"}],"name":"addRequest","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"deleteContract","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"address"}],"name":"requests","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"delRequest","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"cancelRequest","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_address","type":"address"}],"name":"getNumber","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"applicant","type":"address"}],"name":"confirmRequest","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"whoIsOwner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"newOwner","type":"address"}],"name":"changeOwner","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_pn","type":"uint256"}],"name":"getAddress","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_pn","type":"uint256"},{"name":"_value","type":"uint256"}],"name":"sendMoney","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"log","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"verify","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[{"name":"caller","type":"address"}],"name":"listPayments","outputs":[{"name":"","type":"bool[]"},{"name":"","type":"uint256[]"},{"name":"","type":"uint256[]"},{"name":"","type":"uint256[]"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"payable":true,"stateMutability":"payable","type":"fallback"},{"anonymous":false,"inputs":[{"indexed":true,"name":"sender","type":"address"}],"name":"RegistrationRequest","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"sender","type":"address"}],"name":"UnregistrationRequest","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"sender","type":"address"}],"name":"RegistrationCanceled","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"sender","type":"address"}],"name":"UnregistrationCanceled","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"sender","type":"address"}],"name":"RegistrationConfirmed","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"sender","type":"address"}],"name":"UnregistrationConfirmed","type":"event"}]')
    return _bytecode, _abi

def phData():
    # with open("PaymentHandler.bin", 'r') as bin:
    #     _bytecode = bin.read()
    # with open("PaymentHandler.abi", 'r') as abi:
    #     _abi = json.loads(abi.read())
    _bytecode = "608060405234801561001057600080fd5b5033151561001d57600080fd5b60008054600160a060020a0319163317905561018c8061003e6000396000f3fe608060405260043610610050577c010000000000000000000000000000000000000000000000000000000060003504635a58cd4c81146100525780639ee1bd0f14610067578063a6f9dae114610098575b005b34801561005e57600080fd5b506100506100cb565b34801561007357600080fd5b5061007c6100f0565b60408051600160a060020a039092168252519081900360200190f35b3480156100a457600080fd5b50610050600480360360208110156100bb57600080fd5b5035600160a060020a03166100ff565b600054600160a060020a031633146100e257600080fd5b600054600160a060020a0316ff5b600054600160a060020a031690565b600054600160a060020a0316331461011657600080fd5b600054600160a060020a038281169116141561013157600080fd5b6000805473ffffffffffffffffffffffffffffffffffffffff1916600160a060020a039290921691909117905556fea165627a7a72305820526f825b0f9f8428b7535543052e096311f15a10c1a7ae2ddf550741af04d4df0029"
    _abi = json.loads('[{"constant":false,"inputs":[],"name":"deleteContract","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"whoIsOwner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"newOwner","type":"address"}],"name":"changeOwner","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"payable":true,"stateMutability":"payable","type":"fallback"}]')
    return _bytecode, _abi

def deployContract(server, owner, flag):
    # switch contract type
    if flag == "kyc":
        _bytecode, _abi = kycData()
    elif flag == "ph":
        _bytecode, _abi = phData()
    # deployment
    rawContract = server.eth.contract(abi=_abi, bytecode=_bytecode)
    _gas = rawContract.constructor().estimateGas({"from": owner.address})
    txUnsigned = rawContract.constructor().buildTransaction({
        "from": owner.address,
        "nonce": server.eth.getTransactionCount(owner.address),
        "gas": _gas,
        "gasPrice": getGasPrice(speed="fast"),
    })
    txSigned = owner.signTransaction(txUnsigned)
    deploymentHash = server.eth.sendRawTransaction(txSigned.rawTransaction)
    txReceipt = server.eth.waitForTransactionReceipt(deploymentHash)
    if txReceipt["status"] == 1:
        contractAddress = cleanTxResponse(txReceipt)["contractAddress"]
        contract = server.eth.contract(
            address=contractAddress,
            abi=_abi,
        )
        startBlock = cleanTxResponse(txReceipt)["blockNumber"]
        return contract.address, startBlock
    else:
        raise

def getContract(server, flag):

    with open("registrar.json", 'r') as db:
        data = json.load(db)
    # switch contract type
    if flag == "kyc":
        _stub, _abi = kycData()
    elif flag == "ph":
        _stub, _abi = phData()
    contractAddress = data["registrar"]["address"]
    _contract = server.eth.contract(address=contractAddress, abi=_abi)
    return _contract

def invokeContract(server, sender, contract, methodName, methodArgs, ni=0):

    _args = str(methodArgs)[1:-1]
    invoker = "contract.functions.{methodName}({methodArgs})".format(
        methodName=methodName,
        methodArgs=_args,
    )
    _gas = eval(invoker).estimateGas({"from": sender.address})
    txUnsigned = eval(invoker).buildTransaction({
        "from": sender.address,
        "nonce": server.eth.getTransactionCount(sender.address) + ni,
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

# -----------UTILS END------------

# ---------ESSENTIALS START---------

def deploy(server, owner):

    KYCAddress, sb1 = deployContract(server, owner, flag="kyc")
    PHAddress, sb2 = deployContract(server, owner, flag="ph")
    data = {
        "registrar": {
            "address": KYCAddress,
            "startBlock": sb1
        },
        "payments": {
            "address": PHAddress,
            "startBlock": sb2
        }
    }
    with open("registrar.json", 'w') as db:
        json.dump(data, db)
    print("KYC Registrar: {}".format(KYCAddress))
    print("Payment Handler: {}".format(PHAddress))

def returnOwner(server, flag):

    _contract = getContract(server, flag)
    ownerAddress = callContract(_contract, methodName="whoIsOwner")
    return ownerAddress

def changeOwner(server, owner, newOwner, flag):
    assert server.isAddress(newOwner), "SWW"
    _contract = getContract(server, flag)
    txHash = invokeContract(server, owner, _contract, methodName="changeOwner", methodArgs=[newOwner])

# ---------ESSENTIALS END---------


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

    # US-001
    if args["deploy"] is not False:
        deploy(server, user)

    # US-002
    elif args["owner"] is not None:
        if args["owner"] == "registrar":
            ownerAddress = returnOwner(server, flag="kyc")
            print("Admin account: {}".format(ownerAddress))
        elif args["owner"] == "payments":
            ownerAddress = returnOwner(server, flag="ph")
            print("Admin account: {}".format(ownerAddress))
        else:
            raise ValueError("Enter a valid contract type")

    # US-003
    elif args["chown"] is not None:

        if args["chown"][0] == "registrar":
            try:
                newAdminAccount = args["chown"][1]
                changeOwner(server, user, newOwner=newAdminAccount, flag="kyc")
                print("New admin account: {}".format(newAdminAccount))
            except:
                print("Request cannot be executed")
        elif args["chown"][0] == "payments":
            try:
                newAdminAccount = args["chown"][1]
                changeOwner(server, user, newOwner=newAdminAccount, flag="ph")
                print("New admin account: {}".format(newAdminAccount))
            except:
                print("Request cannot be executed")
        else:
            raise ValueError("Enter a valid contract type")

'''
compile:
    solc --abi --bin --optimize --overwrite -o ./ KYCRegistrar.sol && solc --abi --bin --optimize --overwrite -o ./ PaymentHandler.sol
'''
