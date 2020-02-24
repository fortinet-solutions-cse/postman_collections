# SDWAN automation with FortiManager

This repository contains automation scripts and Postman collections to automate FortiManager operation for a successful deployment of an SDWAN configuration. This is achieved using JSON RPC API interface of FortiManager.

It is structured in the following parts:
- Base Configuration: Intended to run basic settings, add devices, setup policy packages, VPNs, etc.
- SDWAN configuration: It covers BGP, ADVPN and SDWAN general configuration


For each part you can choose to configure FortiManager using two alternatives:

- <b>Postman collections</b>: They allow to issue each request individually, iterating all the steps manually. Postman lets you visually inspect each request, result, headers and every detail or each JSON RPC API call.
- <b>Python scripts</b>: They run all the configuration steps automatically with no interaction required.


In order to use these tools, just clone the repo and follow steps below:

- <b>Postman</b>: Just import the .json file into Postman. A new collection will be created per each file.
- <b>Python</b>: Run the python script of your choice (inspect header lines first to adjust for your particular environemt)

Enjoy!