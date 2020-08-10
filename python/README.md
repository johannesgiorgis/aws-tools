# AWS Tools in Python

## TODO

- [ ] Re-factor AWS Glue scripts to use batch approach vs. individual calls to reduce `Rate Exceeded` rates
- [ ] Re-factor AWS Glue scripts to use class based approach
- [ ] Feed the session to the service classes and let them create the client -> avoid having the user create the sessions. Importing a service class should be all that concerns the user
- [ ] Get step functions scripts working
