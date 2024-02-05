const puppeteer = require('puppeteer');

async function crawlSPA(url, waitForSelector) {
    // Launch the browser
    const browser = await puppeteer.launch();
    const page = await browser.newPage();

    // Navigate to the URL & waits until the network is idle (no more than 0 network connections for at least 500 ms)
    await page.goto(url, { waitUntil: 'networkidle0' }).catch(e => console.error(`Failed to navigate: ${url}`, e));
    
    // Wait for the specific element to be loaded if necessary
    if (waitForSelector) {
        await page.waitForSelector(waitForSelector).catch(e => console.error(`Failed to navigate: ${url}`, e));
    }

    // Now, the page is fully loaded, and you can scrape the data you need
    // For example, let's extract the inner text of the awaited element
    const data = await page.evaluate(selector => {
        const element = document.querySelector(selector);
        //return element ? element.innerText : null;
        return element ? element.innerHTML : null;
    }, waitForSelector);

    if(data == null){
        console.log('Failed to scrape from :', url);
    }else{
        console.log('Extracted Data:', data);
    } 
    
    // Close the browser
    await browser.close();
}

//Start crawling
crawlSPA('https://help.salesloft.com/s/article/Manage-Messenger', '.body');
// crawlSPA('https://help.salesloft.com/s/article/List-of-Cadence-Frameworks#Build_Pipeline', '.body');
// crawlSPA('https://help.salesloft.com/s/article/Your-Personal-Settings?language=en_US', '.body');
//crawlSPA('https://help.salesloft.com/s/?language=en_US', '.body');
