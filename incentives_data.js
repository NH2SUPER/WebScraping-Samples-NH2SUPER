const puppeteer = require('puppeteer');
const XLSX = require('xlsx');

async function scrapeTable() {
    console.log("Launching browser...");
    const browser = await puppeteer.launch({ headless: false });  // Run in non-headless mode

    console.log("Opening new page...");
    const page = await browser.newPage();
    await page.setViewport({width:1920, height:1080});
                                          
    console.log("Navigating to page...");
    await page.goto('https://programs.dsireusa.org/system/program?zipcode=32804');
    await new Promise(r => setTimeout(r, 1000)); // wait til page loaded

    console.log("Scraping data...");

    let results = [];

    let nextPage = true;
    while (nextPage) {
        let newResults = await page.evaluate(() => {
            let rows = Array.from(document.querySelectorAll('tbody tr'));
            return rows.map(row => {
                let cells = Array.from(row.querySelectorAll('td'));
                return {
                    name: cells[0].querySelector('a').innerText,
                    state: cells[1].innerText,
                    category: cells[2].innerText,
                    policy: cells[3].innerText,
                    dateCreated: cells[4].innerText,
                    dateUpdated: cells[5].innerText
                };
            });
        });

        results = results.concat(newResults);

        try {
            // Check if "Next" button is disabled
            let disabled = await page.evaluate(() => {
                let nextButton = document.querySelector('.paginate_button.next');
                return nextButton.classList.contains('disabled');
            });

            if (!disabled) {
                // Click "Next" button and wait for page to load
                await page.click('.paginate_button.next');
                await new Promise(r => setTimeout(r, 1000)); // wait for 1000ms
            } else {
                nextPage = false;
            }
        } catch (error) {
            nextPage = false;
        }
    }

    console.log("Scraping completed. Here are the results:");
    console.log(results);

    console.log("Exporting data to Excel...");
    const wb = XLSX.utils.book_new();
    const ws = XLSX.utils.json_to_sheet(results);
    XLSX.utils.book_append_sheet(wb, ws, "Results");
    XLSX.writeFile(wb, "DSIRE_Programs.xlsx");

    console.log("Closing browser...");
    await browser.close();
}

scrapeTable();


//Denver postal codes