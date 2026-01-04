I need to figure out how to call both inputs.

ignore siginput

read the rfc documents

use the signature headers

go to test ending, units on how to use signature headers.

I'm calling library code to sign stuff. I need it to sign a signature header.

None of the unit tests verify the signatures.

keri/app/httping.py

there's a validate function in keri/app/httping.py

I just need to be able to call and sign requests.

"saider" object in coring.py; it injects the said into the object.

If I could use unit tests, then I should be able to learn the code.

create a public programming challenge, use pytests for the unit tests, there's no db (store in memory),