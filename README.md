link-api
REST API built with FastAPI and SQLite. CRUD endpoints for managing links with click tracking.

A REST API I built from scratch using FastAPI and SQLite. It's basically the backend for a Linktree style app. You can store, manage, and track clicks on your personal links through a clean API.
What it does

Add links with a title, URL, and icon
Get all your links
Update existing links
Delete links
Track how many times each link gets clicked
View stats — total links and total clicks

How to run it

Clone the repo
Install dependencies:

   pip3 install fastapi uvicorn

Start the server:

   python3 -m uvicorn FASTAPI:app --reload

Open your browser and go to:

http://localhost:8000/docs — interactive API docs where you can test every endpoint
http://localhost:8000/links — raw JSON response



Endpoints
MethodEndpointWhat it doesGET/linksReturns all linksPOST/linksAdds a new linkPUT/links/{id}Updates a link by IDDELETE/links/{id}Deletes a link by IDGET/links/{id}/clickIncrements click countGET/statsReturns total links and total clicks
Tech used

Python
FastAPI
SQLite (auto-created on first run)
Pydantic (data validation)
