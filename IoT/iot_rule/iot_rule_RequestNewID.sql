SELECT *, topic(3) as thingName FROM '$aws/things/+/shadow/update' WHERE state.desired.state = 'RequestNewID'

--jobs
--lambda GenerateNewID
