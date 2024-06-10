# network-coverage
Miniature API to retrieve data about network coverage. Technical assignment for papernest

## How to run

1. Create a `.env` file in the project directory with `MONGO_USER` and `MONGO_PASS` values
2. Add network coverage data in CSV format and operators table in wikitext table format to the `data-coverage` directory. For operators data I copied table contents without a header from [this article](https://fr.wikipedia.org/w/index.php?title=Mobile_Network_Code&action=edit)
3. Run `docker-compose up --build`
4. When running for the first time create an index in MongoDB collection running following command inside the `api` container:
`flask init-coverage-collection /data/{operators_filename} /data/{coverage_filename}`
