# Datetime API

An API to calculate the difference in time between two dates.

# Installation

Clone the repository
```
git clone git@github.com:TheOrangePuff/datetime-api.git
```

Build and run the Dockerfile
```
docker build -t datetime_api .
docker run -p 80:80 datetime_api
```

Call the API
```
curl -X POST "localhost/days?start_date=2020-08-10&end_date=2020-10-17"
```

# License

This project is licensed under the MIT License.

See [LICENSE](LICENSE) for more information.
