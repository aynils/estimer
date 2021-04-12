docker build -t estimer:test . &&
docker run -i -t --network="host" --env-file=.env.local estimer:test
