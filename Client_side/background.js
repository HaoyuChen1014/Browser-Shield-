// Function to download data as a file on the user's system
function fetchAndUpdateBlacklist() {
    fetch('http://127.0.0.1:5000/getblacklist.json')
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // Save the fetched data to local storage
        chrome.storage.local.set({blacklist: data});
    })
    .catch(error => {
        console.log("There was a problem with the fetch operation:", error.message);
    });
}

// Fetch and store the blacklist when the browser starts and upon extension installation
chrome.runtime.onStartup.addListener(fetchAndUpdateBlacklist);
chrome.runtime.onInstalled.addListener(fetchAndUpdateBlacklist);

chrome.tabs.onUpdated.addListener(function(tabId, changeInfo, tab) {
    if (changeInfo.status === 'complete' && tab.active) {
        const currentUrl = tab.url;

        // Check if the URL is valid
        if (currentUrl && currentUrl.startsWith("http")) {
            chrome.storage.local.get(['blacklist'], function(data) {
                let blacklist = data.blacklist || [];

                if (blacklist.includes(currentUrl)) {
                    // Display a Chrome notification for blacklisted sites
                    chrome.notifications.create({
                        type: 'basic',
                        iconUrl: 'images/warning.png',
                        title: 'Warning!',
                        message: 'You are visiting a blacklisted site!'
                    });
                    return;  // exit early
                }

                // If not blacklisted and the URL is valid, analyze the domain for suspicious characteristics
                analyzeDomain(currentUrl).then(isSuspicious => {
                    if (isSuspicious) {
                        // Display a Chrome notification for suspicious sites
                        chrome.notifications.create({
                            type: 'basic',
                            iconUrl: 'images/warning.png',
                            title: 'Caution!',
                            message: 'This site seems suspicious!'
                        });
                    }
                }).catch(error => {
                    // Handle errors if analyzeDomain fails
                    console.error("Error analyzing domain:", error);
                });
            });
        }
    }
});
