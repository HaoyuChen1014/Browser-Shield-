// Always show the green message by default
document.getElementById('safe').classList.remove('hidden');
document.getElementById('warning').classList.add('hidden');

chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
    let currentUrl = tabs[0].url;

    // Fetch the blacklist from local storage
    chrome.storage.local.get('blacklist', function (data) {
        let blacklist = data.blacklist || [];

        if (blacklist.includes(currentUrl)) {
            // Phishing site detected, show the warning message
            document.getElementById('safe').classList.add('hidden');
            document.getElementById('warning').classList.remove('hidden');
            console.log("URL is in the blacklist.");
        } else {
            // If not blacklisted, analyze the domain for suspicious characteristics
            const domain = new URL(currentUrl).hostname;

            // Dynamically create a script tag to load the classifier.js script
            const script = document.createElement('script');
            script.src = chrome.extension.getURL('Client_side/classifier.js');

            script.onload = function () {
                // Now you can use the analyzeDomain function
                analyzeDomain(domain).then(isSuspicious => {
                    if (isSuspicious) {
                        document.getElementById('warning').classList.remove('hidden');
                        document.getElementById('safe').classList.add('hidden');
                        console.log("URL is suspicious.");
                    } else {
                        // Site is not blacklisted and not suspicious
                        document.getElementById('warning').classList.add('hidden');
                        document.getElementById('safe').classList.remove('hidden');
                        console.log("URL is safe.");
                    }
                }).catch(error => {
                    console.error("Error analyzing domain:", error);
                });
            };

            document.head.appendChild(script);
        }
    });
});
