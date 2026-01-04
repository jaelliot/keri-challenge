
hackmd.io
Programming Challenge KERI Fou - HackMD
5–6 minutes
Programming Challenge KERI Foundation
Create Falcon API using signed requests/responses

Use Falcon as web framework and falcon test client for test fixtures
Run test fixtures in pytest to demonstrate functionality of code.
Register data

A user name for a given requestor AID is registered using POST. The POST body is a SAD with a SAID. The POST includes a signature header which includes a signature of the SAID of the SAD that is the POST body. The signature is generated with the private key of the AID of the requester. Use indexed signatures.

The post body is JSON of the following form.

{
    "d": "SAID value as CESR",
    "i": "AID value as CESR",
    "n":  "John Doe"
}

The Response to the POST returns the posted data JSON and a signature header. The response includes a signature header which signature is generated using the AID of the host and includes the SAID of the response body.
Read data

A GET request with a query parameter of either name= or AID= or SAID= returns associated JSON structure with the matching JSON data.
The signature header on the GET is signing using the requestor AID private key and includes a signature on a digest of the query parameter string.

The GET Response returns the JSON body and the signature header is signed by the Host AID and includes the SAID of the response body JSON
Errors

Error responses do no need to be signed with signature header
Data Storage

May store data in package/module level memory for purpose of test fixture.
Demonstration

Create public github repo of code with test fixture. Document usage in readme file.

Confirmation will consist of installing repo on local machine and running pytest over test fixture(s).

All signature headers must be verified by recipient (client or host)

Tests should include failed signature verification (i.e. bad signature in signature header)

Use appropriate asserts to indicate proper values in tests.

Feel free to ask questions. Better to ask and get it working than to not ask and have it fail due to a misunderstanding.
Questions

Only use signature header. Do not need to use siginput header.
Resources

See RFC8941 https://www.rfc-editor.org/rfc/rfc8941.html
See RFC9421 https://datatracker.ietf.org/doc/html/rfc9421#signature-header

Use the keripy library https://github.com/WebOfTrust/keripy

See src/keri/end/ending.py for the signature() designature() functions

See tests/end/test_ending.py for example unit tests of the functionality in ending.py

See keri/core/coring.py Saider class for class that supports
generating SAIDs on json serializations of python dicts

See keri/app/httping.py class SignatureValidationComponent has example code for verifying signature header

To generate AID use the habbing.openHab context manager or use the openHby context manager with hby.makeHab

hab.pre is the AID

for example


with habbing.openHab(name="test", base="test", temp=True, salt=b'0123456789abcdef') as (hby, hab):
        

with habbing.openHby(name=name, base=base, salt=core.Salter(raw=b'0123456789abcdef').qb64) as hby:
        # hby = habbing.Habery(name=name, base=base, temp=temp, free=True)
        hab = hby.makeHab(name=name, icount=3)
        print()
        print([verfer.qb64 for verfer in hab.kever.verfers])
        # setup habitat
        # hab = habbing.Habitat(name=name, ks=ks, db=db, temp=temp, icount=3)
        assert hab.pre == 'EGqHykT1gVyuWxsVW6LUUsz_KtLJGYMi_SrohInwvjC-'
        digest = hab.kever.serder.said
        assert digest == hab.pre

        # example body text
        text = (b'{"seid":"BA89hKezugU2LFKiFVbitoHAxXqJh6HQ8Rn9tH7fxd68","name":"wit0","dts":"'
                b'2021-01-01T00:00:00.000000+00:00","scheme":"http","host":"localhost","port":'
                b'8080,"path":"/witness"}')

        sigers = hab.sign(ser=text, verfers=hab.kever.verfers)

        # test signature with list markers as indexed sigers and defaults for indexed and signer
        signage = ending.Signage(markers=sigers, indexed=None, signer=None, ordinal=None, digest=None,
                                 kind=None)
        header = ending.signature([signage])  # put it in a list
        assert header == {
            'Signature': 'indexed="?1";0="AACsufRGYI-sRvS2c0rsOueSoSRtrjODaf48DYLJbLvvD8aHe7b2sWGebZ-y9ichhsxMF3Hhn'
                         '-3LYSKIrnmH3oIN";1="ABDs7m2-h5l7vpjYtbFXtksicpZK5Oclm43EOkE2xoQOfr08doj73VrlKZOKNfJmRumD3tfaiFFgVZqPgiHuFVoA";2="ACDVOy2LvGgFINUneL4iwA55ypJR6vDpLLbdleEsiANmFazwZARypJMiw9vu2Iu0oL7XCUiUT4JncU8P3HdIp40F"'}

        

