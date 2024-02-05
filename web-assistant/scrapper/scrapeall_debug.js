const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');
const url = require('url');
const depth = 3

const baseDirectory = './scraped-pages'; // Directory where files will be saved

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

    if (level > depth || visited.has(url) || url.startsWith('javascript:') || !isValidUrl(url)) {
        console.log(level, ' : Skipping URL:', url);
        return; // Skip if level is more than 3, page is already visited, or URL is invalid
    }

    console.log(level, ' : Scraping URL:', url);
        
    visited.add(url);

    await page.goto(url, { waitUntil: 'networkidle0' }).catch(e => console.error(`Failed to navigate: ${url}`, e));
    const content = await page.content();
    saveContentToFile(url, content, level);

    // Find all hyperlinks on the page
    hyperlinks = await page.$$eval('a', links => links.map(link => link.href));
    console.log(typeof(hyperlinks))
    //getAllMethods(hyperlinks)
    // console.log(level, ' found these hyper links:');
    // console.log(hyperlinks);

    //Clean unwanted URLS
    for (const link of hyperlinks) {
        if( (!link.includes("topic/") && !link.includes("article/")) || link.includes("nocache") ){
            hyperlinks = hyperlinks.filter(item => item !== link);  
        }
    }

    console.log(level, ' Filtered hyper links:');
    console.log(hyperlinks);

    for (const link of hyperlinks) {
        await scrapePage(page, link, level + 1, visited); // Recursively scrape the linked page
    }
}

function getAllMethods(obj) {
    let methods = new Set();
    console.log('Object is: ', obj.constructor.name)

    // Loop through each prototype in the chain
    while (obj) {
        // Get all property names
        Object.getOwnPropertyNames(obj).forEach(prop => {
            // Check if the property is a function (method)
            if (typeof obj[prop] === 'function') {
                methods.add(prop);
                console.log('>>>>>>>>> ', prop);
            }
        });

        // Move up the prototype chain
        obj = Object.getPrototypeOf(obj);
    }

    return Array.from(methods);
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

// Example usage
startScraping('https://help.salesloft.com/s/?language=en_US');
