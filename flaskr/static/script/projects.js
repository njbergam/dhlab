// Construct the request url
const currentUrl = window.location.href;
const baseUrl = currentUrl.substring(0, currentUrl.length - 8)
const reqUrl = baseUrl + "projectData"

// Use fetch library to make the request
fetch(reqUrl)
    .then(response => response.json())
    .then(data => {
        // Update the dom using the data
        data.projects.forEach(element => {
          console.log(element)
            const htmlString = `<div class="card mb-3" onclick="handleClick('${element.id}')" style="max-width: 840px;">
            <div class="row g-0">
              <div class="col-md-4">
                <img
                  src="${element.imgPath}"
                  alt="..."
                  class="img-fluid"
                />
              </div>
              <div class="col-md-8">
                <div class="card-body">
                  <h5 class="card-title"> ${element.title} </h5>
                  <p class="card-text"> ${element.desc}</p>
                  <p class="card-text">
                    <small class="text-muted">${element.org}</small>
                  </p>
                </div>
              </div>
            </div>
          </div>`

          document.getElementById("allProjects").innerHTML += htmlString;
        });
    })
    .catch(error => {
        console.log("An error has occurred.")
        console.log(error)
    })

function handleClick(elementId) {
  console.log(baseUrl)
  window.location.replace(baseUrl + "projects/single/" + elementId)
}