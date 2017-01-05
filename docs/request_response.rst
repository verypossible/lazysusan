.. _request_response:

============================
Request/response cycle
============================

- Look at the current state
- Grab the matching yaml block for the current state
- Look at the Intent sent in the request
- Find the matching Intent in the ``branches`` map
- Reply with the response for that matching branch or ``default`` if the Intent isn't defined in
  the ``branches`` map


