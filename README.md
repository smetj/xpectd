# xpectd

A webservice with pre-defined behavior

## Installation

```
pip install xpectd
```

## Usage

```
xpectd --help
usage: xpectd [-h] [--address ADDRESS] [--port PORT] [--workers WORKERS] [--threads THREADS] --plan PLAN

Gyre Grafana cloud integration service.

optional arguments:
  -h, --help         show this help message and exit
  --address ADDRESS  The IP to bind to. (default: 127.0.0.1)
  --port PORT        The port to bind to. (default: 8080)
  --workers WORKERS  The number of processes to run. (default: 1)
  --threads THREADS  The number of threads per process. (default: 10)
  --plan PLAN        The plan file to load. (default: None)
```

## Example plan file

```
error_plan_1:
    outage_cron: "*/1 * * * *"
    outage_duration: 10
    outage_response:
        - return_code: 200
          percentage: 20
          min_duration: 1
          max_duration: 3
          payload: Hi there
        - return_code: 500
          percentage: 80
          min_duration: 0
          max_duration: 0
          payload: Server backend error
    nominal_return_code: 200
    nominal_payload: Hi there
    nominal_min_duration: 0
    nominal_max_duration: 0.3
```

The above config file would create an URL `/error_plan_1` which can be polled
by one or more web clients.  The `nominal_*` values determine the webserver
behavior for that endpoint under a nominal status.  `outage_cron` determines
when an outage for that endpoint should start whilst `outage_duration`
detmines the length of the outage.  `outage_reponse` describes how the outage
should behave.

You can manually start and stop the outage without using `outage_cron` and
`outage_duration` by sending a POST to `/error_plan_1/enable` or
`/error_plan_1/disable` respectively giving you control to start and stop the
outage behaviour.

## Misc information

- To disable a plan from being executed you can put `outage_duration` to `0`.
- If you choose 2 or more workers resulting into multiple processes it will
  throw off your percentages since clients will be connecting to the started
  processes in a random fashion.
- Your list of `outage_response` should always accumulate to `100%` in total
  otherwise the service will refuse to start.
