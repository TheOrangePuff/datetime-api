# Datetime API

[![Test Datetime API](https://github.com/TheOrangePuff/datetime-api/actions/workflows/test.yml/badge.svg)](https://github.com/TheOrangePuff/datetime-api/actions/workflows/test.yml)
[![AWS Deployment](https://github.com/TheOrangePuff/datetime-api/actions/workflows/deploy.yml/badge.svg)](https://github.com/TheOrangePuff/datetime-api/actions/workflows/deploy.yml)

An API to calculate the difference in time between two dates.

# Installation

Clone the repository
```bash
git clone git@github.com:TheOrangePuff/datetime-api.git && cd datetime-api
```

Build and run the Dockerfile
```bash
docker build -t datetime_api .
docker run -p 80:80 datetime_api
```

Call the API
```bash
curl -X POST "localhost/days?start_date=2020-08-10&end_date=2020-10-17"
```

# License

This project is licensed under the MIT License.

See [LICENSE](LICENSE) for more information.
