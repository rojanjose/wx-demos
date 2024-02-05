
const fs = require('fs').promises;


function extractTitle(url) {
    // Regex pattern to match the portion after the last '/' and before the '?'
    const pattern = /\/([^\/\?]+)(\?|$)/;
    const match = url.match(pattern);

    return match ? match[1] : null;
}

function convertToTopic(str) {
    return str
        // Split the string into words based on the hyphen
        .split('-')
        // Capitalize the first letter of each word and join with space
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');
}

function getID(url, startStrimg) {
    // Regex pattern to match the specific format of the string
    // This example assumes the format is a sequence of alphanumeric characters
    const pattern = `/${startStrimg}\/([A-Za-z0-9]+)/`;
    const match = url.match(pattern);

    return match ? match[1] : null;
}

function getToCLineItem(url, level, extension) {

    let tocLineItem = {};
    tocLineItem["level"] = level;
    tocLineItem["url"] =  url.substring(url.lastIndexOf('s/') + 2);
    tocLineItem["filename"] =  `${tocLineItem["url"].replace(/[^a-zA-Z0-9]/g, '_')}.${extension}`;
    title = extractTitle(url);
    if(title != null){
        tocLineItem["topic"] = convertToTopic(title);
    }else{
        tocLineItem["topic"] = "No found";
    }
    tocLineItem["id"] = "Unknown";
    if(url.includes("topic")){
        tocLineItem["contnenttype"] = "topic";
        tocLineItem["id"] = getID(url, "topic");
    }else if(url.includes("article")){
        tocLineItem["contnenttype"] = "article";
    }     

    return tocLineItem;
}


let tableOfContents = [];

const urls = [
    'https://help.salesloft.com/s/?language=en_US',
    'https://help.salesloft.com/s/topic/0TO3n000000RZhrGAG/user-guides?language=en_US',
    'https://help.salesloft.com/s/article/Need-Help-Salesloft-Support-Guide?language=en_US'
];


for (const url of urls) {
    console.log(`Processing URL: ${url}`);
    tocLineItem = getToCLineItem(url, 1, "txt")
    // console.log(tocLineItem)
    tableOfContents.push(tocLineItem);
}

console.log("Final list:")
console.log(tableOfContents)

fs.writeFile('tableOfContents.json', JSON.stringify(tableOfContents, null, 2), 'utf8');
console.log('Customer data has been written to customers.json');
