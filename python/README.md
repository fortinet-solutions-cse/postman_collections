# Automation with FortiManager API using Python

<!-- TOC -->

- [Goal](#goal)
- [Step by Step](#step-by-step)
  - [Scripts structure](#scripts-structure)
  - [Writing Your Child Class](#writing-your-child-class)
    - [Example 1: getDevices()](#example-1-getdevices)
    - [Example 2: setDeviceAttributes()](#example-2-setdeviceattributes)
  - [Writing Your Front Script](#writing-your-front-script)

<!-- /TOC -->

While Postman is a great tool for interactive usage, it probably will not be used
outside a demo or a POC. Primarily, Postman is a tool to _develop_ your API collections.
But once you are familiar with FMG API and once your collection is ready, you will
want to use a real automation platform for the actual deployment.

Here we demonstrate how to quickly start doing it with Python. Note that we are not
delivering a complete reusable FMG API library here. We are also not going to build
an entire solution with Python. We are just going to show a _skeleton_ that can be
then extended for your purposes. And we will show a few examples of "moving"
your API requests from Postman collections to this skeleton.

## Goal

In this demo, we are going to have two tenants in separate ADOMs: Customer1 and Customer2.

- Customer1 has 3 devices: dc1_fgt, branch1_fgt and branch2_fgt
- Customer2 has 1 device: branch3_fgt

We are going to set some meta fields on all devices for both these tenants.
We have an input file per tenant, listing the required values.

Our algorithm will be as simple as follows:

1. Parse the inputs for a given tenant
2. Get the list of managed devices
3. Set the meta fields for each managed device

Let us start from the very end and just show you how the script execution will look like,
once we are done. Note how we pass the tenant name in environment variable `FMG_TENANT`.
The rest just happens automatically:

```
% FMG_TENANT=Customer1 ./demo_update_dev.py
========================
 Tenant: Customer1
========================
     FMG URL = https://34.78.59.208:10415/jsonrpc
     Tenant ADOM = Customer1
Running request 0. Login
 Completed
Running request 1. Get Devices
 Completed
    Currently Managed Devices: 3
    Processing branch1_fgt
      List of meta variables:
          hub-wan1-ip = 100.64.1.1
          hub-wan2-ip = 172.16.1.5
          site-id = 1
    Processing branch2_fgt
      List of meta variables:
          hub-wan1-ip = 100.64.1.1
          hub-wan2-ip = 172.16.1.5
          site-id = 2
    Processing dc1_fgt
      List of meta variables:
          hub-wan1-ip = 100.64.1.1
          hub-wan2-ip = 172.16.1.5
Running request 2. Set Device Attributes
 Completed
```

```
% FMG_TENANT=Customer2 ./demo_update_dev.py
========================
 Tenant: Customer2
========================
     FMG URL = https://34.78.59.208:10415/jsonrpc
     Tenant ADOM = Customer2
Running request 0. Login
 Completed
Running request 1. Get Devices
 Completed
    Currently Managed Devices: 1
    Processing branch3_fgt
      List of meta variables:
          hub-wan1-ip = 100.64.2.1
          hub-wan2-ip = 172.16.2.5
          site-id = 1
Running request 2. Set Device Attributes
 Completed
```

Now when you know what we are planning to achieve, let's see how we do it...


## Step by Step

### Scripts structure

We have 3 "layers" in our scripting.

- First, we take `fmg_api.api_base` which implements a base class `ApiSession`.
  It does all the actual JSON requests. It can be used "as is" for any project,
  because it doesn't depend on what exactly you are planning to do with FMG API.
  It simply implements the following generic methods:

  - `_run_request()` to make an API call
  - `_run_request_async()` to make an API call asynchronously; that is, by creating FMG task

  It also implements `login()` method and maintains the session cookie,
  which makes sense, because you will of course need this for any project with
  FMG API.

- Second, we write our own child class, inheriting from `ApiSession`, implementing
  the actual API calls that we need for our particular project. This somewhat corresponds
  to Postman collection. In our demo it is `fmg_api.device_manager` with the class `DeviceManagerApi`.
  As you will see, it implements the following specific API calls:

  - `getDevices()` to return a list of managed devices
  - `setDeviceAttributes()` to set device location and meta fields
  - `assignCLITemplateGroup()` to assign CLI Template Group to devices
  - `addToDeviceGroup()` to add devices to Device Group
  - `installPolicy()` to install policy package on devices
  - `installConfiguration()` to install configuration on devices

  We are not going to use them all in this demo, but you can examine them all...

- Third, we write the actual "front" script that does what we really want to do.
  In our demo, this will be `demo_update_dev.py`.
  It parses the input (here it relies on another script, `demo_base.py`, that can also be reused "as is").
  Then it creates an instance of `DeviceManagerApi` and uses its exposed methods to
  accomplish the task.

The inputs are stored under `tenants` directory. There is a sub-directory for each
tenant, with `tenant.yaml.j2` input file inside each one. These files are in YAML format,
having the following structure:

```
---
fmg_user: # user to login to FMG
fmg_password: # password to login to FMG
adom: # tenant ADOM name

global:
  # Meta fields applicable to ALL devices for this tenant
  # ...

devices:
  name-of-first-device:
    vars:
      # Meta fields for first device
      # ...
  name-of-second-device:
    vars:
      # Meta fields for second device
      # ...
  # ...
```

You can also notice that the input files themselves are actually Jinja2 templates.
See how we use Jinja loop to simplify definition for Customer1 (imagine how it would
look like if it would have 100 devices, rather than just 2).  

Finally, there is also a global config file, `config.yaml`, which simply defines
the FMG API endpoint.

Now it's time to examine the second and the third layers in more detail.


### Writing Your Child Class

Your typical child class will look like this:

```
#!/usr/bin/env python3

from fmg_api.api_base import ApiSession

class YourCollectionOfApi(ApiSession):

    def firstApiCall(self, args):
      # ...

    def secondApiCall(self, args):
      # ...

    # ...
```

Each method of your class will implement a particular API call.
Hence, if the whole child class is somewhat similar to Postman collection, then
each method is somewhat similar to Postman request. And of course, each method
can accept arguments and apply some logic to them.

So our task now is to translate Postman requests into these Python methods.
Each method will generally have the following structure:

```
def yourApiCall(self, args):

    # Do some args processing, if needed...
    # ...

    # Build payload for JSON request
    payload = {
      # JSON payload (but in Python syntax)
    }

    self._run_request(payload, name="Your API Call Name")
```

If the request must create FMG task (e.g. it is a policy installation or device discovery), then we simply replace the last line with:

```
    self._run_request_async(payload, name="Your API Call Name")
```

This method doesn't return any value, which is great for `set` operations.
What about `get` operations though? Apparently, it's not very different.
Our `_run_request()` method returns JSON response (in Python representation),
so it can be easily parsed and returned:

```
    content = self._run_request(payload, name="Your API Call Name")
    return [ el['name'] for el in content["result"][0]["data"] ]
```

It's time for some specific examples...

#### Example 1: getDevices()

Let's look into our `getDevices()` method that returns the list of managed devices.

In Postman, our request would look like this:

```
{
    "session": "{{session}}",
    "id": 1,
    "method": "get",
    "params": [
        {
            "url": "/dvmdb/adom/{{adom}}/device"
        }
    ]
}
```

All we need to do is translate it into Python representation:

```
{
    "session": self._session,
    "id": 1,
    "method": "get",
    "params": [
        {
            "url": "/dvmdb/adom/" + self.adom + "/device",
        }
    ]
}
```

You might be surprised, but it looks... almost identical! Just referencing variables
is a little bit different. So this will be the value of our payload.

What about the return value? If we run the request in Postman, we can see that FMG
gives us the following JSON response:

```
{
  "method": "get",
  "result": [
    {
      "data": [
        {
          "name": "FirstDevice"
          # Other fields of the first device
        },
        {
          "name": "SecondDevice"
          # Other fields of the second device
        }
        # ...        
      ],
      "status": {
        "code": 0,
        "message": "OK"
      },
      "url": "/dvmdb/device"
    }
  ],
  "id": 1
}
```

So if we want to return a list of device names, we must:

- Take the whole response, which is a dict
- Look into `result` value, which is a list
- Pick the first element there, which is a dict
- Look into `data` value, which is a list
- For each element there, pick the `name` value.

Sounds complex, but this is how it will look like in Python:

```
[ dev['name'] for dev in content["result"][0]["data"] ]
```

And so, we can complete the method:

```
def getDevices(self):

    payload = {
        "session": self._session,
        "id": 1,
        "method": "get",
        "params": [
            {
                "url": "/dvmdb/adom/" + self.adom + "/device",
            }
        ]
    }

    content = self._run_request(payload, name="Get Devices")
    return [ dev['name'] for dev in content["result"][0]["data"] ]
```


#### Example 2: setDeviceAttributes()

Our `setDeviceAttributes()` method is going to set device attributes, including
meta fields and (optionally) location. Logically, the method must receive those
attributes from some upstream function - that will be our "front" script eventually.

We decide that the method is going to receive a list of dicts `dev_attr_list`,
of the following form:

```
[
  {
    "name": "FirstDevice",
    "location": {
      "latitude": 12.1,
      "longitude": 48.7
    },
    "vars": {
      "var1": "val1",
      "var2": "val2"
      # ...
    }
  },
  {
    "name": "SecondDevice",
    "vars": {
      "var1": "val3",
      "var2": "val4"
      # ...
    }    
  }
  # ...
]
```

Here is the Postman request with the equivalent of which we must end up:

```
{
    "session": "{{session}}",
    "id": 1,
    "method": "set",
    "params": [
        {
            "url": "/dvmdb/adom/{{adom}}/device",
            "data": [
                {
                    "name": "FirstDevice",
                    "latitude": "12.1",
                    "longitude": "48.7",
                    "meta fields": {
                        "var1": "val1",
                        "var2": "val2"
                    }
                },
                {
                    "name": "SecondDevice",
                    "meta fields": {
                        "var1": "val3",
                        "var2": "val4"
                    }
                }
                # ...
            ]
        }
    ]
}
```

So you can see that we must do some processing of the input.
This is a better idea than requiring all the "front" scripts to use the exact
syntax that the API call requires, because generally we do not want to think too
much about JSON when we write that "front" script. We want it to use some structures
that make sense for our project, and our method here will do the translation.

We must translate our received `dev_attr_list` into the `data` list of our JSON payload.
From a quick look, the following changes must be applied to `dev_attr_list`:

- Latitude and longitude values must come individually (there is no `location` dict)
- Instead of `vars`, in JSON we must say `meta fields`
- All the values in JSON must actually be strings!

This last item is particularly interesting. Depending on where your inputs come from,
their data type can easily be "a number" ("integer"). For example, you could specify
a latitude as `12.1` above, which is a number. Or you could specify some meta field value
as `5`, which is also a number. But if you try passing it this way to FMG, you
will get an error in response. That's because it expects only strings. So who will
ensure that we pass only strings? This could, of course, be the task for our "front"
script, but as before, we prefer to let it "talk" the intuitive language.
So our method will kindly do the conversion into strings.

To accomplish all this, let us define a new list and fill it up with the values from
`dev_attr_list`, but with the necessary translations:

```
set_dev_list = []
for dev in dev_attr_list:
    set_dev_list.append({
        "name": dev['name'],
        "latitude": str(dev['location']['latitude']) if 'location' in dev else "",
        "longitude": str(dev['location']['longitude'] if 'location' in dev else ""),
        "meta fields": { k: str(v) for k, v in dev['vars'].items() }
    })
```

You can see how we made the coordinates optional: if there is no `location` in the
input, we simply pass empty coordinates. And in any case, we apply `str()` on them,
so that they become strings and not numbers.

Similarly, we apply `str()` to all values of the meta fields.

This new list can be "plugged" into the payload dict that we are going to define -
that will be the `"data"`.
Putting it all together, this is our method:

```
def setDeviceAttributes(self, dev_attr_list):

    set_dev_list = []
    for dev in dev_attr_list:
        set_dev_list.append({
            "name": dev['name'],
            "latitude": str(dev['location']['latitude']) if 'location' in dev else "",
            "longitude": str(dev['location']['longitude'] if 'location' in dev else ""),
            "meta fields": { k: str(v) for k, v in dev['vars'].items() }
        })

    payload = {
        "session": self._session,
        "id": 1,
        "method": "set",
        "params": [
            {
                "url": "/dvmdb/adom/" + self.adom + "/device",
                "data": set_dev_list
            }
        ]
    }

    self._run_request(payload, name="Set Device Attributes")
```

This time, we do not need to return any value, because this is a `set` operation.


### Writing Your Front Script

Now it's time to use our child class in the "front" script.

You can start your script from the following skeleton:

```
#!/usr/bin/env python3

from fmg_api.your_collection import YourCollectionOfApi
from demo_base import *

def main():

    cfg = readConfig()

    session = YourCollectionOfApi(
        url = cfg['fmg_api'],
        adom = cfg['adom'],
        user = cfg['fmg_user'],
        password = cfg['fmg_password']
    )

    # Do your stuff


if __name__ == "__main__":
    main()
```

Here we use `demo_base.py` with `readConfig()` function that simply does the following:

- Reads the tenant name passed via environment variable `FMG_TENANT`
- Renders tenant input file (under `tenants/$FMG_TENANT/tenant.yaml.j2`) using Jinja2 engine
- Parses the global config (`config.yaml`) and the rendered tenant config using
  YAML parser and combines them both into a single dict `cfg`
- Returns `cfg` to be used further by the front script

Then we immediately create an instance of our child class, passing it the necessary
arguments from the newly obtained `cfg` dict. This automatically logs us in to FMG,
and we can use `session` object to make our API calls!

Our algorithm for this demo will be pretty straightforward:

- Get the list of all managed devices:

  ```
  managed_dev_list = session.getDevices()
  ```

- For each device, combine the global meta vars (from `global`) with per-device
  vars, as defined in the input files; add the combined list to `dev_attr_list`
  structure (as you recall, this is the structure that our API method needs):

  ```
  dev_attr_list = []
  for dev in managed_dev_list:
      vars = {}

      # Add global meta vars
      for i in cfg['global']:
          vars[i] = cfg['global'][i]

      # Add per-device meta vars
      if dev in cfg['devices']:
          for i in cfg['devices'][dev]['vars']:
              vars[i] = cfg['devices'][dev]['vars'][i]  

      dev_attr_list.append({
          "name": dev,
          "vars": vars
      })              
  ```

- Apply the meta vars to all the devices at once:

  ```
  session.setDeviceAttributes(dev_attr_list)
  ```

Now you should be able to understand the entire solution, and this is how 
we have achieved our [Goal](#goal)!
