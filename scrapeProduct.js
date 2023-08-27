const puppeteer = require('puppeteer');
const XLSX = require('xlsx');

async function scrapeProduct() {
    console.log("Launching browser...");
    const browser = await puppeteer.launch({ headless: false });  // Run in non-headless mode

    console.log("Opening new page...");
    const page = await browser.newPage();
    await page.setViewport({width:1920, height:1080});
                                          
    console.log("Navigating to page...");
    await page.goto('https://www.sunhub.com/shop/product/solar-panels');
    await page.click('#main-cat-1'); // click the checkbox 1st time
    await new Promise(r => setTimeout(r, 1000)); // wait til page loaded
    await page.click('#main-cat-1'); // click the checkbox 2nd time
    await new Promise(r => setTimeout(r, 1000)); //wait til page loaded

    console.log("Scraping data...");

    let results = [];

    let nextPage = true;
    while (nextPage) {
        let productLinks = await page.evaluate(() => {
            let products = Array.from(document.querySelectorAll('.product.product-list'));
            return products.map(product => product.querySelector('h3.product-title a').href);
        });

        for (let productLink of productLinks) {
            const productPage = await browser.newPage();
            await productPage.setViewport({width:1920, height:1080});
            await productPage.goto(productLink);
            await new Promise(r => setTimeout(r, 1500)); // wait for 1000ms

            // Wait for the "Specifications" link to load
            await productPage.waitForSelector('.nav-link');

            // Click on the "Specifications" button
            await productPage.evaluate(() => {
            let navLinks = Array.from(document.querySelectorAll('.nav-link'));
            let specificationsLink = navLinks.find(link => link.textContent.includes('Specifications'));
            specificationsLink.click();
            });
            await new Promise(r => setTimeout(r, 1500)); // wait for 1000ms

            let productData = await productPage.evaluate(() => {
                let title = document.querySelector('h1.product-title').innerText;
                let price = document.querySelector('.product-price.mb-0').innerText;
                let rows = Array.from(document.querySelectorAll('.product-desc-content table tr'));
                let data = {};
                rows.forEach(row => {
                    let ths = Array.from(row.querySelectorAll('th'));
                    let tds = Array.from(row.querySelectorAll('td'));
                    ths.forEach((th, index) => {
                        let key = th.innerText.replace(':', '').trim();
                        let value = tds[index] ? tds[index].innerText.trim() : 'N/A';
                        data[key] = value;
                    });
                });
                return {title, price, ...data};
            });

            results.push(productData);

            await productPage.close();
        }

        // Check if "Next" button is disabled
        let disabled = await page.evaluate(() => {
            let nextButton = document.querySelector('.ant-pagination-next');
            return nextButton.classList.contains('ant-pagination-disabled');
        });

        if (!disabled) {
            // Click "Next" button and wait for page to load
            await page.click('.ant-pagination-next');
            await new Promise(r => setTimeout(r, 1000)); // wait for 1000ms
        } else {
            nextPage = false;
        }
    }

    console.log("Scraping completed. Here are the results:");
    console.log(results);

    console.log("Exporting data to Excel...");
    const wb = XLSX.utils.book_new();
    const ws = XLSX.utils.json_to_sheet(results);
    XLSX.utils.book_append_sheet(wb, ws, "Results");
    XLSX.writeFile(wb, "Sunhub_SolarPanels.xlsx");

    console.log("Closing browser...");
    await browser.close();
}

scrapeProduct();
