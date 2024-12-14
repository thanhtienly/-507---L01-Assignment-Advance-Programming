# Transaction Search API Application (Without Front End)

## How to run the application
1. `git clone https://github.com/thanhtienly/-507---L01-Assignment-Advance-Programming.git`
2. `cd ./-507---L01-Assignment-Advance-Programming`
3. `docker compose up`
## Note:
Sometimes, you need to change the application's port because of a conflict with another application on your machine; you can find out and change it in the docker-compose.yml file.
## API Endpoint & Response format
API Endpoint: http://localhost:8000/query?q=searchTerm </br>
Response Format: 
```
  "data": [
    {
      "date": "10/09/2024_5245.55229",
      "transactionId": "47311",
      "credit": "1000000",
      "detail": "MBVCB.6991846866.NGUYEN VAN HOANG ung ho dong bao lu lut.CT tu 0721000582827 NGUYEN VAN HOANG toi 0011001932418 MAT TRAN TO QUOC VN - BAN CUU TRO TW\n"
    },
    ...
  ],
  "page": 1,
  "num_of_transactions": 366
```
