console.log("Hi from background script file")
chrome.action.onClicked.addListener((tab) => {
    console.log("Extension icon clicked! Attempting to execute script...");

    chrome.scripting.executeScript({
        target: { tabId: tab.id },
        func: () => {
            console.log("Script executed inside the page context!");
            alert("Hello from my extension!");
        }
    }).then(() => {
        console.log("Script execution successful!");
    }).catch((error) => {
        console.error("Error executing script:", error);
    });
});
