# xpectd: A Web Service to Simulate Various Outage Scenarios

## Installation

From the root of this repository

### Using pip

```bash
python -m pip install .
```

### Using uv

```bash
uv pip install .
```

## Usage

```bash
usage: xpectd [-h] [--address ADDRESS] [--port PORT] [--workers-connections WORKER_CONNECTIONS] --plan PLAN
A web service to simulate various outage scenarios.

optional arguments:
-h, --help            show this help message and exit
--address ADDRESS     The IP to bind to. (default: 127.0.0.1)
--port PORT           The port to bind to. (default: 8080)
--workers-connections WORKER_CONNECTIONS
                      The maximum number of simultaneous clients. (default: 1000)
--plan PLAN           The plan file to load. (default: None)
```

## Example Plan File

```yaml
scenarios:
- endpoint: scenario_one
  response:
    status: 200
    payload: Hi there
    min_time: 0
    max_time: 0.3
  outage:
    schedule: "*/1 * * * *"
    duration: 0
    response:
    - percentage: 20
      status: 200
      payload: Hi there
      min_time: 1
      max_time: 3
    - percentage: 80
      status: 500
      payload: Server Error
      min_time: 0
      max_time: 0
```

The above config file would start a web service with an endpoint named
`/scenario_one`. The nominal behavior is defined by the `response` values
whereas `status` determines the return code, `payload` the body of the
response, `min_time` the minimal time to respond, and `max_time` the maximum
time to respond.

The `outage` value determines the behavior when an outage is started for that
particular endpoint. `schedule` determines the start of an outage whilst
`duration` determines the length of the outage after which the outage
recovers to normal behavior. When `duration` is set to `0`, the scheduled
outage trigger is effectively disabled, meaning the only way is to manually
trigger an outage for that endpoint. See below for more information.

The `outage.response` value holds a list of responses that the endpoint will
return when the outage is enabled. The `percentage` value determines how much
percent of the requests should have the corresponding response behavior.

## Manually enabling an outage

If you're not making use of the scheduled outages by setting `.duration` to
`0`, you can still trigger an outage manually per endpoint. For example:

```bash
$ curl -XPOST http://localhost:8080/scenario_one/enable
{"status": "enabled"}
$ curl -XPOST http://localhost:8080/scenario_one/disable
{"status": "disabled"}
```
