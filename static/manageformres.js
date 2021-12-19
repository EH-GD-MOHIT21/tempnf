const token = document.URL.split('/')[document.URL.split('/').length - 1]


async function mohit(filters) {
    let response = await fetch('/getresform/' + token, {
        credentials: 'include',
        method: 'POST',
        mode: 'same-origin',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            "filters": filters
        })
    })
    if (response.ok) {
        let json = await response.json();
        let message = json["message"]
        let data = json["data"]
        let extdata = json["extdata"]
        if (message == "success") {
            console.log(data);
            showdataonpage(data, extdata);
        }
    } else {
        alert("HTTP-Error: " + response.status);
    }
}
mohit(null)

function showdataonpage(data, extdata) {
    document.getElementById("formtitle").textContent = extdata["title"]
    document.getElementById("formdesc").textContent = extdata["desc"]
    document.getElementById("formcreator").textContent = "Created by: " + extdata["creator"]
    document.getElementById("formdate").textContent = "Date Created: " + extdata["date"]
    if (data == null) {
        h1 = document.createElement('h1')
        h1.textContent = "No Responses to display"
        body = document.querySelector('body')
        body.appendChild(h1)
    } else {
        document.getElementById('injection').remove();
        var maindiv = document.createElement('div')
        maindiv.setAttribute('id', 'injection')
        var names = data["names"]
        var emails = data["emails"]
        var address = data["address"]
        var phone_no = data["phone_no"]

        var pdiv = document.createElement('div');
        pdiv.setAttribute('class', 'mainposrel');
        var div = document.createElement('li')
        div.setAttribute('class', 'injecting_property')
        var h3 = document.createElement('h3')
        h3.textContent = "Name";
        var p0 = document.createElement('a')
        p0.textContent = "Email";
        var p1 = document.createElement('p')
        p1.textContent = "Address";
        var p2 = document.createElement('p')
        p2.textContent = "Phone";
        div.appendChild(h3);
        div.appendChild(p0);
        div.appendChild(p1);
        div.appendChild(p2);
        pdiv.appendChild(div);
        maindiv.appendChild(pdiv);

        for (var i = 0; i < names.length; i++) {
            var pdiv = document.createElement('div');
            pdiv.setAttribute('class', 'posrel');
            var div = document.createElement('li')
            div.setAttribute('class', 'injecting_property')
            var h3 = document.createElement('h3')
            h3.textContent = names[i];
            var p0 = document.createElement('a')
            p0.textContent = emails[i];
            p0.href = '/showresponses/' + token + '/filter?email=' + emails[i]
            p0.target = "_blank"
            var p1 = document.createElement('p')
            p1.textContent = address[i];
            var p2 = document.createElement('p')
            p2.textContent = phone_no[i];
            div.appendChild(h3);
            div.appendChild(p0);
            div.appendChild(p1);
            div.appendChild(p2);
            pdiv.appendChild(div);
            maindiv.appendChild(pdiv);
        }
        document.querySelector('body').appendChild(maindiv);
    }
    document.getElementById('dispno').style.display = 'none';
}

document.getElementById('choice').addEventListener('change', function() {
    mohit(this.value);
})