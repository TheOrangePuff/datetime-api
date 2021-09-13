# Datetime API

[![Test Datetime API](https://github.com/TheOrangePuff/datetime-api/actions/workflows/test.yml/badge.svg)](https://github.com/TheOrangePuff/datetime-api/actions/workflows/test.yml)
[![AWS Deployment](https://github.com/TheOrangePuff/datetime-api/actions/workflows/deploy.yml/badge.svg)](https://github.com/TheOrangePuff/datetime-api/actions/workflows/deploy.yml)

An API to calculate the difference in time between two dates.

# Usage

API Parameters

Parameter | Description | Valid Data
--------- | ------- | -------
start_date | The first datetime parameter | 2020-01-01, 2020-12-31T0930, 2020-12-31T0000-1200
end_date | The second datetime parameter | 2020-01-01, 2020-12-31T0930, 2020-12-31T0000-1200
unit | The unit of time to return | seconds, minutes, hours, days, weeks, years

Call the API via GET or POST
```bash
curl -X GET "https://api.danielvdp.com/days?start_date=2020-08-10&end_date=2020-10-17"
curl -X POST "https://api.danielvdp.com/days?start_date=2020-08-10&end_date=2020-10-17"
```

To find the number of weekdays between the two dates
```bash
curl -X GET "https://api.danielvdp.com/weekdays?start_date=2020-01-01&end_date=2021-01-01"
```

To find the number complete weeks between the two dates
```bash
curl -X GET "https://api.danielvdp.com/completeweeks?start_date=2020-01-01&end_date=2021-01-01"
```

To find the number of hours between two dates
```bash
curl -X GET "https://api.danielvdp.com/days?start_date=2020-01-01&end_date=2021-01-01&unit=hours"
```

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
