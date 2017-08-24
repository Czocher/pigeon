pigeon
====

An MTA (*Mail Transfer Agent*) which resends emails to a given recipient while also encrypting them with the recepitent's public key.


Functionality:
-------------
  - [ ] encrypt and resend a received email to a given recipient
    - [ ] receipient is from a list of allowed receipients
    - [ ] do not encrypt encrypted emails
  - [ ] notify the receipient in case of errors
  - [ ] support either TLS/SSL (prefered) or STARTTLS (less secure) or both
  - [ ] verify/authenticate the connecting party
  - [ ] support logging
  - [ ] WUI configuration screen?
