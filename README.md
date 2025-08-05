# PUBLIC DATA SCRAPER API

A FastAPI server that uses Selenium and residential proxies to scrape Google Search results and extract the main content from websites. It's designed for market research, SEO analysis, and content aggregation, and is ready for deployment on Heroku.

## FEATURES
Automate Research: Enter a search query and instantly get back clean, readable text from the top search results.

Bypass Blocks: Built-in residential proxy support helps avoid IP bans and ensures reliable scraping.

Developer & n8n Friendly: Simple JSON input/output, ready for Heroku deployment, and perfect for integrating directly into n8n workflows.

## QUICK START: DEPLOYMENT & USAGE
Deploy to Heroku:

Create a Heroku app and connect your Git repository.

Add the required buildpacks: heroku/chrome-for-testing and heroku/python.

Set your SECRET_API_KEY and proxy credentials (PROXY_HOST, PROXY_PORT, etc.) in the app's Config Vars.

Push your code to deploy.

Send a Request:
Once deployed, send a POST request to the /scrape-public endpoint.

## EXAMPLE CURL REQUEST
    curl -X POST "https://your-app-name.herokuapp.com/scrape-public" \
    -H "Content-Type: application/json" \
    -H "X-API-Key: your-strong-and-secret-api-key" \
    -d '{
        "query": "latest trends in generative AI",
        "num_results": 3
    }'

## EXAMPLE N8N INTEGRATION
Use the HTTP Request node in n8n.

Set the URL to your Heroku app's URL (https://.../scrape-public).

Add a Header for your X-API-Key.

In the Body, provide the JSON with your search query.

The output of the node will be the structured data (title, URL, content) which you can then pass to other nodes like Google Sheets, Airtable, or an LLM for summarization.

## DISCLAIMER
This tool is for educational purposes only. Web scraping may be against the terms of service of some websites. Use this script responsibly and at your own risk. The author is not responsible for any misuse of this tool.