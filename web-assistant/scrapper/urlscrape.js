const puppeteer = require('puppeteer');

async function scrapeURLs(url, linkSelector) {
    // Launch the browser
    const browser = await puppeteer.launch();
    const page = await browser.newPage();

    // Navigate to the URL
    await page.goto(url, { waitUntil: 'networkidle0' });

    // Scrape the current page URL
    const currentPageURL = page.url();
    console.log('Current Page URL:', currentPageURL);

    // Scrape URLs of specific elements (e.g., links)
    const links = await page.evaluate(selector => {
        const elements = Array.from(document.querySelectorAll(selector));
        return elements.map(element => element.href);
    }, linkSelector);

    console.log('Extracted Links:', links);

    // Close the browser
    await browser.close();
}

// Example usage
scrapeURLs('https://help.salesloft.com/s/?language=en_US', 'a'); // 'a' is the selector for anchor tags (links)
