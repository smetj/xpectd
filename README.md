# xpectd

A webservice to simulate various outage scenarios.

## Installation

```
python setup.py install
```

## Docker images

Docker builds can be found on [Dockerhub](https://hub.docker.com/r/smetj/xpectd)

```bash
docker run -t -i -p 8080:8080 -v $(pwd)/test_plan.yml:/test_plan.yml smetj/xpectd:latest \
  --address 0.0.0.0 \
  --plan /test_plan.yml
```

## Usage

```
xpectd --help
usage: xpectd [-h] [--address ADDRESS] [--port PORT] [--workers WORKERS] [--threads THREADS] --plan PLAN

A webservice to simulate various outage scenarios.

optional arguments:
  -h, --help         show this help message and exit
  --address ADDRESS  The IP to bind to. (default: 127.0.0.1)
  --port PORT        The port to bind to. (default: 8080)
  --workers WORKERS  The number of processes to run. (default: 1)
  --threads THREADS  The number of threads per process. (default: 10)
  --plan PLAN        The plan file to load. (default: None)
```

## Example plan file

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
