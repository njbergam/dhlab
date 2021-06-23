// Function to use the ID of a function to get data and update DOM
function getData(id) {
    // Construct the request url
    const currentUrl = window.location.href;
    const baseUrl = currentUrl.substring(0, currentUrl.length - 18)
    const reqUrl = baseUrl + "projectData"

    fetch(reqUrl)
        .then(response => response.json())
        .then(data => {
            data.projects.forEach(element => {
                if (element.id == id) {
                    document.getElementById("title").textContent = element.title;
                    document.getElementById("desc").textContent = element.desc;
                    document.getElementById("org").textContent = element.org;
                }
            });

        })
}