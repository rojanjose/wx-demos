const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');
const url = require('url');

const baseURL = 'https://help.salesloft.com/s/?language=en_US'
const depth = 50

// Directory where files will be saved
const baseDirectory = './scraped-pages'; 

// Function to check if a URL is valid
function isValidUrl(string) {
    try {
        new URL(string);
        return true;
    } catch (_) {
        console.log('Invalid URL:', string);
        return false;
    }
}


// Function to save content to a file
function saveContentToFile(url, content, level) {

    url = url.substring(url.lastIndexOf('s/') + 2);
    const fileName = `L${level}-${url.replace(/[^a-zA-Z0-9]/g, '_')}.html`;
    const filePath = path.join(baseDirectory, fileName);
    fs.writeFileSync(filePath, content);
    console.log(`Saved: ${filePath}`);
}

// Function to scrape a single page
async function scrapePage(page, url, level = 1, visited = new Set()) {

    waitForSelector = '.body';

    // Skip if level is more than depth, page is already visited, or URL is invalid
    if (level > depth || visited.has(url) || url.startsWith('javascript:') || !isValidUrl(url)) {
        // console.log(level, ' : Skipping URL:', url);
        return; 
    }        
    visited.add(url);
    console.log(level, '> Scraping URL:', url);

    try{

        // Navigate to the URL && waits until the network is idle (no more than 0 network connections for at least 500 ms)
        await page.goto(url, { waitUntil: 'networkidle0', timeout: 30000 })

        // Wait for the specific element to be loaded if necessary
        if (waitForSelector) {
            await page.waitForSelector(waitForSelector)
        }

        // Now, the page is fully loaded, scrape the data
        // Extract the inner html of the awaited element
        const content = await page.evaluate(selector => {
            const element = document.querySelector(selector);
            return element ? element.innerHTML : null;
        }, waitForSelector)

        if(content == null){
            console.log('Failed to scrape from :', url);
            return;
        }

        //Save the content
        saveContentToFile(url, content, level);
        
        // Find all hyperlinks on the page
        hyperlinks = await page.$$eval('a', links => links.map(link => link.href));
    
        //Clean unwanted URLS
        for (const link of hyperlinks) {
            if( (!link.includes("topic/") && !link.includes("article/")) || link.includes("nocache") ){
                hyperlinks = hyperlinks.filter(item => item !== link);  
            }
        }
    
        for (const link of hyperlinks) {
            // Recursively scrape the linked page
            await scrapePage(page, link, level + 1, visited);
        }

    } catch (error) {
        console.error(`Failed to scrape: ${url}`, error);
        return false;
    }

}

// Main function to start scraping
async function startScraping(baseUrl) {
    // Ensure base directory exists
    if (!fs.existsSync(baseDirectory)) {
        fs.mkdirSync(baseDirectory);
    }

    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    await scrapePage(page, baseUrl);
    await browser.close();
}

// Start scraping
startScraping(baseURL);
